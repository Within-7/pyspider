#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-02-22 23:20:39

import socket
import hashlib
import six
from six import iteritems, itervalues
from flask import render_template, request, json

try:
    import flask_login as login
except ImportError:
    from flask.ext import login

from .app import app

index_fields = ['name', 'group', 'status', 'comments', 'rate', 'burst', 'updatetime']
md5string = lambda x: hashlib.md5(utf8(x)).hexdigest()


def utf8(string):
    """
    Make sure string is utf8 encoded bytes.

    If parameter is a object, object.__str__ will been called before encode as bytes
    """
    if isinstance(string, six.text_type):
        return string.encode('utf8')
    elif isinstance(string, six.binary_type):
        return string
    else:
        return six.text_type(string).encode('utf8')

@app.route('/')
def index():
    projectdb = app.config['projectdb']
    projects = sorted(projectdb.get_all(fields=index_fields),
                      key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
    return render_template("index.html", projects=projects)

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/queues')
def get_queues():
    def try_get_qsize(queue):
        if queue is None:
            return 'None'
        try:
            return queue.qsize()
        except Exception as e:
            return "%r" % e

    result = {}
    queues = app.config.get('queues', {})
    for key in queues:
        result[key] = try_get_qsize(queues[key])
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


@app.route('/update', methods=['POST', ])
def project_update():
    projectdb = app.config['projectdb']
    project = request.form['pk']
    name = request.form['name']
    value = request.form['value']

    project_info = projectdb.get(project, fields=('name', 'group'))
    if not project_info:
        return "no such project.", 404
    if 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    if name not in ('group', 'status', 'rate'):
        return 'unknown field: %s' % name, 400
    if name == 'rate':
        value = value.split('/')
        if len(value) != 2:
            return 'format error: rate/burst', 400
        rate = float(value[0])
        burst = float(value[1])
        update = {
            'rate': min(rate, app.config.get('max_rate', rate)),
            'burst': min(burst, app.config.get('max_burst', burst)),
        }
    else:
        update = {
            name: value
        }

    ret = projectdb.update(project, update)
    if ret:
        rpc = app.config['scheduler_rpc']
        if rpc is not None:
            try:
                rpc.update_project()
            except socket.error as e:
                app.logger.warning('connect to scheduler rpc error: %r', e)
                return 'rpc error', 200
        return 'ok', 200
    else:
        app.logger.warning("[webui index] projectdb.update() error - res: {}".format(ret))
        return 'update error', 500


@app.route('/counter')
def counter():
    rpc = app.config['scheduler_rpc']
    if rpc is None:
        return json.dumps({})

    result = {}
    try:
        data = rpc.webui_update()
        for type, counters in iteritems(data['counter']):
            for project, counter in iteritems(counters):
                result.setdefault(project, {})[type] = counter
        for project, paused in iteritems(data['pause_status']):
            result.setdefault(project, {})['paused'] = paused
    except socket.error as e:
        app.logger.warning('connect to scheduler rpc error: %r', e)
        return json.dumps({}), 200, {'Content-Type': 'application/json'}

    return json.dumps(result), 200, {'Content-Type': 'application/json'}

@app.route('/test', methods=['POST', ])
def test():
    value = request.form['value']
    return f'ok:{value}', 200

@app.route('/dispatcher', methods=['POST', ])
def dispatchertask():
    rpc = app.config['scheduler_rpc']
    if rpc is None:
        return json.dumps({})

    projectdb = app.config['projectdb']

    project = request.form['project']   # 项目文件名称
    key = request.form['key']           # 不同项目需要传入的参数
    keyword = request.form['keyword']   # 传入的搜索词
    url = request.form['url']   # 传入的url唯一值

    if not project:
        return "no such request project.", 404
    
    if not url:
        return "no such request url.", 404

    if not key:
        return "no such request key.", 404
    
    if not keyword:
        return "no such request keyword.", 404
    
    message = {
        key: keyword
    }

    project_info = projectdb.get(project, fields=('name', 'group'))
    if not project_info:
        return "no such project.", 404
    if 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    # newtask = {
    #     # "taskid": md5string(url),
    #     'taskid': md5string('data:,on_message'),
    #     "project": project,
    #     # "url": url,
    #     'url': 'data:,on_message',
    #     "fetch": {
    #         "save": ('__command__', message),
    #     },
    #     "process": {
    #         "callback": "_on_message",
    #     },
    #     # "schedule": {
    #     #     "age": 0,
    #     #     "priority": 9,
    #     #     "force_update": True,
    #     # },
    # }

    sendtask = {
        'taskid': md5string('data:,on_message'),
        'project': project,
        'url': 'data:,on_message',
        'fetch': {
            'save': ('__command__', message),
        },
        'process': {
            'callback': '_on_message',
        }
    }

    try:
        # send_task
        # ret = rpc.newtask(sendtask)
        ret = rpc.send_task(sendtask)
    except socket.error as e:
        app.logger.warning('connect to scheduler rpc error: %r', e)
        return json.dumps({"result": False}), 200, {'Content-Type': 'application/json'}
    return json.dumps({"result": ret}), 200, {'Content-Type': 'application/json'}

@app.route('/run', methods=['POST', ])
def runtask():
    rpc = app.config['scheduler_rpc']
    if rpc is None:
        return json.dumps({})

    projectdb = app.config['projectdb']
    project = request.form['project']
    project_info = projectdb.get(project, fields=('name', 'group'))
    if not project_info:
        return "no such project.", 404
    if 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    newtask = {
        "project": project,
        "taskid": "on_start",
        "url": "data:,on_start",
        "process": {
            "callback": "on_start",
        },
        "schedule": {
            "age": 0,
            "priority": 9,
            "force_update": True,
        },
    }

    try:
        ret = rpc.newtask(newtask)
    except socket.error as e:
        app.logger.warning('connect to scheduler rpc error: %r', e)
        return json.dumps({"result": False}), 200, {'Content-Type': 'application/json'}
    return json.dumps({"result": ret}), 200, {'Content-Type': 'application/json'}


@app.route('/robots.txt')
def robots():
    return """User-agent: *
Disallow: /
Allow: /$
Allow: /debug
Disallow: /debug/*?taskid=*
""", 200, {'Content-Type': 'text/plain'}
