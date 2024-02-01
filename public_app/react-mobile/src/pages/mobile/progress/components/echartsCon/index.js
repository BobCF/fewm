/**
* @file  index
* @date 2023-12-06
*/


import React, { useCallback, useEffect, useMemo, useState } from 'react';
import * as echarts from 'echarts';
import './index.scss'

const EchartsCon = (props) => {
    const { index, dataProps } = props
    const options = useMemo(() => {
        let arr = dataProps.data
        let xRay = dataProps.date
        let otherX = []
        let num = Number(dataProps.data[0])
        let divic = (Number(dataProps.data[0]) / (dataProps.date.length - 1)).toFixed(2)
        xRay.map((item, index) => {
            if (index === dataProps.date.length - 1) {
                otherX.push(0)
            } else {
                otherX.push(num)
            }
            num = (Number(num - divic).toFixed(2))
        })
        return {
            xAxis: {
                type: 'category',
                data: xRay,
                boundaryGap: false,
                axisLabel: {
                    rotate: -60, // 设置标签倾斜角度，单位为度
                    fontSize: '8'
                }
            },
            yAxis: {
                axisLabel: {
                    fontSize: '9'
                },
                type: 'value'
            },
            grid: {
                left: '12%',
                right: '12%',
                bottom: '40%',
                top: '10%'
            },
            series: [
                {
                    data: arr,
                    type: 'line',
                    smooth: true
                },
                {
                    data: otherX,
                    type: 'line',
                    lineStyle: {
                        type: 'dashed'
                    },
                    smooth: true
                }
            ]
        }
    }, [])

    useEffect(() => {
        let chartDom = document.getElementsByClassName('main')[index]
        let myChart = echarts.init(chartDom)
        options && myChart.setOption(options)
        window.addEventListener('resize', () => {
            myChart.resize()
        })
    }, [])

    return <div className='echarts_inner'>
        <div className='main'></div>
    </div>
};

export default EchartsCon;
