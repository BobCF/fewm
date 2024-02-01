import http from '../../utils/http';

function loginUser(params){
  return new Promise((resolve, reject) => {
    http("post", 'login/', params, '',false).then(res => {
      resolve (res);
    },error => {
      console.log("网络异常~",error);
      reject(error)
    })
  }) 
}

export {
  loginUser
}