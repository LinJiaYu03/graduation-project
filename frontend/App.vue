<script >
	export default {
		onLaunch: function() {
			console.log('App Launch')
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
