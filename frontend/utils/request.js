const BASE_URL = 'http://localhost:8080/api/v1'

let refreshTask = null

function buildHeader(header = {}) {
	const token = uni.getStorageSync('token')
	if (token) {
		header.Authorization = `Bearer ${token}`
	}
	return header
}

function redirectToLogin() {
	uni.removeStorageSync('token')
	uni.removeStorageSync('refreshToken')
	uni.removeStorageSync('userInfo')
	uni.reLaunch({
		url: '/pages/system/login/login'
	})
}

// 多个请求同时 401 时只发起一次刷新
function refreshAccessToken() {
	if (refreshTask) {
		return refreshTask
	}

	const refreshToken = uni.getStorageSync('refreshToken')
	if (!refreshToken) {
		return Promise.reject(new Error('缺少刷新令牌'))
	}

	refreshTask = new Promise((resolve, reject) => {
		uni.request({
			url: BASE_URL + '/users/refresh',
			method: 'POST',
			data: {
				refreshToken
			},
			success(res) {
				const data = res.data && res.data.data
				if (res.statusCode === 200 && res.data && res.data.code === 200 && data) {
					uni.setStorageSync('token', data.accessToken)
					uni.setStorageSync('refreshToken', data.refreshToken)
					resolve(data.accessToken)
				} else {
					reject(new Error((res.data && res.data.message) || '登录状态已失效'))
				}
			},
			fail(error) {
				reject(error)
			}
		})
	})

	refreshTask.then(() => {
		refreshTask = null
	}).catch(() => {
		refreshTask = null
	})

	return refreshTask
}

// 响应式对象（reactive/ref）无法被小程序克隆，需转成普通对象
function normalizeData(data) {
	if (data && typeof data === 'object') {
		return JSON.parse(JSON.stringify(data))
	}
	return data
}

function send(config, isRetry) {
	let {
		url,
		header = {},
		data = {},
		method
	} = config

	return new Promise((resolve, reject) => {
		uni.request({
			url: BASE_URL + url,
			header: buildHeader(header),
			method,
			data: normalizeData(data),
			success(res) {
				if (res.statusCode === 200) {
					const {
						code,
						message
					} = res.data

					if (code === 200) {
						resolve(res.data)
					} else if (code === 400 || code === 403) {
						uni.showModal({
							title: '错误提示',
							content: message,
							showCancel: false
						})
						resolve(res.data)
					} else if (code === 401) {
						// accessToken 过期：用 refreshToken 换新后重试一次
						if (isRetry) {
							redirectToLogin()
							resolve(res.data)
							return
						}
						refreshAccessToken()
							.then(() => send(config, true))
							.then(resolve)
							.catch(() => {
								redirectToLogin()
								resolve(res.data)
							})
					} else {
						resolve(res.data)
					}
				} else {
					uni.showToast({
						title: res.errMsg,
						icon: 'none'
					})
					reject(res)
				}
			},
			fail(error) {
				reject(error)
			}
		})
	})
}

export default function request(config = {}) {
	return send(config, false)
}
