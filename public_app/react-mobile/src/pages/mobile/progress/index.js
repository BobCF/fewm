/**
* @file  index
* @date 2023-12-04
*/


import React, { useEffect, useState, useCallback } from 'react';
import Nav from '../../../components/mobile/nav'
import EchartsCon from './components/echartsCon'
import { useHistory } from 'react-router-dom'
import { Toast } from 'antd-mobile'
import { dateFormat } from '../../../utils/dataFormat'
import ListScroll from '../../../components/mobile/listScroll'
import { getList } from './service'
import './index.scss'

const Progress = () => {
    const [list, setList] = useState([])
    const [pageNum, setPageNum] = useState(0)
    const [hasMore, setHasMore] = useState(false)
    const [loading, setLoading] = useState(false)
    const history = useHistory()

    const queryList = useCallback((page) => {
        setLoading(true)
        Toast.show({
            icon: 'loading',
            content: '加载中…',
            duration: 0,
            maskClickable: false,
        })
        getList({index: page}).then((res) => {
            if (res.status === 200) {
                setLoading(false)
                setHasMore(page < res.data.total - 1)
                if (page === 0) {
                    setList(res.data.list || [])
                } else {
                    setList([...list, ...res.data.list] || [])
                }
                Toast.clear()
            } else {
                setLoading(false)
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
    }, [list])
    const queryMore = useCallback(() => {
        if (loading) return
        queryList(pageNum + 1)
        setPageNum(pageNum + 1)
    }, [pageNum, loading])

    useEffect(() => {
        queryList(0)
    }, [])
    return <>
        <Nav showBack={false} showTime={false} title={'执行进度'}></Nav>
        <ListScroll loadMore={queryMore} hasMore={hasMore}>
            <div className='pro-body-inner'>
                {list && list.map((item, index) => (
                    <div className='pro-body-inner-item' key={item.id}>
                        <div className='top'>
                            <div className='id'>{item.id}</div>
                            <div className='title'>{item.title}</div>
                        </div>
                        <div className='echarts-outer'>
                            <div className='echarts'>
                                <EchartsCon index={index} dataProps={item.executiondata || {}}></EchartsCon>
                            </div>
                            <div className='bottom'>
                                <div className='case-style'>
                                    {item.executionsize && [...Array(item.executionsize.complete)].map(() => <div className='case-style-item green'></div> )}
                                    {item.executionsize && [...Array(item.executionsize.running)].map(() => <div className='case-style-item yellow'></div> )}
                                    {item.executionsize && [...Array(item.executionsize.open)].map(() => <div className='case-style-item'></div> )}
                                </div>
                                <div className='item'>
                                    <div className='left'>执行团队:</div>
                                    <div className='right'>{item.team || '--'}</div>
                                </div>
                                {/* <div className='item'>
                                    <div className='left'>版本:</div>
                                    <div className='right'>{item.configuration || '--'}</div>
                                </div> */}
                                <div className='item'>
                                    <div className='left'>开始时间:</div>
                                    <div className='right'>{item.start_time ? dateFormat(item.start_time) : '--'}</div>
                                </div>
                                <div className='item'>
                                    <div className='left'>截至时间:</div>
                                    <div className='right'>{item.eta ? dateFormat(item.eta) : '--'}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </ListScroll>
    </>
};

export default Progress;
