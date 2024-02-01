import { CHANGEDATA } from "../constants.js";

// 当第一次 preState 为 undefined 时，preState 赋值等于 initState
export default function increment(preState, action) {
  const loginObj = localStorage.getItem('loginObj') || '{}'
  const { assignee, token } = JSON.parse(loginObj)
  const INITIAL_STATE = JSON.parse(localStorage.getItem('messageList' + assignee)) || []
  // 从 action 对象中获取：type,data
  const { type, data } = action;
  // 根据 type 决定加工数据
  switch (type) {
    case CHANGEDATA:
        localStorage.setItem('messageList' + assignee, JSON.stringify(data))
    return data
    default:
      return preState || INITIAL_STATE; // 返回preState src/redux/reducers/index.ts allReducer 接收这个值
  }
};