import { DECREMENT, INCREMENT } from "../constants.js";

// const initState = 3; //初始化状态
const INITIAL_STATE = {
    name:'名字',
    num:1,
}

// 当第一次 preState 为 undefined 时，preState 赋值等于 initState
export default function increment(preState = INITIAL_STATE, action) {
  // 从 action 对象中获取：type,data
  const { type, data } = action;
  // 根据 type 决定加工数据
  switch (type) {
    case INCREMENT:
    return {
        ...preState,
        num: preState.num + data['num'],
        name: data['name'],
    }
    case DECREMENT:
      return {
        ...preState,
        num: preState.num - 1,
        name: '名字',
    }
    default:
      return preState; // 返回preState src/redux/reducers/index.ts allReducer 接收这个值
  }
};