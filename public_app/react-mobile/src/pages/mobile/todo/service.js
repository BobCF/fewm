import http from '../../../utils/http';
/**
 * 获取首页列表
 */
/**
 * 获取测试计划列表
 */
function getList(param, id) {
  return new Promise((resolve, reject) => {
    http("post", (id ? `active-testcycle/${id}/` : 'active-testcycle/'), { page_size: 10, ...param }).then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}
function getCaseList(id, params) {
  return new Promise((resolve, reject) => {
    http("post", `active-testcases/${id}/`, { ...params }).then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}

// 执行textstep
function setStep(id, params, c_id) {
  return new Promise((resolve, reject) => {
    http("post", `active-testcases/${id}/${c_id}/execution/`, { ...params }).then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}

// 开始执行textstep
function startStep(id, params, c_id) {
  return new Promise((resolve, reject) => {
    http("post", `active-testcases/${id}/${c_id}/start/`, { ...params }).then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}
// 重新执行textstep
function reStartStep(id, params, c_id) {
  return new Promise((resolve, reject) => {
    http("post", `active-testcases/${id}/${c_id}/restart/`).then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}
// 提交结果textstep
function completeStep(id, params, c_id) {
  return new Promise((resolve, reject) => {
    http("post", `active-testcases/${id}/${c_id}/complete/`).then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}
// 分配任务
function assignmentStep(id, params) {
  return new Promise((resolve, reject) => {
    http("post", `active-testcycle/${id}/assignment/`, { ...params }).then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}
// 获取分配人员
function getUserList() {
  return new Promise((resolve, reject) => {
    http("post", 'users/').then(res => {
      resolve(res);
    }, error => {
      console.log("网络异常~", error);
      reject(error)
    })
  })
}

export {
  getList,
  getCaseList,
  setStep,
  startStep,
  reStartStep,
  completeStep,
  assignmentStep,
  getUserList
}