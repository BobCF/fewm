/**
* @file  index
* @date 2023-12-04
*/


import React, { useEffect, useState, useCallback, useRef, useMemo } from 'react';
import Nav from '../../../../../components/mobile/nav'
import { CameraComponent } from '../../../../../components/mobile/uploadImage'
import ListScroll from '../../../../../components/mobile/listScroll'
import { useRouteMatch, useHistory } from 'react-router-dom'
import { Toast, Button, ImageViewer, Popover } from 'antd-mobile'
import { CloseOutline, DownOutline } from 'antd-mobile-icons'
import { getCaseList, setStep, startStep, reStartStep, completeStep } from '../../service'
import './index.scss'

const page_size = 10

const TextStep = () => {
    const [list, setList] = useState([])
    const [pageNum, setPageNum] = useState(0)
    const [hasMore, setHasMore] = useState(false)
    const [running, setRunning] = useState(false)
    const [loading, setLoading] = useState(false)
    const [caseStatus, setCaseStatus] = useState('')
    const [swDisable, setSwDisable] = useState(false)
    const [descAcon, setDdescAcon] = useState({})
    const [imgList, setImgList] = useState([])
    const inputListRef = useRef([])
    const history = useHistory()
    const { params: { id, state: cycle_title, cycleid } } = useRouteMatch()

    const desc = useMemo(() => {
        return <div className='poptext' dangerouslySetInnerHTML={{ __html: descAcon.description ? descAcon.description.replace(/\n/g, '<br>') : '--' }}></div>
    }, [descAcon])
    const precon = useMemo(() => {
        return <div className='poptext' dangerouslySetInnerHTML={{ __html: descAcon.pre_condition ? descAcon.pre_condition.replace(/\n/g, '<br>') : '--' }}></div>
    }, [descAcon])

    const queryList = useCallback((page, id) => {
        setLoading(true)
        Toast.show({
            icon: 'loading',
            content: '加载中…',
            duration: 0,
            maskClickable: false
        })
        getCaseList(id, { cycle_id: cycleid, index: page, page_size }).then((res) => {
            if (res.status === 200) {
                setLoading(false)
                setHasMore(page < res.data.total - 1)
                setCaseStatus(res.data.status)
                setRunning(res.data.running)
                if (page === 0) {
                    setList(res.data.list || [])
                    setDdescAcon(res.data)
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
            })
    }, [list])

    const queryMore = useCallback(() => {
        if (loading) return
        queryList(pageNum + 1, id)
        setPageNum(pageNum + 1)
    }, [pageNum, loading])

    // 执行textStep
    const handleSet = useCallback((type, id = 0) => {
        Toast.show({
            icon: 'loading',
            content: '加载中…',
            duration: 0,
            maskClickable: false,
        })
        let obj = { result: type }
        if(id){
            obj.task_step_id = id
        }
        setStep(cycleid, obj, id).then((res) => {
            console.log(res, '=========')
            if (res.status === 200) {
                Toast.clear()
                refresh()
            } else {
                Toast.show({
                    icon: 'fail',
                    content: '网络异常',
                    duration: 3000,
                    maskClickable: false,
                })
            }
        }, (error) => {
            Toast.show({
                icon: 'fail',
                content: '网络异常',
                duration: 3000,
                maskClickable: false
            })
        }).catch((error) => {
            Toast.show({
                icon: 'fail',
                content: '网络异常',
                duration: 3000,
                maskClickable: false
            })
        })
    }, [])

    // 重新加载
    const refresh = useCallback(() => {
        setList([])
        setPageNum(0)
        queryList(0, id)
    }, [queryList])

    // 重新开始
    const handleRestart = useCallback(() => {
        Toast.show({
            icon: 'loading',
            content: '开始中…',
            duration: 0,
            maskClickable: false,
        })
        reStartStep(cycleid, {}, id).then((res) => {
            console.log(res, '=========')
            if (res.status === 200) {
                Toast.clear()
                refresh()
            } else {
                Toast.show({
                    icon: 'fail',
                    content: '网络异常',
                    duration: 3000,
                    maskClickable: false,
                })
            }
        }, (error) => {
            Toast.show({
                icon: 'fail',
                content: '网络异常',
                duration: 3000,
                maskClickable: false,
            })
        })
    }, [refresh])

    // 提交结果
    const handleComplete = useCallback(() => {
        Toast.show({
            icon: 'loading',
            content: '提交中…',
            duration: 0,
            maskClickable: false,
        })
        completeStep(cycleid, {}, id).then((res) => {
            console.log(res, '=========')
            if (res.status === 200) {
                Toast.clear()
                localStorage.setItem('caseact', 'Completed')
                history.go(-1)
            } else {
                Toast.show({
                    icon: 'fail',
                    content: '网络异常',
                    duration: 3000,
                    maskClickable: false,
                })
            }
        }, (error) => {
            Toast.show({
                icon: 'fail',
                content: '网络异常',
                duration: 3000,
                maskClickable: false,
            })
        })
    }, [])

    // 开始执行
    const handleOpen = useCallback(() => {
        // console.log(imgList, '======imgList========')

        // console.log(cycleid, 'cycleid', id, 'id')
        Toast.show({
            icon: 'loading',
            content: '开始中…',
            duration: 0,
            maskClickable: false,
        })
        startStep(cycleid, {}, id).then((res) => {
            console.log(res, '=========')
            if (res.status === 200) {
                Toast.clear()
                refresh()
                localStorage.setItem('caseact', 'WIP')
            } else {
                Toast.show({
                    icon: 'fail',
                    content: '网络异常',
                    duration: 3000,
                    maskClickable: false,
                })
            }
        }, (error) => {
            Toast.show({
                icon: 'fail',
                content: '网络异常',
                duration: 3000,
                maskClickable: false,
            })
        })
    }, [inputListRef, refresh])

    const delImage = useCallback((e, index) => {
        e.stopPropagation()
        const arr = imgList.filter((v, i) => i !== index)
        setImgList([...arr])
    }, [imgList])

    // 接收子组件返回的imgList
    const getImageList = useCallback((res) => {
        console.log([...imgList, res])
        setImgList([...imgList, res])
    }, [imgList])

    useEffect(() => {
        queryList(0, id)
    }, [])

    return <>
        <Nav showBack={true} showTime={false} title={'测试步骤'}></Nav>
        <ListScroll loadMore={queryMore} hasMore={hasMore}>
            <div className='tstep-body-nav'>
                <div className='tstep-body-nav-inner'>
                    <Button className='start' disabled={caseStatus !== 'ReadExecutionSteps'} color='primary' onClick={handleOpen}>开始执行</Button>
                    <div className='tstep-body-nav-pop'>
                        <Popover
                            content={desc}
                            placement='bottom'
                            trigger='click'
                        >
                            <Button style={{ marginRight: '10px' }} color='primary' fill='none'><DownOutline /> 描述</Button>
                        </Popover>
                        <Popover
                            content={precon}
                            placement='bottom'
                            trigger='click'
                        >
                            <Button color='primary' fill='none'><DownOutline /> 前提条件</Button>
                        </Popover>
                    </div>
                    <div className='tstep-body-nav-com'>
                        <Button disabled={caseStatus !== 'ConfirmResult'} style={{ marginRight: '10px' }} color='primary' fill='outline' onClick={handleRestart}>重新开始</Button>
                        <Button disabled={caseStatus !== 'ConfirmResult'} color='primary' fill='outline' onClick={handleComplete}>提交结果</Button>
                    </div>
                </div>
                {running && <div className='tstep-body-nav-com-tip'>执行中...</div>}
            </div>
            <div className='tstep-body-inner'>
                {list && list.map((item, index) => (
                    <div className='tstep-body-inner-item' key={item.id}>
                        <div className='top'>
                            <div className='id' dangerouslySetInnerHTML={{ __html: item.expected_results ? item.expected_results.replace(/\n/g, '<br>') : '--' }}></div>
                            <div className='title' dangerouslySetInnerHTML={{ __html: item.action ? item.action.replace(/\n/g, '<br>') : '--' }}></div>
                        </div>
                        <div className='bottom'>
                            {item.active && <div className='item'>
                                <div className='left'>备注:</div>
                                <CameraComponent imgListProp={imgList} getimgProps={getImageList} ref={(ref) => (inputListRef.current[index] = ref)}></CameraComponent>
                                <div className='left_list'>
                                    <div className='left_list_inner'>
                                        {imgList.map((items, indexs) => <div className="left_img" onClick={() => {
                                            ImageViewer.Multi.show({ images: imgList.map((res) => 'data:image/png;base64,' + res), defaultIndex: indexs })
                                        }}>
                                            <div className='del_img' onClick={(e) => delImage(e, indexs)}><CloseOutline /></div>
                                            <img src={'data:image/png;base64,' + items} alt="imgTag" />
                                        </div>)}

                                    </div>
                                </div>
                            </div>}
                            {!item.active && <div className='item'>
                                <div className='left'>备注:</div>
                                <div className='left_list'>
                                    <div className='left_list_inner'>
                                        {item.notes && item.notes.map((items, indexs) => <div className="left_img" onClick={() => {
                                            ImageViewer.Multi.show({ images: item.notes.map((res) => 'data:image/png;base64,' + res), defaultIndex: indexs })
                                        }}>
                                            <img src={'data:image/png;base64,' + items} alt="imgTag" />
                                        </div>)}

                                    </div>
                                </div>
                            </div>}
                            <div className='item space'>
                                <div className='item-inner'>
                                    <div className='left'>操作:</div>
                                    <div className='right'>
                                        <Button onClick={() => handleSet('ignore')} disabled={!item.active || running} color='primary'>跳过</Button>
                                        <Button onClick={() => handleSet('block')} disabled={!item.active || running} color='danger'>阻塞</Button>
                                        <Button onClick={() => handleSet('fail')} disabled={!item.active || running} color='warning'>失败</Button>
                                        <Button onClick={() => handleSet('pass')} disabled={!item.active || running} color='success'>成功</Button>
                                    </div>
                                </div>
                                <div className='status'><Button color='primary' fill='outline' onClick={() => handleSet('execution', item.id)} disabled={!item.active || running}>执行</Button></div>
                            </div>
                            <div className='item space'>
                                <div className='status'>状态: {item.stepstatus || '未执行'}</div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </ListScroll>
    </>
};

export default TextStep;
