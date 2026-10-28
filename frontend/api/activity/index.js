import request from '@/utils/request.js'

// 创建活动
export const apiCreateActivity = (data) => request({
	url: '/activities/create',
	method: 'POST',
	data
})

// 获取活动列表
export const apiGetActivityList = (data) => request({
	url: '/activities/search',
	method: 'POST',
	data
})

// 活动详情
export const apiQueryActivity = (id) => request({
	url: `/activities/${id}`
})

// 报名活动
export const apiJoinActivity = (id, data) => request({
	url: `/activities/${id}/register`,
	method: 'POST',
	data
})

// 获取热门活动列表
export const apiGetHotActivity = () => request({
	url: '/activities/hot'
})

// 获取社团活动
export const apiGetClubActivity = (id) => request({
	url: `/activities/club/${id}`
})

//获取参与或管理的活动列表
export const apiGetJoinOrManangeActivity = (data) => request({
	url: `/activities/user/${data.id}?type=${data.type}&keyword=${data.keyword}`
})


// 获取活动报名详情
export const apiGetActiviyStatus = (data) => request({
	url: `/activities/${data.activityId}/registrations/check`
})

//评价活动
export const apiActivityRate = (data) => request({
	url: '/activities/comment',
	method: 'POST',
	data
})

// 获取人员审核列表
export const apiGetMemberReviewList = (data) => request({
	url: `/activities/${data.activityId}/registrations/status`
})

// 审核人员
export const apiMemberReview = (data) => request({
	url: '/activities/registrations/review',
	method: 'POST',
	data
})

// 审核活动列表
export const apiActivityReviewList = () => request({
	url: '/activities/pending'
})

// 活动审核
export const apiActivityReview = (data) => request({
	url: '/activities/review',
	method: 'POST',
	data
})

// 获取活动报名统计数据
export const apiGetActivityRegistrationStats = (activityId, type) => request({
	url: `/activities/${activityId}/statistics?type=${type}`
})

// 获取报名统计
export const apiGetRegistrationStatistics = (data) => request({
	url: `/activities/${data.activityId}/statistics`,
})

// 获取签到统计
export const apiGetCheckinStatistics = (data) => request({
	url: `/activities/${data.activityId}/checkin-statistics`,
})

// 获取评分统计
export const apiGetScoreStatistics = (data) => request({
	url: `/activities/${data.activityId}/score-statistics`,
})

// 扫码签到
export const apiCheckinActivity = (data) => request({
	url: '/activities/checkin',
	method: 'POST',
	data
})

// 更新活动
export const apiUpdateActivity = (data) => request({
	url: '/activities/update',
	method: 'PUT',
	data
})

// 活动上下架
export const apiUpdateActivityStatus = (id, data) => request({
	url: `/activities/${id}/publish-status`,
	method: 'PUT',
	data
})

// 删除活动
export const apiDeleteActivity = (activityId) => request({
	url: `/activities/${activityId}`,
	method: 'DELETE'
})

// 获取基地址
const getBaseUrl = () => {
	return 'http://localhost:8080/api/v1'
}

// 判断是否为小程序环境
const isMiniProgram = () => {
	return typeof uni.getFileSystemManager === 'function'
}

// 导出文件通用方法
const exportFile = (url, fileName) => {
	uni.showLoading({ title: '正在导出...' })

	uni.request({
		url,
		responseType: 'arraybuffer',
		header: {
			Authorization: `Bearer ${uni.getStorageSync('token')}`
		},
		success: (res) => {
			uni.hideLoading()

			const contentType = res.header && (res.header['content-type'] || res.header['Content-Type'])
			if (res.statusCode !== 200 || (contentType && contentType.includes('application/json'))) {
				uni.showToast({ title: '导出失败，请确认权限', icon: 'none' })
				return
			}

			if (isMiniProgram()) {
				const fs = uni.getFileSystemManager()
				const filePath = wx.env.USER_DATA_PATH + '/' + fileName
				fs.writeFile({
					filePath,
					data: res.data,
					encoding: 'binary',
					success: () => {
						uni.openDocument({
							filePath,
							fileType: 'xlsx',
							success: () => uni.showToast({ title: '导出成功', icon: 'success' }),
							fail: (err) => {
								console.error('打开文件失败', err)
								uni.showToast({ title: '文件已保存到: ' + filePath, icon: 'none' })
							}
						})
					},
					fail: (err) => {
						console.error('写入文件失败', err)
						uni.showToast({ title: '导出失败', icon: 'none' })
					}
				})
			} else {
				const blob = new Blob([res.data], {
					type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
				})
				const objectUrl = URL.createObjectURL(blob)
				const link = document.createElement('a')
				link.href = objectUrl
				link.download = fileName
				link.click()
				URL.revokeObjectURL(objectUrl)
				uni.showToast({ title: '导出成功', icon: 'success' })
			}
		},
		fail: (err) => {
			uni.hideLoading()
			console.error('请求失败', err)
			uni.showToast({ title: '导出失败', icon: 'none' })
		}
	})
}

// 导出报名情况表
export const apiExportRegistration = (activityId) => {
	const url = `${getBaseUrl()}/activities/${activityId}/export/registration`
	exportFile(url, '报名情况表.xlsx')
}

// 导出签到情况表
export const apiExportCheckin = (activityId) => {
	const url = `${getBaseUrl()}/activities/${activityId}/export/checkin`
	exportFile(url, '签到情况表.xlsx')
}

// 导出评分情况表
export const apiExportScore = (activityId) => {
	const url = `${getBaseUrl()}/activities/${activityId}/export/score`
	exportFile(url, '评分情况表.xlsx')
}