import React, { useState, useEffect, useMemo } from 'react'
import { TabBar, Toast } from 'antd-mobile'
import { notification } from 'antd'
import mqtt from 'mqtt'
import {
    Route,
    Switch,
    useHistory,
    useLocation,
    MemoryRouter as Router
} from 'react-router-dom'
import {
    AppOutline,
    MessageOutline,
    UnorderedListOutline,
    UserOutline,
    HistogramOutline
} from 'antd-mobile-icons'
import Home from '../home'
import Todo from '../todo'
import Progress from '../progress'
import TextCase from '../todo/pages/textCase'
import TextStep from '../todo/pages/textStep'
import Message from '../message'
import PersonalCenter from '../personal'
import './index.scss'
import { useDispatch, useSelector } from 'react-redux'
import { changeData } from '../../../redux/actions/message'

const roleObj = {
    mobile: ['Executor', 'ExecutionLead', 'ValidationLead'],
    pc: ['ValidationLead']
}
const MObileDashBoard = () => {
    const [client, setClient] = useState(null);
    const [list, setList] = useState([])
    const history = useHistory()
    const location = useLocation()
    const [api, contextHolder] = notification.useNotification({
        maxCount: 5,
        stack: {
            threshold: 1
        }
    });
    const { pathname } = location
    const setRouteActive = (value) => {
        history.push(value)
    }
    const dispatch = useDispatch();
    const { message } = useSelector((state) => state)

    // 建立链接函数
    const mqttConnect = (host, mqttOption) => {
        // setConnectStatus('Connecting');
        setClient(mqtt.connect(host, mqttOption));
    };


    const tabs = useMemo(() => [
        {
            key: '/mobile/home',
            title: '首页',
            icon: <AppOutline />,
        },
        {
            key: '/mobile/todo',
            title: '任务',
            icon: <UnorderedListOutline />,
        },
        {
            key: '/mobile/message',
            title: '通知',
            icon: <MessageOutline />,
            badge: message.filter((item) => item.ishow && !item.isRead).length || null
        },
        {
            key: '/mobile/progress',
            title: '执行进度',
            icon: <HistogramOutline />,
        },
        {
            key: '/mobile/me',
            title: '我的',
            icon: <UserOutline />,
        },
    ], [message])

    useEffect(() => {
        if (!localStorage.getItem('loginObj')) return
        const loginObj = localStorage.getItem('loginObj') || '{}'
        const { assignee, token } = JSON.parse(loginObj)
        const brokerUrl = 'ws://121.40.124.59:15675/ws';
        const options = {
            clientId: assignee,// 设置 clientId
            clean: false, // 设置为 false 表示持久性订阅
            username: 'mqtt',
            password: 'mqtt@123'
        };
        mqttConnect(brokerUrl, options)


    }, [])

    // 监听消息并存储
    useEffect(() => {
        const loginObj = localStorage.getItem('loginObj') || '{}'
        const { assignee, token } = JSON.parse(loginObj)
        if (client) {
            client.on('connect', () => {
                // setConnectStatus('Connected');
                client.subscribe('topic/user/all', { qos: 2 });
                client.subscribe('topic/mobile/user/' + assignee, { qos: 2 }); // 执行topic
                client.subscribe('topic/user/' + assignee, { qos: 2 });
            });
            client.on('error', (err) => {
                console.error('Connection error: ', err);
                client.end();
            });
            client.on('reconnect', () => {
                // setConnectStatus('Reconnecting');
            });
            //   通信时调用
            client.on('message', (topic, con) => {
                console.log(con.toString(), '接收消息', topic, 'topic')
                if (['topic/user/all', 'topic/user/' + assignee].indexOf(topic) !== -1) {
                    let arr = message
                    let obj = JSON.parse(con.toString())
                    arr.unshift({ ...obj, ishow: true, isRead: false })
                    dispatch(changeData([...arr]))
                } else {
                    if(JSON.parse(con.toString()).url === '/notification/refresh'){
                        api.info({
                            message: `提示`,
                            description:
                                '任务已执行完成',
                            placement: 'top',
                            duration: 3
                        });
                    }
                }
            });
        }
    }, [client, message]);

    // 监听路由变化
    useEffect(() => {
        // 判断是否含有登录状态
        if (!localStorage.getItem('loginObj')) {
            // if (false) {
            Toast.show({
                icon: 'fail',
                content: '登录失效，即将跳转登录页',
                duration: 3000,
                maskClickable: false,
            })
            setTimeout(() => {
                history.replace('/login')
            }, 1000);
            return;
        }
        // 判断是否存在权限
        let isAuth = true
        if (roleObj[location.pathname.split('/')[1]].indexOf(JSON.parse(localStorage.getItem('loginObj') || '{}').role) === -1) {
            // 后期改成无权访问页面
            history.push('/pc/noauth')
        }
    }, [location, history])
    return (
        <div className='mo-da-app'>
            {contextHolder}
            <Switch>
                <Route exact path='/mobile/home'>
                    <Home />
                </Route>
                <Route exact path='/mobile/todo'>
                    <Todo />
                </Route>
                <Route exact path='/mobile/todo/textcase/:id/:state'>
                    <TextCase />
                </Route>
                <Route exact path='/mobile/todo/textstep/:id/:state/:cycleid'>
                    <TextStep />
                </Route>
                <Route exact path='/mobile/message'>
                    <Message />
                </Route>
                <Route exact path='/mobile/progress'>
                    <Progress />
                </Route>
                <Route exact path='/mobile/me'>
                    <PersonalCenter />
                </Route>
            </Switch>
            <div className='mo-da-bottom'>
                <div className='footer'>
                    <a href="https://beian.miit.gov.cn/">沪ICP备2024045151号</a>
                </div>
                <TabBar activeKey={pathname} onChange={value => setRouteActive(value)}>
                    {tabs.map(item => (
                        <TabBar.Item key={item.key} icon={item.icon} title={item.title} badge={item.badge} />
                    ))}
                </TabBar>
            </div>
        </div>
    )
}
export default MObileDashBoard