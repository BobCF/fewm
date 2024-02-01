import http from '../../../utils/http';

/**
 * 获取测试计划列表
 */
function getData() {
  return new Promise((resolve, reject) => {
    http("post", '/myview/').then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}

export {
  getData
}