# 每次启动项目，将代码拷贝一份作为启动项目的执行代码
#

from pyspider.database.mongodb.projectdb import ProjectDB


class CopyProject:

    def __init__(self):
        url = 'mongodb://root:8a2p9j3x9g@3.134.227.240/projectdb?authSource=admin'
        self.db = ProjectDB(url, database='projectdb')

    def start_copy(self, project_name):
        # self.collection['']
        pipeline = [
            # {"$match": {"result.keyword":{"$eq":"@Frontrunneroutfitters"}}},
            {"$match": {"result.name": {"$eq": project_name}}},
        ]
        # tk_code = self.db.collection.aggregate(pipeline)
        # print(list(tk_code))
        # return list(tk_code)

        return self.db.get(project_name)


