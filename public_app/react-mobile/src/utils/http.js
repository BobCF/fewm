/**
 * 网络请求配置
 */
import axios from "axios";

const INIT_BASE_URL = 'http://121.40.124.59:18000/' // 阿里云地址
// const INIT_BASE_URL = 'http://10.238.2.206:8082/' // 本地测试地址

// const urlList = ['login/', 'upload/', 'getTestPlan/'] // 不需要携带token, assign的接口

const axiosInstance = axios.create({
    timeout: 100000
});

/**
 * http request 拦截器
 */
axiosInstance.interceptors.request.use(
    (config) => {
        config.data = config.data;
        config.headers = {
            "Content-Type": "application/json",
        };
        // config.withCredentials = true
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

/**
 * http response 拦截器
 */
axiosInstance.interceptors.response.use(
    (response) => {
        if (response.data.errCode === 2) {
            console.log("过期");
        }
        return response;
    },
    (error) => {
        console.log("请求出错：", error);
        return error
    }
);

/**
 * 封装get方法
 * @param url  请求url
 * @param params  请求参数
 * @returns {Promise}
 */
export function get(url, params = {}, baseURL) {
    return new Promise((resolve, reject) => {
        axiosInstance.get(url, {
            params: params,
            baseURL
        }).then((response) => {
            landing(url, params, response);
            resolve(response);
        })
            .catch((error) => {
                reject(error);
            });
    });
}

/**
 * 封装post请求
 * @param url
 * @param data
 * @returns {Promise}
 */

export function post(url, data, baseURL) {
    return new Promise((resolve, reject) => {
        axiosInstance.post(url, data, { baseURL }).then(
            (response) => {
                //关闭进度条
                resolve(response);
            },
            (err) => {
                reject(err);
            }
        );
    });
}

/**
 * 封装patch请求
 * @param url
 * @param data
 * @returns {Promise}
 */
export function patch(url, data = {}) {
    return new Promise((resolve, reject) => {
        axiosInstance.patch(url, data).then(
            (response) => {
                resolve(response);
            },
            (err) => {
                msag(err);
                reject(err);
            }
        );
    });
}

/**
 * 封装put请求
 * @param url
 * @param data
 * @returns {Promise}
 */

export function put(url, data = {}) {
    return new Promise((resolve, reject) => {
        axiosInstance.put(url, data).then(
            (response) => {
                resolve(response);
            },
            (err) => {
                msag(err);
                reject(err);
            }
        );
    });
}

//统一接口处理，返回数据
export default function (fecth, url, params, baseURl = INIT_BASE_URL, isHasToken = true) {
     // isHasToken 是否携带token
    const baseURL = baseURl|| INIT_BASE_URL
    let param = {}
    if (isHasToken) {
        const loginObj = localStorage.getItem('loginObj') || '{}'
        const { assignee, token } = JSON.parse(loginObj)
        // const assignee = 'zdingx'
        // const assignee = 'bfeng1'
        // const token = '20wB1Cm1f1sV007' 
        param = { ...params, assignee, token }
    } else {
        param = { ...params }
    }
    return new Promise((resolve, reject) => {
        switch (fecth) {
            case "get":
                console.log("begin a get request,and url:", url);
                get(url, param, baseURL)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log("get request GET failed.", error);
                        reject(error);
                    });
                break;
            case "post":
                post(url, param, baseURL)
                    .then(function (response) {
                        resolve(response);
                    })
                    .catch(function (error) {
                        console.log("get request POST failed.", error);
                        reject(error);
                    });
                break;
            default:
                break;
        }
    });
}

//失败提示
function msag(err) {
    if (err && err.response) {
        switch (err.response.status) {
            case 400:
                alert(err.response.data.error.details);
                break;
            case 401:
                alert("未授权，请登录");
                break;

            case 403:
                alert("拒绝访问");
                break;

            case 404:
                alert("请求地址出错");
                break;

            case 408:
                alert("请求超时");
                break;

            case 500:
                alert("服务器内部错误");
                break;

            case 501:
                alert("服务未实现");
                break;

            case 502:
                alert("网关错误");
                break;

            case 503:
                alert("服务不可用");
                break;

            case 504:
                alert("网关超时");
                break;

            case 505:
                alert("HTTP版本不受支持");
                break;
            default:
        }
    }
}

/**
 * 查看返回的数据
 * @param url
 * @param params
 * @param data
 */
function landing(url, params, data) {
    if (data.code === -1) {
    }
}