/**
* @file  index
* @date 2023-12-04
*/


import React, { useEffect, useState, useCallback } from 'react';
import Nav from '../../../../../components/mobile/nav'
import ListScroll from '../../../../../components/mobile/listScroll'
import { useRouteMatch, useHistory } from 'react-router-dom'
import { LoopOutline, CheckOutline, CloseOutline } from 'antd-mobile-icons'
import { Toast, Tabs } from 'antd-mobile'
import { getList } from '../../service'
import './index.scss'

const TextCase = () => {
    const [list, setList] = useState([])
    const [pageNum, setPageNum] = useState(0)
    const [hasMore, setHasMore] = useState(false)
    const [loading, setLoading] = useState(false)
    const [actKey, setActKey] = useState(localStorage.getItem('caseact') || 'WIP')
    const { params: { id, state } } = useRouteMatch()
    const history = useHistory()

    const queryList = useCallback((page, id, table) => {
        setLoading(true)
        Toast.show({
            icon: 'loading',
            content: '加载中…',
            duration: 0,
            maskClickable: false,
        })
        getList({ index: page, table }, id).then((res) => {
            if (res) {
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
    }, [list, actKey])
    const queryMore = useCallback(() => {
        if (loading) return
        queryList(pageNum + 1, id, actKey)
        setPageNum(pageNum + 1)
    }, [pageNum, loading, actKey])

    const handleTab = useCallback((e) => {
        setActKey(e)
        queryList(0, id, e)
        setPageNum(pageNum + 1)
    }, [])

    // 跳转step
    const gotoStep = useCallback((item) => {
        localStorage.setItem('caseact', actKey)
        history.push('/mobile/todo/textstep/' + item.id + '/' + state + '/' + id)
    }, [actKey])

    useEffect(() => {
        queryList(0, id, localStorage.getItem('caseact') || 'WIP')
    }, [])
    return <>
        <Nav showBack={true} showTime={false} title={state}></Nav>
        <ListScroll loadMore={queryMore} hasMore={hasMore}>
            <div className="tcase-body-tab">
                <div className='tcase-body-tab-bottom'>
                    <div className='tcase-body-tab-bottom-item'>
                        <div className='left'>执行团队:</div>
                        <div className='right'>item.team</div>
                    </div>
                    <div className='tcase-body-tab-bottom-item'>
                        <div className='left'>版本:</div>
                        <div className='right'>item.configuration</div>
                    </div>
                    <div className='tcase-body-tab-bottom-item'>
                        <div className='left'>开始时间:</div>
                        <div className='right'>dateFormat(item.start_time)</div>
                    </div>
                    <div className='tcase-body-tab-bottom-item'>
                        <div className='left'>截至时间:</div>
                        <div className='right'>dateFormat(item.eta)</div>
                    </div>
                </div>
                <Tabs activeKey={actKey} onChange={handleTab}>
                    <Tabs.Tab title='进行中' key='WIP' />
                    <Tabs.Tab title='未开始' key='NotRun' />
                    <Tabs.Tab title='已完成' key='Completed' />
                </Tabs>
            </div>
            <div className='tcase-body-inner'>
                {list && list.map((item) => (
                    <div className='tcase-body-inner-item' onClick={() => gotoStep(item)} key={item.id}>
                        <div className='top'>
                            <div className='id'>
                                <span>{item.id || '--'}</span>
                            {/* <div className='icon green'> */}
                                {/* <div className='icon red'> */}
                                {actKey === 'WIP' && item.running && <div className='icon'>
                                    {<LoopOutline color='#fff' className='icon-ant' />}
                                    {/* {<CheckOutline color='#fff' />} */}
                                    {/* {<CloseOutline color='#fff' />} */}
                                </div>}
                            </div>
                            <div className='title'>{item.title || '--'}</div>
                        </div>
                        <div className='bottom'>
                            <div className='item'>
                                <div className='left'>测试人员:</div>
                                <div className='right'>{item.owner || '--'}</div>
                            </div>
                            <div className='item'>
                                <div className='left'>当前状态:</div>
                                <div className='right'>{item.status || '--'}</div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </ListScroll>
    </>
};

export default TextCase;
