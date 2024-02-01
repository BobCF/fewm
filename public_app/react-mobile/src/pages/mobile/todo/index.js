/**
* @file  index
* @date 2023-11-01
*/


import React, { useState, useEffect, useCallback } from 'react';
import { Toast, Tabs } from 'antd-mobile'
import { LoopOutline, CheckOutline, CloseOutline } from 'antd-mobile-icons'
import { getList, getUserList } from './service'
import SelectExcu from './components/selectExcu'
import Nav from '../../../components/mobile/nav'
import ListScroll from '../../../components/mobile/listScroll'
import { useHistory } from 'react-router-dom'
import { dateFormat } from '../../../utils/dataFormat'
import './index.scss'

const Todo = () => {
    const [list, setList] = useState([])
    const [userlist, setUserList] = useState([])
    const [actKey, setActKey] = useState('AssignmentCompleted')
    const [pageNum, setPageNum] = useState(0)
    const [hasMore, setHasMore] = useState(false)
    const [loading, setLoading] = useState(false)

    const history = useHistory()

    const queryList = useCallback((page, status) => {
        setLoading(true)
        Toast.show({
            icon: 'loading',
            content: '加载中…',
            duration: 0,
            maskClickable: false,
        })
        getList({ index: page, status }).then((res) => {
            if (res.status === 200) {
                setLoading(false)
                setHasMore(page < res.data.total - 1)
                setUserList(res.data.executor)
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
    }, [list])

    const handleTab = useCallback((e) => {
        setActKey(e)
        setList([])
        setPageNum(0)
        queryList(0, e)
    }, [])

    // 跳转到textCase
    const gotoCase = useCallback((item) => {
        if (actKey === 'open') return
        localStorage.removeItem('caseact')
        history.push('/mobile/todo/textcase/' + item.id + '/' + item.title)
    }, [actKey])

    const queryMore = useCallback(() => {
        if (loading) return
        queryList(pageNum + 1, actKey)
        setPageNum(pageNum + 1)
    }, [pageNum, loading, actKey])

    const refreshList = useCallback(() => {
        setList([])
        setPageNum(0)
        queryList(0, actKey)
    }, [queryList])

    useEffect(() => {
        queryList(0, actKey)
    }, [])

    return <>
        <Nav showBack={false} showTime={false} title='测试计划'></Nav>
        <ListScroll loadMore={queryMore} hasMore={hasMore}>
            <div className="to-body-tab">
                <Tabs activeKey={actKey} onChange={handleTab}>
                    <Tabs.Tab title='执行' key='AssignmentCompleted' />
                    <Tabs.Tab title='任务分配' key='open' />
                </Tabs>
            </div>
            {actKey === 'AssignmentCompleted' && <div className='to-body-inner change'>
                {list && list.map((item, index) => (
                    <div className='to-body-inner-item' key={item.id} onClick={() => gotoCase(item)}>
                        <div className='top'>
                            <div className='id'>
                                <span>{item.id || '--'}</span>
                                {/* <div className='icon green'> */}
                                {/* <div className='icon red'> */}
                                {/* <div className='icon'> */}
                                    {/* {<LoopOutline color='#fff' />} */}
                                    {/* {<CheckOutline color='#fff' />} */}
                                    {/* {<CloseOutline color='#fff' />} */}
                                {/* </div> */}
                            </div>
                            <div className='title'>{item.title || '--'}</div>
                        </div>
                        {/* <div className='bottom'>
                            <div className='item'>
                                <div className='left'>执行团队:</div>
                                <div className='right'>{item.team || '--'}</div>
                            </div>
                            <div className='item'>
                                <div className='left'>版本:</div>
                                <div className='right'>{item.configuration || '--'}</div>
                            </div>
                            <div className='item'>
                                <div className='left'>开始时间:</div>
                                <div className='right'>{dateFormat(item.start_time) || '--'}</div>
                            </div>
                            <div className='item'>
                                <div className='left'>截至时间:</div>
                                <div className='right'>{dateFormat(item.eta) || '--'}</div>
                            </div>
                        </div> */}
                    </div>
                ))}
            </div>}
            {actKey === 'open' && <div className='to-body-inner'>
                {list && list.map((item) => (
                    <div className='to-body-inner-item' key={item.id} onClick={() => gotoCase(item)}>
                        <div className='top'>
                            <div className='id'>{item.id || '--'}</div>
                            <div className='title'>{item.title || '--'}</div>
                        </div>
                        <div className='bottom'>
                            <div className='item'>
                                <div className='left'>执行团队:</div>
                                <div className='right'>{item.team || '--'}</div>
                            </div>
                            <div className='item'>
                                <div className='left'>版本:</div>
                                <div className='right'>{item.configuration || '--'}</div>
                            </div>
                            {/* <div className='item'>
                                <div className='left'>里程碑:</div>
                                <div className='right'>{item.plc_milestone || '--'}</div>
                            </div> */}
                            <div className='item'>
                                <div className='left'>开始时间:</div>
                                <div className='right'>{dateFormat(item.start_time) || '--'}</div>
                            </div>
                            <div className='item'>
                                <div className='left'>截至时间:</div>
                                <div className='right'>{dateFormat(item.eta) || '--'}</div>
                            </div>
                        </div>
                        {actKey === 'open' && <SelectExcu fresh={refreshList} userlist={userlist} item={item}></SelectExcu>}
                    </div>
                ))}
            </div>}
        </ListScroll>
    </>
};

export default Todo;
