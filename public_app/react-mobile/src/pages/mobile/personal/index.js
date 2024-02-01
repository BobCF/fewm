/**
* @file  index
* @date 2023-11-01
*/


import React, { useState, useEffect, useCallback } from 'react';
import { useHistory } from 'react-router-dom'
import { Toast } from 'antd-mobile'
import { FillinOutline, DownFill } from 'antd-mobile-icons'
import { getData } from './service'
import Nav from '../../../components/mobile/nav'
import './index.scss'
const PersonalCenter = () => {

    const [perData, setPerData] = useState({})
    const history = useHistory()
    // 退出登录
    const loginout = useCallback(() => {
        localStorage.removeItem('loginObj')
        history.replace('/login')
    }, [])

    // 请求
    const queryData = useCallback(() => {
        Toast.show({
            icon: 'loading',
            content: '加载中…',
            duration: 0,
            maskClickable: false,
        })
        getData().then((res) => {
            if (res.data && res.data.code === 200) {
                const { works_time, monthworks_time, ...rest } = res.data.data
                let d = Number(works_time);
                let dm = Number(monthworks_time);
                let h = Math.floor(d / 3600);
                let m = Math.floor(d % 3600 / 60) +1;
                let mm = Math.floor(dm % 3600 / 60) +1;
                setPerData({h, m, mm, ...rest})
                Toast.clear()
            } else {
                Toast.show({
                    icon: 'fail',
                    content: '网络异常',
                    duration: 3000,
                    maskClickable: false,
                })
            }
        },
            (error) => {
                Toast.show({
                    icon: 'fail',
                    content: '网络异常',
                    duration: 3000,
                    maskClickable: false,
                })
            })
    }, [])

    useEffect(() => {
        queryData()
    }, [])

    return <>
        <Nav showBack={false} showTime={false} title='个人'></Nav>
        <div className='pe-body'>
            <div className='pe-body-inner'>
                <div className='pe-body-inner-top'>
                    <div className='pe-body-inner-top-item'>
                        <div className='left'>
                            <div className='cycle'>
                                <FillinOutline />
                            </div>
                            <span>工作时间</span>
                        </div>
                        <div className='right'>
                            <div className='sum'><span>{perData.h}</span>小时<span>{perData.m}</span>分钟</div>
                            <div>本月<span className='now'>{perData.mm}</span>分钟</div>
                        </div>
                    </div>
                    <div className='pe-body-inner-top-item'>
                        <div className='left'>
                            <div className='cycle' style={{ background: '#1677ff' }}>
                                <DownFill />
                            </div>
                            <span>勋章</span>
                        </div>
                        <div className='right'>
                            <div className='sum'>
                                <span>0</span>
                                枚勋章</div>
                        </div>
                    </div>
                </div>
                <div className='pe-body-inner-bottom'>
                    <div className='pe-body-inner-bottom-item'>
                        <div className='cycle' style={{ background: '#16ffa6' }}>
                        </div>
                        <div className='right'>
                            <div className='sum'><span className='title'>正在进行的任务组</span><span style={{ color: '#16ffa6' }}>{perData.runinggroup}</span></div>
                            <div>本月进行<span className='now'>{perData.monthruninggroup}</span></div>
                        </div>
                    </div>
                    <div className='pe-body-inner-bottom-item'>
                        <div className='cycle' style={{ background: '#168aff' }}>
                        </div>
                        <div className='right'>
                            <div className='sum'><span className='title'>已完成的任务组</span><span style={{ color: '#168aff' }}>{perData.completedgroup}</span></div>
                            <div>本月已完成<span className='now'>{perData.monthcompletedgroup}</span></div>
                        </div>
                    </div>
                    <div className='pe-body-inner-bottom-item'>
                        <div className='cycle' style={{ background: '#1645ff' }}>
                        </div>
                        <div className='right'>
                            <div className='sum'><span className='title'>正在进行的任务</span><span style={{ color: '#1645ff' }}>{perData.runingtask}</span></div>
                            <div>本月进行<span className='now'>{perData.monthruningtask}</span></div>
                        </div>
                    </div>
                    <div className='pe-body-inner-bottom-item'>
                        <div className='cycle' style={{ background: '#ad16ff' }}>
                        </div>
                        <div className='right'>
                            <div className='sum'><span className='title'>已完成的任务</span><span style={{ color: '#ad16ff' }}>{perData.completedtask}</span></div>
                            <div>本月已完成<span className='now'>{perData.monthcompletedtask}</span></div>
                        </div>
                    </div>
                </div>
                <div className='pe-body-inner-loginout' onClick={loginout}>
                    退出
                </div>
            </div>
        </div>
    </>
};

export default PersonalCenter;
