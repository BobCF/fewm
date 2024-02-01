import { CHANGEDATA } from "../constants.js";

// 定义方法

export const changeData = (data) => {
  return {
    type: CHANGEDATA,
    data,
  };
};