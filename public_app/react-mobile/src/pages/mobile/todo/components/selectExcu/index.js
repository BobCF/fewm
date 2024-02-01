/**
* @file  index
* @date 2023-12-06
*/


import React, { useState, useCallback, useMemo } from 'react';
import { SearchBar, Toast, Button, Checkbox } from 'antd-mobile'
import { assignmentStep } from '../../service'
// import { executor_ist } from '../../data'
import './index.scss'

const SelectExcu = (props) => {
    const { item, fresh, userlist } = props
    const [visible, setVisible] = useState(false)
    const [checkValue, setCheckValue] = useState([])
    const [searchValue, setSearchValue] = useState('')
    const [executorList, setExecutorList] = useState([])

    const executor_ist = useMemo(() => {
        let arr = []
        // console.log(userlist, 'user')
        userlist.map((item) => {
            arr.push({ label: item, value: item })
        })
        return arr
    }, [userlist])

    // 取消选择列表
    const handleClear = useCallback(() => {
        setVisible(false)
    }, [])

    // 确定
    const handleSub = useCallback((id, type) => {
        setVisible(false)
        console.log(checkValue)
        Toast.show({
            icon: 'loading',
            content: '分配中…',
            duration: 0,
            maskClickable: false,
        })
        assignmentStep(id, { team: type ? executorList : checkValue }).then((res) => {
            if (res.status === 200) {
                Toast.show({
                    icon: 'success',
                    content: '分配成功',
                })
                setVisible(false)
                setExecutorList(executor_ist)
                setSearchValue('')
                setCheckValue([])
                // ===========================刷新=========
                fresh()
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
    }, [checkValue, executorList, executor_ist])

    // 显示弹出框
    const handleshowToast = useCallback(() => {
        setExecutorList(executor_ist)
        // setSearchValue('')
        // setCheckValue([])
        setVisible(true)
    }, [executor_ist])

    const searchUser = useCallback((val) => {
        setSearchValue(val)
        let queryStringArr = val.split('');
        let str = '(.*?)';
        const arr = [];
        let regStr = str + queryStringArr.join(str) + str;
        let reg = RegExp(regStr, "i"); // 以mh为例生成的正则表达式为/(.*?)m(.*?)h(.*?)/i
        executor_ist.map(item => {
            if (reg.test(item.label)) {
                arr.push(item);
            }
        });
        setExecutorList([...arr])
    }, [executor_ist])

    return <div>
        <div className='set'>
            <Button className='select' color='primary' fill='solid' onClick={() => handleshowToast()}>Select Executor</Button>
            <Button disabled={!checkValue.length} color='primary' fill='outline' onClick={() => handleSub(item.id, false)}>随机分配</Button>
        </div>
        {/* 弹出列表 */}
        <div className={visible ? 'toastlist active' : 'toastlist'}>
            <div className='toastlist-inner'>
                <div className='con'>
                    <div className='act'>
                        <Button color='primary' fill='none' onClick={handleClear}>返回</Button>
                        <Button fill='none' style={{ fontWeight: 'bolder' }}>选择分配</Button>
                        <Button color='primary' fill='none' onClick={() => setVisible(false)}>确定</Button>
                    </div>
                    <div className='search'>
                        <SearchBar placeholder='请输入内容' value={searchValue} onChange={searchUser} showCancelButton={() => true} />
                    </div>
                </div>
                {executorList.length !== 0 && <div className='list-outer'>
                    <div className='list'>
                        <Checkbox.Group
                            value={checkValue}
                            onChange={v => {
                                console.log(v, 'v======')
                                setCheckValue(v)
                            }}
                        >
                            {executorList.map((item) => <div className='item'>
                                <Checkbox key={item} value={item.value}>{item.label}</Checkbox>
                            </div>)}
                        </Checkbox.Group>
                    </div>
                </div>}
            </div>
        </div>
    </div>
};

export default SelectExcu;
