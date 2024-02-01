/**
* @file  index
* @date 2023-12-01
*/


import React, { useEffect, useState, useCallback } from 'react';
import { useHistory } from 'react-router-dom'
import { NavBar } from 'antd-mobile'
import './index.scss'

const Nav = (props) => {
    const { showBack = true, title, showTime = false } = props
    const [time, setTime] = useState('')
    const history = useHistory()

    const getDate = useCallback(() => {
        let arr = new Array('星期天', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六')
        let now = new Date();
        let week = arr[now.getDay()];
        let year = now.getFullYear();
        let month = now.getMonth() + 1; 
        let day = now.getDate();
        setTime(year + '-' + month + '-' + day + ' ' + week)
    }, [])

    // 返回
    const goback = useCallback(() => {
        history.go(-1)
    }, [])

    useEffect(() => {
        getDate()
    }, [])

    return <div className='nav-top'>
        <NavBar onBack={goback} back={showBack ? '' : null}>
            <div className='nav-outer'>
                <div className='nav-big-title'>{title}</div>
                {showTime && <div className='nav-small-title'>{time}</div>}
            </div>
        </NavBar>
    </div>
};

export default Nav;
