 // 引入combineReducers，用于汇总所有的reducer
 import { combineReducers } from "redux";
 import count from './count'
 import message from './message'
 // 汇总所有的reducer，变为一个整的reducer
 const allReducer = combineReducers({
     count,
     message
 });
 export default allReducer;