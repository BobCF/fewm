// 引入createStore，专门用于创建redux中最为核心的store对象
import { createStore, applyMiddleware } from "redux";
// 引入redux-thunk，用于支持异步action
import thunk from "redux-thunk";
// 引入 redux-devtools-extension
// import { composeWithDevTools } from "redux-devtools-extension";
// 引入汇总之后的reducer
import allReducer from "./reducers";

const store = createStore(
  allReducer,
//   composeWithDevTools(applyMiddleware(thunk))
);
export default store;