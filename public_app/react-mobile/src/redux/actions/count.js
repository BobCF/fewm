import { INCREMENT, DECREMENT } from "../constants.js";

// 定义方法

export const increment = (data) => {
  return {
    type: INCREMENT,
    data,
  };
};
// 减
export const decrement = (data) => {
  return {
    type: DECREMENT,
    data,
  };
};