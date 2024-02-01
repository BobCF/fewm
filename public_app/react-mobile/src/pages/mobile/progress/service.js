import http from '../../../utils/http';

/**
 * 获取测试计划列表
 */
function getList(param, id) {
  return new Promise((resolve, reject) => {
    http("post", (id ? `active-testcycle/${id}/` : 'active-testcycle/'), { status: 'AssignmentCompleted', page_size: 10, ...param }).then(res => {
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