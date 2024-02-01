import React, { Component } from 'react'
import {
    HashRouter,  // 构建 hash 路由, #/home #/login  === ( Vue mode:hash )
    // BrowserRouter,// 构建 history 路由  /home /login === ( Vue mode:history )
    Redirect, //重定向
    Route, //路由坑
    Switch //模糊匹配，箱单与Switch判断语句
} from 'react-router-dom'
//-------blog 自定义组件-------------------------
import Login from './pages/login'
import MObileDashBoard from './pages/mobile/dashboard'

export default class Router extends Component {
    render() {
        return (
            <HashRouter>
                <Switch> 
                    <Route path="/" exact component={Login} />
                    <Route path="/login" component={Login} />
                    <Route path="/mobile" render={() =>
                        // localStorage.getItem("token") ? <MObileDashBoard /> : <Redirect to="/login" />
                        <MObileDashBoard />
                    } />
                </Switch>
            </HashRouter>
        )
    }
}
