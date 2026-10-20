const BASE_URL = 'http://localhost:8080/api'

export default function request(config = {}) {
	let {
		url,
		header = {},
		data = {},
		method
	} = config


	// header['access-key']='ljy123ljy'
	url = BASE_URL + url

	return new Promise((resolve, reject) => {
		uni.request({
			url,
			header,
			method,
			data,
			success(res) {
				if (res.statusCode === 200) {
					let {
						code,
						message
					} = res.data
					if (code === 200) {
						resolve(res.data)
					} else if (code === 400) {
						uni.showModal({
							title: "错误提示",
							content: message,
							showCancel: false
						})
						resolve(res.data)
					}
				} else {
					uni.showToast({
						title: res.errMsg,
						icon: "none"
					})
				}
			},
			fail(error) {
				reject(error)
			}
		})
	})
}