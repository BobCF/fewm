/**
* @file  index
* @date 2023-11-01
*/


import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Nav from '../../../components/mobile/nav'
import { Badge, SwipeAction, Empty } from 'antd-mobile'
import { useDispatch, useSelector } from 'react-redux'
import { changeData } from '../../../redux/actions/message'
import { data } from './data'
import './index.scss'
const Message = () => {
    const [list, setList] = useState([])
    const dispatch = useDispatch();
    const { count, message } = useSelector((state) => state)
    // 右侧按钮操作
    const rightActions = useCallback((item, index) => {
        return [
            {
                key: 'unsubscribe',
                text: item.isRead ? '标为未读' : '标为已读',
                color: 'primary',
                onClick: () => {
                    const arr = list.map((items, indexs) => {
                        const { isRead, ...rest } = items
                        if (item.id === items.id) {
                            return {
                                isRead: !isRead,
                                ...rest
                            };
                        }
                        return items;
                    });
                    dispatch(changeData([...arr]))
                    setList([...arr])
                }
            },
            {
                key: 'mute',
                text: '不显示',
                color: 'warning',
                onClick: () => {
                    const arr = list.map((items, indexs) => {
                        const { ishow, ...rest } = items
                        if (item.id === items.id) {
                            return {
                                ishow: false,
                                ...rest
                            };
                        }
                        return items;
                    });
                    dispatch(changeData([...arr]))
                    setList([...arr])
                }
            },
            {
                key: 'delete',
                text: '删除',
                color: 'danger',
                onClick: () => {
                    // 先用不显示函数代替
                    const arr = list.filter((items) => items.id !== item.id)
                    dispatch(changeData([...arr]))
                    setList([...arr])
                }
            },
        ]
    }, [list])
    
    useEffect(() => {
        setList(message)
    }, [message])

    return <>
        <Nav showBack={false} showTime={false} title='消息'></Nav>
        <div className='me-body'>
            <div className='me-body-inner'>
                {list.filter((v) => v.ishow).length !== 0 && <div className='me-body-inner-list'>
                    {list.map((item, index) => item.ishow && <div key={index} className='me-body-inner-list-item'>
                        <Badge content={!item.isRead ? Badge.dot : ''}>
                            <SwipeAction
                                key={index}
                                rightActions={rightActions(item, index)}
                            >
                                <div className='me-body-list-title'>
                                    <div className='text'>{item.name}</div>
                                    <div>{item.time}</div>
                                </div>
                                <div className='me-body-list-con'>{item.message}</div>
                            </SwipeAction>
                        </Badge>
                    </div>)}
                </div>}
                {list.filter((v) => v.ishow).length === 0 && <Empty
                    style={{ padding: '64px 0' }}
                    imageStyle={{ width: 128 }}
                    description='暂无消息'
                />}
            </div>
        </div>
    </>
};

export default Message;
