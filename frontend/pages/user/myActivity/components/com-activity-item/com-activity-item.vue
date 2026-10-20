<template>
	<view class="com-activity-item">
		<view class="activity_info">
			<view class="activity_info_left">
				<image :src="activeInfo.imageUrls[0]" mode="aspectFill"></image>
			</view>
			<view class="activity_info_right">
				<view class="title">{{ activeInfo.name }}</view>
				<view class="type">{{ activeInfo.activityType }}</view>
				<view class="timer">{{ formatTime(activeInfo.startTime,'YYYY.MM.DD hh:mm') }} 至
					{{ formatTime(activeInfo.endTime,'YYYY.MM.DD hh:mm') }}
				</view>
			</view>
		</view>

		<view class="activity_btn">
			<view class="btn_item" @click="onActivityDetail">
				活动详情
			</view>
			<view class="btn_item" @click="onParticipationDetail">
				参与详情
			</view>
			<view class="btn_item" @click="onOpenRate">
				评价活动
			</view>
		</view>

		<view class="activity_tag">
			{{ activeInfo.status }}
		</view>

		<uni-popup ref="rateActivityPopup" type="bottom" background-color="#fff">
			<view class="popup_container">
				<view class="popup_header">
					<view class="popup_title">
						评分和留言
					</view>
					<view class="popup_close" @click="onCloseRate">
						<view>取消</view>
					</view>
				</view>

				<view class="popup_content">
					<!-- 评分区域 -->
					<view class="rate_section">
						<view class="rate_label">
							你的评分：
							<text class="rate_value">{{ rateValue.toFixed(1) }}</text>
							<text class="rate_max">/5.0</text>
						</view>
						<view class="rate_stars">
							<uni-rate size="45" allow-half v-model="rateValue" active-color="#FF9500" :margin="15" />
						</view>
					</view>

					<!-- 留言区域 -->
					<view class="comment_section">
						<view class="comment_label">
							留言（选填）
						</view>
						<textarea class="comment_input" v-model="commentText" :maxlength="200"
							placeholder="分享你的活动体验和建议..." placeholder-class="comment_placeholder" auto-height />
					</view>
				</view>

				<view class="popup_footer">
					<button class="submit_btn" :class="{ 'submit_btn_active': rateValue > 0 }"
						:disabled="rateValue === 0" @click="onGitRate">
						提交评价
					</button>
				</view>
			</view>
		</uni-popup>
	</view>
</template>

<script setup>
	import {
		ref
	} from 'vue'
	import formatTime from '@/utils/dateUtil.js'
	import {
		apiActivityRate
	} from '@/api/activity/index.js'

	const props = defineProps(['activeInfo'])
	const userId = uni.getStorageSync('userInfo').id
	const rateActivityPopup = ref()
	const rateValue = ref(0)
	const commentText = ref('')

	function onActivityDetail() {
		uni.navigateTo({
			url: `/pages/activity/activityDetail/activityDetail?id=${props.activeInfo.id}`
		})
	}

	function onParticipationDetail() {
		uni.navigateTo({
			url: `/pages/user/myActivity/participationDetails/participationDetails?activeId=${props.activeInfo.id}`
		})
	}

	function onOpenRate() {
		rateActivityPopup.value.open()
	}

	function onCloseRate() {
		rateActivityPopup.value.close()
		rateValue.value = 0
	}

	async function onGitRate() {

		let res = await apiActivityRate({
			activityId: props.activeInfo.id,
			userId: userId,
			score: rateValue.value,
			comment:commentText.value
		})

		if (res.code == 200) {
			uni.showToast({
				icon: 'success',
				title: res.message
			})
		}
		onCloseRate()
	}
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
			}
		}

		.activity_btn {
			display: flex;
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

		.popup_container {
			background: #ffffff;
			border-radius: 32rpx 32rpx 0 0;
			padding-bottom: env(safe-area-inset-bottom);

			.popup_header {
				display: flex;
				align-items: center;
				justify-content: space-between;
				padding: 32rpx 32rpx 24rpx;
				border-bottom: 2rpx solid #f5f5f7;

				.popup_title {
					font-size: 34rpx;
					font-weight: 600;
					color: #1a1a1a;
					line-height: 1.4;
				}

				.popup_close {
					width: 64rpx;
					height: 64rpx;
					display: flex;
					align-items: center;
					justify-content: center;

					.icon-close {
						font-size: 28rpx;
						color: #8e8e93;
					}
				}
			}

			.popup_content {
				padding: 32rpx;

				.rate_section {
					margin-bottom: 48rpx;

					.rate_label {
						font-size: 28rpx;
						color: #8e8e93;
						margin-bottom: 32rpx;

						.rate_value {
							font-size: 44rpx;
							font-weight: 700;
							color: #1a1a1a;
							margin: 0 8rpx;
						}

						.rate_max {
							font-size: 24rpx;
							color: #c7c7cc;
						}
					}

					.rate_stars {
						display: flex;
						justify-content: center;

						::v-deep .uni-rate {
							.uni-rate__icon {
								transition: transform 0.2s ease;

								&:active {
									transform: scale(1.2);
								}
							}
						}
					}
				}

				.comment_section {
					.comment_label {
						display: flex;
						justify-content: space-between;
						align-items: center;
						font-size: 28rpx;
						color: #1a1a1a;
						font-weight: 500;
						margin-bottom: 20rpx;

						.comment_count {
							font-size: 24rpx;
							color: #c7c7cc;
							font-weight: normal;
						}
					}

					.comment_input {
						width: 100%;
						min-height: 200rpx;
						padding: 24rpx;
						background: #f8f8fa;
						border-radius: 20rpx;
						font-size: 28rpx;
						color: #1a1a1a;
						line-height: 1.5;
						box-sizing: border-box;
						transition: all 0.3s ease;

						&:focus {
							background: #fff;
							box-shadow: 0 0 0 4rpx rgba($uni-topic-color, 0.1);
						}
					}

					.comment_placeholder {
						color: #c7c7cc;
						font-size: 28rpx;
					}
				}
			}

			.popup_footer {
				padding: 0 32rpx 32rpx;

				.submit_btn {
					width: 100%;
					height: 88rpx;
					display: flex;
					align-items: center;
					justify-content: center;
					border-radius: 24rpx;
					font-size: 32rpx;
					font-weight: 600;
					color: #ffffff;
					background: linear-gradient(135deg, #c7c7cc, #d1d1d6);
					transition: all 0.3s ease;
					border: none;

					// 禁用状态
					&[disabled] {
						opacity: 0.5;
						background: linear-gradient(135deg, #c7c7cc, #d1d1d6) !important;
						box-shadow: none !important;
					}

					// 激活状态
					&_active:not([disabled]) {
						background: linear-gradient(135deg, $uni-topic-color, lighten($uni-topic-color, 10%));
						box-shadow: 0 8rpx 32rpx rgba($uni-topic-color, 0.25);

						&:active {
							transform: scale(0.98);
							box-shadow: 0 4rpx 16rpx rgba($uni-topic-color, 0.2);
						}
					}
				}
			}
		}
	}
</style>