import{_ as x,r as T,g as j,a as $,b as s,o as p,c as u,d as m,t as i,e as o,w as t,F as f,f as B}from"./index-49328046.js";const C={__name:"task",setup(U){const k=T(0),y=j(),r=$({form:{keyword:"kid build a robot"},rule:{orderId:[{required:!0,message:"单号必须填写"}],name:[{required:!0,message:"會員ID/電話/姓名必须填写"}]}}),_=[{val:"ScrapingTikTokPostsByCharles",name:"tiktok抓取",keyword:""},{val:"ScrapingTaskDispatcher",name:"任务分发",keyword:""},{val:"ScrapingYoutubeVideosByKeywordsV001",name:"Youtube抓取",keyword:""},{val:"ScrapingFacebookPageIdBykeywords",name:"Facebook抓取",keyword:""},{val:"ScrapingTikTokUserPostsByUniqueId",name:"TikTokUserPosts",keyword:""},{val:"ScrapingInstagramDispathcer",name:"ins抓取",keyword:"tagArr"}],w=(a,e)=>{console.log("onSelect",a,e)},g=async()=>{let a=r.form.project,e=r.form.keyword,l="keyword";_.forEach(n=>{n.val==a&&(l=n.keyword||"keyword")}),console.log("project",a,l,e);let d=await b(a,e,l);console.log(d)},b=async(a,e,l)=>{let d=`data:,on_message?keywords=${e}&task=${a}`;const n=`project=${a}&key=${l}&keyword=${e}&url=${encodeURIComponent(d)}`;return await y.proxy.$api.dispatcher(n)};return(a,e)=>{const l=s("a-input"),d=s("a-form-item"),n=s("a-col"),v=s("a-option"),h=s("a-select"),I=s("a-button"),S=s("a-row"),V=s("a-form");return p(),u(f,null,[m(i(r.form)+" ",1),o(V,{"auto-label-width":"",class:"input-zh",ref_key:"formRef",ref:k,size:"large",model:r.form,style:{width:"800px"},onSubmit:g},{default:t(()=>[o(S,{gutter:2},{default:t(()=>[o(n,{span:12},{default:t(()=>[o(d,{field:"orderId",label:"关键词"},{default:t(()=>[o(l,{modelValue:r.form.keyword,"onUpdate:modelValue":e[0]||(e[0]=c=>r.form.keyword=c),placeholder:"输入抓取关键词"},null,8,["modelValue"])]),_:1})]),_:1}),o(n,{span:12},{default:t(()=>[o(d,{field:"orderId",label:"项目"},{default:t(()=>[o(h,{onChange:w,modelValue:r.form.project,"onUpdate:modelValue":e[1]||(e[1]=c=>r.form.project=c),placeholder:"选择抓取项目"},{default:t(()=>[(p(),u(f,null,B(_,c=>o(v,{value:c.val,key:c.val},{default:t(()=>[m(i(c.name),1)]),_:2},1032,["value"])),64))]),_:1},8,["modelValue"])]),_:1})]),_:1}),o(n,{span:24},{default:t(()=>[o(d,{field:"orderId"},{default:t(()=>[o(I,{"html-type":"submit"},{default:t(()=>[m("确认保存")]),_:1})]),_:1})]),_:1})]),_:1})]),_:1},8,["model"])],64)}}},F=x(C,[["__scopeId","data-v-d35b1d06"]]);export{F as default};
