/**
 * 日期格式话方法
 */ 
function dateFormat(date) {
    let dateObj = new Date(date)
    return dateObj.toLocaleDateString()
}

// 获取当前年月日时分秒
function getNowTime() {
    let date = new Date()
    return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds()
}
export {
    dateFormat,
    getNowTime
}