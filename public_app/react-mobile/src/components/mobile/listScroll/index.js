/**
* @file  index
* @date 2023-12-07
*/


import React, { useCallback, useState } from 'react'
import { Toast, InfiniteScroll } from 'antd-mobile'
import './index.scss'

const ListScroll = (props) => {
    const { children, loadMore, hasMore } = props

    return <>
        <div className='tcase-body'>
            {children}
            <InfiniteScroll loadMore={loadMore} hasMore={hasMore} />
        </div>
    </>
};

export default ListScroll;
