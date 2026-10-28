<template>
	<view class="com-activity-item">
		<view class="activity_info">
			<view class="activity_info_left">
				<image :src="activeInfo.imageUrls[0]" mode="aspectFill"></image>
			</view>
			<view class="activity_info_right">
				<view class="title">{{ activeInfo.name }}</view>
				<view class="status-tag" :class="activeInfo.isPublished ? 'online' : 'offline'">
					{{ activeInfo.isPublished ? '上线状态' : '下线状态' }}
				</view>
				<br />
				<view class="type">{{ activeInfo.activityType }}</view>
				<view class="timer">{{ formatTime(activeInfo.startTime,'YYYY.MM.DD hh:mm') }} 至
					{{ formatTime(activeInfo.endTime,'YYYY.MM.DD hh:mm') }}
				</view>
			</view>
		</view>

		<view class="activity_btn">
			<view class="btn_item" @click="activityDetail">
				活动详情
			</view>
			<view class="btn_item" @click="memberReview">
				人员审核
			</view>
			<view class="btn_item" @click="()=>{
				uni.navigateTo({
					url:`/pages/user/myActivity/registrationStatistics/registrationStatistics?id=${props.activeInfo.id}`
				})
			}">
				活动统计
			</view>
			<view class="btn_item" @click="editActivity">
				活动编辑
			</view>
			<view class="btn_item" @click="showQrcode">
				签到码
			</view>
			<view class="btn_item" @click="onChangeActivityStatus(activeInfo.isPublished)">
				{{ activeInfo.isPublished?'活动下架':'活动上架' }}
			</view>
		</view>

		<view class="activity_tag">
			{{ activeInfo.status }}
		</view>

		<!-- 删除按钮 -->
		<view class="delete-btn" @click.stop="deleteActivity">
			<uni-icons type="trash" size="18" color="#fff"></uni-icons>
		</view>

	</view>

	<!-- 二维码弹窗 -->
	<uni-popup ref="qrcodePopup" type="center" background-color="rgba(0,0,0,0.5)">
		<view class="qrcode-popup">
			<view class="qrcode-header">
				<view class="qrcode-title">活动签到二维码</view>
				<view class="qrcode-close" @click="closeQrcode">
					<uni-icons type="closeempty" size="24" color="#A39B90"></uni-icons>
				</view>
			</view>
			<view class="qrcode-content">
				<view v-if="loading" class="qrcode-loading">
					<uni-icons type="spinner-cycle" size="40" color="#FCB857"></uni-icons>
					<text>加载中...</text>
				</view>
				<view v-else-if="qrcodeData" class="qrcode-wrapper">
					<image :src="qrcodeData.qrCode" mode="aspectFit" class="qrcode-image"></image>
					<view class="qrcode-info">
						<text class="activity-name">{{ qrcodeData.activityName }}</text>
						<text class="activity-id">活动ID: {{ qrcodeData.activityId }}</text>
					</view>
				</view>
				<view v-else class="qrcode-error">
					<uni-icons type="info" size="40" color="#E56B62"></uni-icons>
					<text>加载失败，请重试</text>
				</view>
			</view>
			<view class="qrcode-footer" v-if="qrcodeData">
				<view class="save-btn" @click="saveQrcode">
					<uni-icons type="download" size="18" color="#fff"></uni-icons>
					<text>保存到相册</text>
				</view>
			</view>
		</view>
	</uni-popup>
</template>

<script setup>
	import {
		ref
	} from 'vue'
	import {
		apiUpdateActivityStatus,
		apiDeleteActivity
	} from '@/api/activity/index.js'
	import formatTime from '@/utils/dateUtil.js'
	import request from '@/utils/request.js'

	const props = defineProps(['activeInfo'])
	const emits=defineEmits(['updataActivityList'])
	const userId = uni.getStorageSync('userInfo').id
	const rateActivityPopup = ref()
	const rateValue = ref(0)
	const qrcodePopup = ref(null)
	const qrcodeData = ref(null)
	const loading = ref(false)
	let qrcodeTimer = null

	function activityDetail() {
		uni.navigateTo({
			url: `/pages/activity/activityDetail/activityDetail?id=${props.activeInfo.id}`
		})
	}

	function memberReview() {
		uni.navigateTo({
			url: `/pages/user/memberReview/memberReview?id=${props.activeInfo.id}`
		})
	}

	function editActivity() {
		uni.navigateTo({
			url: `/pages/user/publishActivity/publishActivity?id=${props.activeInfo.id}`
		})
	}

	function onChangeActivityStatus(value) {
		uni.showModal({
			content: value ? '确认下架该活动？' : '确认上架该活动？',
			async success(e) {
				if (e.confirm) {
					let res = await apiUpdateActivityStatus(props.activeInfo.id, {
						managerUserId: userId,
						isPublished: !value
					})

					if (res.code == 200) {
						emits('updataActivityList')
						uni.showToast({
							title: res.message,
							icon: 'success'
						})
					}
				}
			}
		})
	}

	// 删除活动
	function deleteActivity() {
		uni.showModal({
			content: '确认删除该活动？删除后不可恢复！',
			async success(e) {
				if (e.confirm) {
					let res = await apiDeleteActivity(props.activeInfo.id, userId)
					if (res.code === 200) {
						uni.showToast({
							title: '删除成功',
							icon: 'success'
						})
						emits('updataActivityList')
					} else {
						uni.showToast({
							title: res.message || '删除失败',
							icon: 'none'
						})
					}
				}
			}
		})
	}


	// 显示二维码弹窗
	async function showQrcode() {
		qrcodePopup.value?.open()
		loading.value = true
		qrcodeData.value = null

		try {
			const res = await request({
				url: `/activities/${props.activeInfo.id}/qrcode`,
				method: 'GET'
			})

			if (res.code === 200 && res.data?.qrcode) {
				qrcodeData.value = res.data.qrcode
				startQrcodeTimer()
			} else {
				uni.showToast({
					title: res.message || '获取二维码失败',
					icon: 'none'
				})
			}
		} catch (error) {
			console.error('获取二维码失败:', error)
			uni.showToast({
				title: '获取二维码失败',
				icon: 'none'
			})
		} finally {
			loading.value = false
		}
	}

	// 启动二维码刷新定时器
	function startQrcodeTimer() {
		stopQrcodeTimer()
		qrcodeTimer = setTimeout(() => {
			refreshQrcode()
		}, 60000) // 1分钟后自动刷新
	}

	// 停止二维码刷新定时器
	function stopQrcodeTimer() {
		if (qrcodeTimer) {
			clearTimeout(qrcodeTimer)
			qrcodeTimer = null
		}
	}

	// 刷新二维码
	async function refreshQrcode() {
		stopQrcodeTimer()
		loading.value = true

		try {
			const res = await request({
				url: `/activities/${props.activeInfo.id}/qrcode`,
				method: 'GET'
			})

			if (res.code === 200 && res.data?.qrcode) {
				qrcodeData.value = res.data.qrcode
				startQrcodeTimer()
			} else {
				uni.showToast({
					title: res.message || '刷新二维码失败',
					icon: 'none'
				})
			}
		} catch (error) {
			console.error('刷新二维码失败:', error)
			uni.showToast({
				title: '刷新二维码失败',
				icon: 'none'
			})
		} finally {
			loading.value = false
		}
	}

	// 关闭二维码弹窗
	function closeQrcode() {
		stopQrcodeTimer()
		qrcodePopup.value?.close()
	}

	// 保存二维码到相册
	async function saveQrcode() {
		if (!qrcodeData.value?.qrCode) {
			uni.showToast({
				title: '二维码数据不存在',
				icon: 'none'
			})
			return
		}

		const base64 = qrcodeData.value.qrCode

		// #ifdef MP-WEIXIN
		uni.showLoading({
			title: '保存中...'
		})

		try {
			// 将base64转换为临时文件
			const filePath = await base64ToPath(base64)

			// 保存到相册
			await new Promise((resolve, reject) => {
				uni.saveImageToPhotosAlbum({
					filePath: filePath,
					success: () => {
						uni.hideLoading()
						uni.showToast({
							title: '保存成功',
							icon: 'success'
						})
						resolve()
					},
					fail: (err) => {
						uni.hideLoading()
						if (err.errMsg.includes('auth deny')) {
							uni.showModal({
								title: '需要相册权限',
								content: '请在设置中开启相册权限以保存图片',
								confirmText: '去设置',
								success: (res) => {
									if (res.confirm) {
										uni.openSetting()
									}
								}
							})
						} else {
							uni.showToast({
								title: '保存失败',
								icon: 'none'
							})
						}
						reject(err)
					}
				})
			})
		} catch (error) {
			console.error('保存二维码失败:', error)
			uni.hideLoading()
			uni.showToast({
				title: '保存失败',
				icon: 'none'
			})
		}
		// #endif

		// #ifdef H5
		// H5端直接下载图片
		try {
			const [, format] = /data:image\/(\w+);base64,(.*)/.exec(base64) || []
			const link = document.createElement('a')
			link.href = base64
			link.download = `qrcode_${qrcodeData.value.activityName || Date.now()}.${format || 'png'}`
			document.body.appendChild(link)
			link.click()
			document.body.removeChild(link)
			uni.showToast({
				title: '下载成功',
				icon: 'success'
			})
		} catch (error) {
			console.error('下载二维码失败:', error)
			uni.showToast({
				title: '下载失败',
				icon: 'none'
			})
		}
		// #endif
	}

	// 将base64转换为临时文件路径（仅微信小程序）
	// #ifdef MP-WEIXIN
	function base64ToPath(base64) {
		return new Promise((resolve, reject) => {
			const [, format, bodyData] = /data:image\/(\w+);base64,(.*)/.exec(base64) || []
			if (!format) {
				reject(new Error('ERROR_BASE64SRC_PARSE'))
				return
			}
			const filePath = `${wx.env.USER_DATA_PATH}/${Date.now()}.${format}`
			const fs = wx.getFileSystemManager()
			fs.writeFile({
				filePath: filePath,
				data: bodyData,
				encoding: 'base64',
				success: () => resolve(filePath),
				fail: reject
			})
		})
	}
	// #endif
</script>

<style lang="scss" scoped>
	.com-activity-item {
		position: relative;
		margin-bottom: 24rpx;
		padding: 24rpx;
		background: $bg-card;
		border-radius: $radius-md;
		box-shadow: $shadow-card;
		border: 1rpx solid $border-base;

		.activity_info {
			display: flex;
			align-items: flex-start;
			margin-bottom: 24rpx;
			gap: 24rpx;

			.activity_info_left {
				flex-shrink: 0;
				width: 240rpx;
				height: 180rpx;
				border-radius: $radius-sm;
				overflow: hidden;
				position: relative;

				image {
					width: 100%;
					height: 100%;
					object-fit: cover;
				}
			}

			.activity_info_right {
				flex: 1;
				min-width: 0;

				.title {
					font-size: 30rpx;
					font-weight: 600;
					color: $text-primary;
					line-height: 1.4;
					margin-bottom: 12rpx;
					display: -webkit-box;
					-webkit-line-clamp: 2;
					-webkit-box-orient: vertical;
					overflow: hidden;
					text-overflow: ellipsis;
				}

				.type {
					display: inline-block;
					padding: 6rpx 16rpx;
					background: $brand-primary-soft;
					color: $brand-primary-ink;
					font-size: 22rpx;
					border-radius: $radius-pill;
					margin-bottom: 12rpx;
					font-weight: 500;
				}

				.timer {
					font-size: 24rpx;
					color: $text-secondary;
					display: flex;
					align-items: center;
				}

				.status-tag {
					display: inline-flex;
					align-items: center;
					padding: 4rpx 16rpx;
					border-radius: $radius-pill;
					font-size: 22rpx;
					font-weight: 500;
					margin-bottom: 12rpx;
					line-height: 1.4;

					&.online {
						background: $color-success-soft;
						color: $color-success;
					}

					&.offline {
						background: $color-danger-soft;
						color: $color-danger;
					}

					&::before {
						content: '';
						display: inline-block;
						width: 8rpx;
						height: 8rpx;
						border-radius: 50%;
						margin-right: 8rpx;
					}

					&.online::before {
						background-color: $color-success;
					}

					&.offline::before {
						background-color: $color-danger;
					}
				}
			}
		}

		.activity_btn {
			display: grid;
			grid-template-columns: repeat(3, 1fr);
			gap: 16rpx;
			margin-bottom: 8rpx;

			.btn_item {
				height: 68rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				border-radius: $radius-pill;
				font-size: 26rpx;
				font-weight: 500;
				border: 2rpx solid $border-base;
				color: $text-secondary;
				background: $bg-card;

				&:active {
					background: $bg-subtle;
				}
			}
		}

		.activity_tag {
			position: absolute;
			top: 24rpx;
			left: 24rpx;
			padding: 6rpx 20rpx;
			background: rgba(255, 251, 244, 0.92);
			color: $brand-primary-ink;
			font-size: 22rpx;
			border-radius: $radius-pill;
			line-height: 1.4;
			font-weight: 600;
			letter-spacing: 0.5rpx;
			z-index: 2;
		}

		.delete-btn {
			position: absolute;
			top: 24rpx;
			right: 24rpx;
			width: 56rpx;
			height: 56rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			background: $color-danger;
			border-radius: 50%;
			z-index: 2;

			&:active {
				opacity: 0.85;
			}
		}

		.popup_container {
			display: flex;
			flex-direction: column;
			padding: 20rpx 20rpx 0 20rpx;
			width: 100vw;
			height: 600rpx;

			.title {
				height: 90rpx;
				display: flex;
				align-items: center;
				justify-content: space-between;
				border-bottom: 1rpx solid $border-light;
			}

			.rate {
				flex: 1;
				display: flex;
				align-items: center;
				justify-content: space-between;
			}

			.btn {
				border-top: 1rpx solid $border-light;
				text-align: center;
				height: 90rpx;
				line-height: 90rpx;
			}
		}
	}

	// 二维码弹窗样式
	.qrcode-popup {
		width: 600rpx;
		background: $bg-card;
		border-radius: $radius-md;
		overflow: hidden;
		box-shadow: 0 16rpx 48rpx rgba(122, 94, 45, 0.12);

		.qrcode-header {
			display: flex;
			align-items: center;
			justify-content: space-between;
			padding: 32rpx;
			border-bottom: 1rpx solid $border-light;

			.qrcode-title {
				font-size: 32rpx;
				font-weight: 600;
				color: $text-primary;
			}

			.qrcode-close {
				width: 48rpx;
				height: 48rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				border-radius: 50%;
				background: $bg-subtle;

				&:active {
					background: $bg-hover;
				}
			}
		}

		.qrcode-content {
			padding: 40rpx;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			min-height: 400rpx;

			.qrcode-loading {
				display: flex;
				flex-direction: column;
				align-items: center;
				justify-content: center;
				gap: 20rpx;
				color: $text-secondary;
				font-size: 28rpx;
			}

			.qrcode-wrapper {
				display: flex;
				flex-direction: column;
				align-items: center;
				gap: 24rpx;
				width: 100%;

				.qrcode-image {
					width: 400rpx;
					height: 400rpx;
					border-radius: $radius-sm;
					background: $bg-subtle;
					border: 2rpx solid $border-light;
				}

				.qrcode-info {
					display: flex;
					flex-direction: column;
					align-items: center;
					gap: 12rpx;
					width: 100%;

					.activity-name {
						font-size: 28rpx;
						font-weight: 600;
						color: $text-primary;
						text-align: center;
					}

					.activity-id {
						font-size: 24rpx;
						color: $text-tertiary;
						text-align: center;
					}
				}
			}

			.qrcode-error {
				display: flex;
				flex-direction: column;
				align-items: center;
				justify-content: center;
				gap: 20rpx;
				color: $color-danger;
				font-size: 28rpx;
			}
		}

		.qrcode-footer {
			padding: 24rpx 32rpx 32rpx;
			border-top: 1rpx solid $border-light;

			.save-btn {
				width: 100%;
				height: 88rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				gap: 12rpx;
				background: $brand-primary;
				border-radius: $radius-pill;
				color: $text-on-primary;
				font-size: 28rpx;
				font-weight: 500;

				&:active {
					background: $brand-primary-deep;
				}
			}
		}
	}
</style>