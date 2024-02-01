/**
* @file  index
* @date 2023-11-01
*/


import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Nav from '../../../components/mobile/nav';
import ListScroll from '../../../components/mobile/listScroll'
import { DownOutline } from 'antd-mobile-icons'
import { getList } from './service'
import { Popover, Toast } from 'antd-mobile'
import './index.scss'
const Home = () => {
    const [list, setList] = useState([])
    const [hoData, setHoData] = useState({})
    const [pageNum, setPageNum] = useState(0)
    const [hasMore, setHasMore] = useState(false)
    const [loading, setLoading] = useState(false)
    const popData = useMemo(() => <div className='popData'>
        {hoData.owner_group && hoData.owner_group.map((item, index) =>
            <div className='item' key={index}>{item}</div>
        )
        }
    </div >, [hoData])

    // 请求数据
    const queryList = useCallback((page) => {
        setLoading(true)
        Toast.show({
            icon: 'loading',
            content: '加载中…',
            duration: 0,
            maskClickable: false,
        })
        getList({ index: page }).then((res) => {
            if (res.status === 200) {
                setLoading(false)
                setHasMore(page < res.data.total - 1)
                if (page === 0) {
                    setList(res.data.data.result || [])
                    setHoData(res.data.data)
                } else {
                    setList([...list, ...res.data.list] || [])
                }
                Toast.clear()
            } else {
                setLoading(false)
                setHasMore(false)
                Toast.show({
                    icon: 'fail',
                    content: '网络异常',
                    duration: 3000,
                    maskClickable: false,
                })
            }
        },
            (error) => {
                setLoading(false)
                setHasMore(false)
                Toast.show({
                    icon: 'fail',
                    content: '网络异常',
                    duration: 3000,
                    maskClickable: false,
                })
            }).catch((error) => {
                setLoading(false)
                setHasMore(false)
                Toast.show({
                    icon: 'fail',
                    content: '网络异常',
                    duration: 3000,
                    maskClickable: false
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
        <Nav showBack={false} showTime={false} title='主页'></Nav>
        <ListScroll loadMore={queryMore} hasMore={hasMore}>
            <div className='ho-body-inner'>
                <div className='ho-body-inner-top'>
                    <div className='ho-body-inner-top-item'>
                        <div className='ho-body-inner-top-item-top'>昨日累计完成</div>
                        <div className='num'>{hoData.yestdayComplete}</div>
                    </div>
                    {/* <Popover
                        content={popData}
                        trigger='click'
                        placement='bottom'
                    >
                        <div className='ho-body-inner-top-item pop'>
                            <div className='ho-body-inner-top-item-top'>所在项目</div>
                            <div className='num'>{hoData.owner_group && hoData.owner_group.join(' | ')}</div>
                            <div className="icon"><DownOutline /></div>

                        </div>
                    </Popover> */}
                    <div className='ho-body-inner-top-item'>
                        <div className='ho-body-inner-top-item-top'>本月累计完成</div>
                        <div className='num'>{hoData.monthComplete}</div>
                    </div>
                </div>
                <div className='ho-body-inner-bottom'>
                    <div className='ho-body-inner-bottom-inner'>
                        {list && list.map((item, index) => <div key={index} className='ho-body-inner-bottom-inner-item'>
                            <div className='top'>
                                <div className='id'>{item.title}</div>
                                <div className='title'>{item.id}</div>
                            </div>
                            <div className='bottom'>
                                <div className='item'>
                                    <div className='left'>今日新增:</div>
                                    <div className='right' style={{ color: '#ffc116' }}>{item.todayNewAssignment}</div>
                                </div>
                                <div className='item'>
                                    <div className='left'>分配给我的:</div>
                                    <div className='right'>{item.assigneedto_me}</div>
                                </div>
                                <div className='item'>
                                    <div className='left'>已完成:</div>
                                    <div className='right' style={{ color: '#16ff25' }}>{item.completed}</div>
                                </div>
                                <div className='item'>
                                    <div className='left'>未分配:</div>
                                    <div className='right' style={{ color: 'red' }}>{item.unassignee}<div>
                                    </div>
                                    </div>
                                </div>
                            </div>
                        </div>)}
                    </div>
                </div>
            </div>
        </ListScroll>
    </>
};

export default Home;
