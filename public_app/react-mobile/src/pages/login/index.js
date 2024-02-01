/**
* @file  login
* @date 2023-10-31
*/


import React, { useCallback, useState } from 'react';
import { Button, Form, Input, Toast } from 'antd-mobile';
import { useHistory } from 'react-router-dom'
import { loginUser } from './service'
import { useDispatch, useSelector } from 'react-redux'
import { changeData } from '../../redux/actions/message'
import './index.scss'

const Login = () => {
    const history = useHistory()
    const [loading, setLoading] = useState(false)

    // mqtt赋值
    const dispatch = useDispatch();

    const onFinish = useCallback((values) => {
        const { username, password } = values
        setLoading(true)
        loginUser({ username, password }).then((res) => {
            if (res && res.data) {
                setLoading(false)
                if (res.data.code === 0) {
                    Toast.show({
                        icon: 'success',
                        content: '登陆成功！',
                    });
                    localStorage.setItem('loginObj', JSON.stringify({ assignee: username, token: password, role: res.data.role }))
                    const ini_data = JSON.parse(localStorage.getItem('messageList' + username)) || []
                    dispatch(changeData([...ini_data]))
                    setTimeout(() => {
                        // 权限判断
                        // if (res.data.role !== 'ValidationLead') {
                        //     history.replace('/mobile/home')
                        // } else {
                        //     history.replace('/pc/configurations')
                        // }
                        history.replace('/mobile/home')
                    }, 1000);
                } else if (res.data.code === 100) {
                    Toast.show({
                        icon: 'fail',
                        content: res.data.errmsg,
                    });
                }
            } else {
                setLoading(false)
                Toast.show({
                    icon: 'fail',
                    content: '网络错误',
                });
            }
        },
            (error) => {
                setLoading(false)
                Toast.show({
                    icon: 'fail',
                    content: '网络错误',
                });
            })
    }, [history])

    const onFinishFailed = useCallback((errorInfo) => {
        console.log('Failed:', errorInfo);
    }, [])

    return <div className="login">
        <div className="login_inner">
            <div className="login_inner_form">
                <h1>欢迎</h1>
                <Form
                    layout='horizontal'
                    name="basic"
                    onFinish={onFinish}
                    onFinishFailed={onFinishFailed}
                    footer={
                        <Button loading={loading} block type='submit' color='primary' >
                            登录
                        </Button>}
                >
                    <Form.Item
                        label="用户名"
                        name="username"
                        rules={[
                            {
                                required: true,
                                message: '请输入用户名！'
                            },
                        ]}
                    >
                        <Input placeholder='请输入用户名' />
                    </Form.Item>

                    <Form.Item
                        label="密码"
                        name="password"
                        rules={[
                            {
                                required: true,
                                message: '请输入密码！'
                            },
                        ]}
                    >
                        <Input type='password' placeholder='请输入密码' />
                    </Form.Item>
                </Form>
                <div className='login_footer'>
                    <a href="https://beian.miit.gov.cn/">沪ICP备2024045151号</a>
                </div>
            </div>
        </div>
    </div>
};

export default Login;
