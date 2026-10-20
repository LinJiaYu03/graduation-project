<template>
	<view class="area"></view>
	<view class="custom-tabbar">
		<view class="tabbar-container">
			<view v-for="(item, index) in tabList" :key="index" class="tabbar-item"
				:class="{ 'active': currentPath === item.pagePath }" @click="switchTab(item)">
				<image :src="currentPath === item.pagePath ? item.selectedIconPath : item.iconPath" class="tabbar-icon"
					mode="aspectFit" />
				<text class="tabbar-text">{{ item.text }}</text>
			</view>
		</view>
		<!-- 安全区域占位 -->
		<view class="safety-area"></view>
	</view>
</template>

<script setup>
	import {
		ref,
		computed,
		onMounted
	} from 'vue'
	import {
		onShow
	} from '@dcloudio/uni-app'

	// 所有tab配置
	const allTabs = [{
			text: "主页",
			pagePath: "/pages/index/index",
			iconPath: "/static/image/iconfonts/主页.png",
			selectedIconPath: "/static/image/iconfonts/主页 (1).png"
		},
		{
			text: "活动",
			pagePath: "/pages/activity/activity",
			iconPath: "/static/image/iconfonts/活动.png",
			selectedIconPath: "/static/image/iconfonts/活动 (1).png"
		},
		{
			text: "扫码签到",
			pagePath: "/pages/scanCode/scanCode",
			iconPath: "/static/image/iconfonts/扫码.png",
			selectedIconPath: "/static/image/iconfonts/扫码 (1).png",
			requireAuth: true // 需要登录
		},
		{
			"text": "社团",
			"pagePath": "/pages/clubList/clubList",
			"iconPath": "/static/image/iconfonts/社团_s.png",
			"selectedIconPath": "/static/image/iconfonts/社团_s (1).png",
			requireAuth: true // 需要登录
		},
		{
			text: "个人",
			pagePath: "/pages/user/user",
			iconPath: "/static/image/iconfonts/个人.png",
			selectedIconPath: "/static/image/iconfonts/个人 (1).png"
		}
	]

	const currentPath = ref('')

	// 根据token状态过滤tab列表
	const tabList = computed(() => {
		return allTabs.filter(tab => {
			const token = uni.getStorageSync('token')
			// 如果tab需要登录但用户未登录，则隐藏
			if (tab.requireAuth && !token) {
				return false
			}
			return true
		})
	})

	// 更新当前路径
	function updateCurrentPath() {
		// 获取页面栈
		const pages = getCurrentPages()
		// 页面栈还没初始化或当前没有页面
		if (pages.length === 0) return
		// 获取栈顶页面（当前显示页面）
		const currentPage = pages[pages.length - 1]
		currentPath.value = '/' + currentPage.route
	}

	// 切换tab
	function switchTab(item) {
		// 如果点击的是当前页面，不执行跳转
		if (currentPath.value === item.pagePath) {
			return
		}

		uni.switchTab({
			url: item.pagePath
		})
	}

	onMounted(() => {
		updateCurrentPath()
	})

	// 使用onShow生命周期
	onShow(() => {
		updateCurrentPath()
	})
</script>

<style lang="scss" scoped>
	.custom-tabbar {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		background-color: #ffffff;
		border-top: 1px solid #e5e5e5;
		z-index: 999;
	}

	.tabbar-container {
		display: flex;
		align-items: center;
		justify-content: space-around;
		padding: 10rpx 0;
		height: 98rpx;
	}

	.tabbar-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		flex: 1;
		height: 100%;
		transition: all 0.3s;
	}

	.tabbar-icon {
		width: 44rpx;
		height: 44rpx;
		margin-bottom: 4rpx;
	}

	.tabbar-text {
		font-size: 24rpx;
		color: #bfbfbf;
		transition: color 0.3s;
	}

	.tabbar-item.active .tabbar-text {
		color: #007aff;
	}

	.safety-area {
		width: 100%;
		height: env(safe-area-inset-bottom);
		background-color: #ffffff;
	}
	
	.area {
		width: 100%;
		height: calc(env(safe-area-inset-bottom) + 100rpx);
		background-color: #ffffff;
	}
</style>