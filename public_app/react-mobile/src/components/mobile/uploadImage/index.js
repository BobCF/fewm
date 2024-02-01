/**
* @file  index
* @date 2023-12-05
*/


import React, { useState, useRef, useCallback, useImperativeHandle, forwardRef, useEffect } from 'react';
import { CameraOutline, LeftOutline } from 'antd-mobile-icons'
import { demoSrc, mockUpload } from './utils'
import { ImageUploader } from 'antd-mobile'
import './index.scss'

// 图片上传
const UploadImage = forwardRef((props, ref) => {
    const { id } = props
    const [fileList, setFileList] = useState([])
    const input = useRef()
    const handleUploadImage = useCallback(() => {
        const nativeInput = input.current?.nativeElement
        if (nativeInput) {
            nativeInput.click()
        }
    }, [input])

    const getImageList = useCallback(() => {
        return {
            id,
            fileList
        }
    }, [fileList])

    useImperativeHandle(ref, () => ({
        getImageList
    }))

    return <div className='up-image'>
        <div className='up-image-icon'>
            <CameraOutline className='icon' onClick={handleUploadImage} fontSize={45} color='#1677ff' />
        </div>
        <div className='up-image-list'>
            <ImageUploader
                ref={input} value={fileList} onChange={setFileList} upload={mockUpload}>
            </ImageUploader>
        </div>
    </div>
});

// 调取摄像头
const CameraComponent = forwardRef((props, ref) => {
    const { imgListProp, getimgProps } = props
    const [imgSrc, setImgSrc] = useState()
    const cameraVideoRef = useRef(null);
    const cameraCanvasRef = useRef(null);
    const [showImage, setShowImage] = useState(false)
    const [screenW, setScreenW] = useState(0)
    const [screenH, setScreenH] = useState(0)
    const [imglist, setImglist] = useState([])
    const [fileList, setFileList] = useState([])
    const handleUploadImage = useCallback(() => {
        setImgSrc('')
        setShowImage(true)
        openMedia()
    }, [])

    // 确认
    const checkImg = useCallback(() => {
        setImglist([...imgListProp, imgSrc])
        getimgProps(imgSrc)
        setShowImage(false)
    }, [imgSrc])

    const successFunc = useCallback((mediaStream) => {
        const video = cameraVideoRef.current;
        // const video = document.getElementById('cameraVideo') as HTMLVideoElement;
        // 旧的浏览器可能没有srcObject
        if ('srcObject' in video) {
            video.srcObject = mediaStream;
        }
        video.onloadedmetadata = () => {
            video.play();
        };
    }, [cameraVideoRef])

    const errorFunc = useCallback((err) => {
        console.log(`${err.name}: ${err.message}`);
        // always check for errors at the end.
    }, [])
    // 启动摄像头
    const openMedia = useCallback(() => { // 打开摄像头
        let w = document.documentElement.clientWidth || document.body.clientWidth
        let h = document.documentElement.clientHeight || document.body.clientHeight
        setScreenW(w)
        setScreenH(h)
        const opt = {
            audio: false,
            video: {
                width: w,
                height: h
            }
        };
        console.log(w, h, 'sasdad')
        navigator.mediaDevices.getUserMedia(opt).then(successFunc).catch(errorFunc);
    }, [])
    // 关闭摄像头
    const closeMedia = useCallback(() => {
        // const video = document.getElementById('cameraVideo') as HTMLVideoElement;
        const video = cameraVideoRef.current;
        const stream = video.srcObject;
        if ('getTracks' in stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => {
                track.stop();
            });
        }
    }, [cameraVideoRef])
    // 返回
    const goback = useCallback(() => {
        closeMedia()
        setShowImage(false)
    }, [])

    const getImg = useCallback(() => { // 获取图片资源
        // const video = document.getElementById('cameraVideo') as HTMLVideoElement;
        // const canvas = document.getElementById('cameraCanvas') as HTMLCanvasElement;
        const video = cameraVideoRef.current;
        const canvas = cameraCanvasRef.current;
        if (canvas == null) {
            return;
        }
        const ctx = canvas.getContext('2d');
        console.log(canvas.videoWidth, canvas.videoHeight,canvas,video,'==============')
        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight); // 把视频中的一帧在canvas画布里面绘制出来
        const imgStr = canvas.toDataURL(); // 将图片资源转成字符串
        const base64Img = imgStr.split(';base64,').pop(); // 将图片资源转成base64格式
        const imgData = {
            base64Img
        };
        closeMedia(); // 获取到图片之后可以自动关闭摄像头
        return imgData;
    }, [cameraVideoRef, cameraCanvasRef, screenW, screenH])


    const saveImg = useCallback(() => { // electron项目保存到本地
        const data = getImg();
        setImgSrc(data.base64Img)
        // 网页保存图片的方法
    }, [])

    return (
        <div className='up-image'>
            <div className='up-image-icon'>
                <CameraOutline className='icon' onClick={handleUploadImage} fontSize={45} color='#1677ff' />
            </div>

            {showImage && <div className='cameraModal'>
                <div className='cameraModal_back' onClick={goback}><LeftOutline /></div>
                <video
                    id="cameraVideo"
                    ref={cameraVideoRef}
                    // style={{
                    //     width: screenW, height: screenH
                    //   }}
                    width={screenW}
                    height={screenH}
                />
                <canvas
                    id="cameraCanvas"
                    ref={cameraCanvasRef}
                    // style={{
                    //     width: screenW, height: screenH
                    //   }}
                    width={screenW}
                    height={screenH}
                />
                {!imgSrc && <div className='cameraModal_pack' onClick={saveImg}>
                    <div className='cameraModal_pack_inner'></div>
                </div>}
                {imgSrc &&  <div className='cameraModal_pack' onClick={checkImg}>确认</div>}
                {imgSrc && <img id="imgTag" src={'data:image/png;base64,' + imgSrc} alt="imgTag" />}
                {imgSrc && <div className='img_recare' onClick={handleUploadImage}>重拍</div>}
                {/* <button onClick={openMedia} >打开摄像头</button>
                <button onClick={saveImg} >保存</button>
                <button onClick={closeMedia} >关闭摄像头</button> */}
            </div>}
        </div>
    )
})
export { UploadImage, CameraComponent };