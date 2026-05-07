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
					<uni-icons type="closeempty" size="24" color="#666"></uni-icons>
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
					<uni-icons type="info" size="40" color="#ff3b30"></uni-icons>
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
		margin-bottom: 32rpx;
		padding: 32rpx;
		background: #ffffff;
		border-radius: 24rpx;
		box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.06);
		border: 1px solid transparent;
		transition: all 0.3s ease;

		.activity_info {
			display: flex;
			align-items: flex-start;
			margin-bottom: 40rpx;
			gap: 24rpx;

			.activity_info_left {
				flex-shrink: 0;
				width: 240rpx;
				height: 180rpx;
				border-radius: 16rpx;
				overflow: hidden;
				position: relative;

				&::after {
					content: '';
					position: absolute;
					top: 0;
					left: 0;
					right: 0;
					bottom: 0;
					background: linear-gradient(180deg,
							rgba(0, 0, 0, 0) 70%,
							rgba(0, 0, 0, 0.1) 100%);
					pointer-events: none;
				}

				image {
					width: 100%;
					height: 100%;
					object-fit: cover;
					transition: transform 0.5s ease;
				}
			}

			.activity_info_right {
				flex: 1;
				min-width: 0;

				.title {
					font-size: 32rpx;
					font-weight: 600;
					color: #1a1a1a;
					line-height: 1.4;
					margin-bottom: 16rpx;
					display: -webkit-box;
					-webkit-line-clamp: 2;
					-webkit-box-orient: vertical;
					overflow: hidden;
					text-overflow: ellipsis;
				}

				.type {
					display: inline-block;
					padding: 6rpx 16rpx;
					background: rgba($uni-topic-color, 0.1);
					color: $uni-topic-color;
					font-size: 22rpx;
					border-radius: 8rpx;
					margin-bottom: 20rpx;
					font-weight: 500;
				}

				.timer {
					font-size: 10px;
					color: #666;
					display: flex;
					align-items: center;
				}

				.status-tag {
					display: inline-flex;
					align-items: center;
					padding: 4rpx 16rpx;
					border-radius: 20rpx;
					font-size: 22rpx;
					font-weight: 500;
					margin-bottom: 20rpx;
					line-height: 1.4;

					&.online {
						background: rgba(76, 175, 80, 0.1);
						color: #4CAF50;
						border: 1rpx solid rgba(76, 175, 80, 0.3);
					}

					&.offline {
						background: rgba(244, 67, 54, 0.1);
						color: #F44336;
						border: 1rpx solid rgba(244, 67, 54, 0.3);
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
						background-color: #4CAF50;
					}

					&.offline::before {
						background-color: #F44336;
					}
				}
			}
		}

		.activity_btn {
			display: grid;
			grid-template-columns: repeat(3, 1fr);
			gap: 20rpx;
			margin-bottom: 8rpx;

			.btn_item {
				flex: 1;
				height: 68rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				border-radius: 16rpx;
				font-size: 26rpx;
				font-weight: 500;
				transition: all 0.3s ease;
				position: relative;
				overflow: hidden;
				border: 2rpx solid #e8e8e8;
				color: #666;
				background: #fafafa;
			}
		}

		.activity_tag {
			position: absolute;
			top: 32rpx;
			left: 32rpx;
			padding: 6rpx 20rpx;
			background: linear-gradient(135deg, #FF6B35, #FF8B5E);
			color: #fff;
			font-size: 22rpx;
			border-radius: 12rpx;
			line-height: 1;
			font-weight: 600;
			letter-spacing: 0.5rpx;
			z-index: 2;
			box-shadow: 0 4rpx 12rpx rgba(255, 107, 53, 0.25);

			&::before {
				content: '';
				position: absolute;
				top: -2rpx;
				left: -2rpx;
				right: -2rpx;
				bottom: -2rpx;
				background: linear-gradient(135deg,
						rgba(255, 107, 53, 0.4),
						rgba(255, 139, 94, 0.4));
				border-radius: 14rpx;
				z-index: -1;
			}
		}

		.delete-btn {
			position: absolute;
			top: 32rpx;
			right: 32rpx;
			width: 56rpx;
			height: 56rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			background: linear-gradient(135deg, #ff4d4f, #ff7875);
			border-radius: 50%;
			z-index: 2;
			box-shadow: 0 4rpx 12rpx rgba(255, 77, 79, 0.3);
			transition: all 0.3s ease;

			&:active {
				transform: scale(0.9);
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
				border-bottom: 1px solid #e0e0e0;
			}

			.rate {
				flex: 1;
				display: flex;
				align-items: center;
				justify-content: space-between;
			}

			.btn {
				border-top: 1px solid #e0e0e0;
				text-align: center;
				height: 90rpx;
				line-height: 90rpx;
			}
		}
	}

	// 二维码弹窗样式
	.qrcode-popup {
		width: 600rpx;
		background: #ffffff;
		border-radius: 24rpx;
		overflow: hidden;
		box-shadow: 0 16rpx 48rpx rgba(0, 0, 0, 0.2);

		.qrcode-header {
			display: flex;
			align-items: center;
			justify-content: space-between;
			padding: 32rpx;
			border-bottom: 1px solid #f0f0f0;

			.qrcode-title {
				font-size: 32rpx;
				font-weight: 600;
				color: #1a1a1a;
			}

			.qrcode-close {
				width: 48rpx;
				height: 48rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				border-radius: 50%;
				background: #f5f5f5;
				cursor: pointer;
				transition: all 0.3s ease;

				&:active {
					background: #e8e8e8;
					transform: scale(0.95);
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
				color: #666;
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
					border-radius: 16rpx;
					background: #fafafa;
					border: 2rpx solid #f0f0f0;
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
						color: #1a1a1a;
						text-align: center;
					}

					.activity-id {
						font-size: 24rpx;
						color: #999;
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
				color: #ff3b30;
				font-size: 28rpx;
			}
		}

		.qrcode-footer {
			padding: 24rpx 32rpx 32rpx;
			border-top: 1px solid #f0f0f0;

			.save-btn {
				width: 100%;
				height: 88rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				gap: 12rpx;
				background: linear-gradient(135deg, #FCB857 0%, #FF9800 100%);
				border-radius: 16rpx;
				color: #ffffff;
				font-size: 28rpx;
				font-weight: 500;
				box-shadow: 0 8rpx 24rpx rgba(252, 184, 87, 0.3);
				transition: all 0.3s ease;

				&:active {
					transform: scale(0.98);
					box-shadow: 0 4rpx 12rpx rgba(252, 184, 87, 0.3);
				}
			}
		}
	}
</style>