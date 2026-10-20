import App from './App'

// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
	...App
})
app.$mount()
// #endif

// #ifdef VUE3
import {
	createSSRApp
} from 'vue'
export function createApp() {
	const app = createSSRApp(App)
	return {
		app
	}
}
// #endif

// 需要权限的api
const routeTypes = ['navigateTo', 'redirectTo', 'switchTab', 'reLaunch', 'navigateBack'];
// 不需要权限的页面
const routeNoControl=['/pages/index/index','/pages/system/login/login','/pages/system/registration/registration','/pages/system/userInfo/userInfo','/pages/activity/activity','/pages/user/user']

// 兼容带查询参数的路径匹配
const normalizePath = (url = '') => url.split('?')[0] || ''

// 为每个api添加拦截器
routeTypes.forEach(item => {
	uni.addInterceptor(item, {
		invoke(option) {
			const token = uni.getStorageSync('token')
			
			// 检查是否登录
			const targetPath = normalizePath(option.url)
			if (!token && !routeNoControl.includes(targetPath)) {
				uni.reLaunch({
					url: '/pages/system/login/login'
				})
				return false
			}
		}
	})
});
