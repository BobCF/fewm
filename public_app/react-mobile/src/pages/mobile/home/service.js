import http from '../../../utils/http';

// 获取主页统计数据
function getList(params) {
  return new Promise((resolve, reject) => {
    http("post", `indexview/`, { ...params, page_size: 10 }).then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}

export {
  getList
}