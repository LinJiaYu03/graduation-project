<script >
	import { useUserStore } from '@/stores/user.js'
	import { setUnauthorizedHandler } from '@/utils/request.js'

	export default {
		onLaunch: function() {
			const userStore = useUserStore()
			setUnauthorizedHandler(() => userStore.clear())
			// 有令牌但没有本地缓存时，补拉一次用户信息
			if (uni.getStorageSync('token') && !userStore.user) {
				userStore.fetchMe().catch(() => {})
			}
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style lang="scss">
	page {
		background-color: $bg-page;
		color: $text-primary;
		font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', sans-serif;
	}

	view {
		box-sizing: border-box;
	}

	.safety_area {
		width: 100vw;
		height: env(safe-area-inset-bottom);
		background-color: $bg-card;
	}

	.container {
		padding: 24rpx;
		min-height: 100vh;
	}

	.activity_item_wrap {
		width: calc(50% - 10rpx);
	}
</style>
