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
							<uni-rate size="45" allow-half v-model="rateValue" active-color="#FCB857" :margin="15" />
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
					background: $brand-primary-soft;
					color: $brand-primary-ink;
					font-size: 22rpx;
					border-radius: $radius-pill;
					margin-bottom: 16rpx;
					font-weight: 500;
				}

				.timer {
					font-size: 24rpx;
					color: $text-secondary;
					display: flex;
					align-items: center;
				}
			}
		}

		.activity_btn {
			display: flex;
			gap: 16rpx;
			margin-bottom: 8rpx;

			.btn_item {
				flex: 1;
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

		.popup_container {
			background: $bg-card;
			border-radius: $radius-md $radius-md 0 0;
			padding-bottom: env(safe-area-inset-bottom);

			.popup_header {
				display: flex;
				align-items: center;
				justify-content: space-between;
				padding: 32rpx 32rpx 24rpx;
				border-bottom: 1rpx solid $border-light;

				.popup_title {
					font-size: 32rpx;
					font-weight: 600;
					color: $text-primary;
					line-height: 1.4;
				}

				.popup_close {
					width: 64rpx;
					height: 64rpx;
					display: flex;
					align-items: center;
					justify-content: center;
					font-size: 26rpx;
					color: $text-tertiary;
				}
			}

			.popup_content {
				padding: 32rpx;

				.rate_section {
					margin-bottom: 40rpx;

					.rate_label {
						font-size: 26rpx;
						color: $text-secondary;
						margin-bottom: 24rpx;

						.rate_value {
							font-size: 40rpx;
							font-weight: 600;
							color: $text-primary;
							margin: 0 8rpx;
						}

						.rate_max {
							font-size: 24rpx;
							color: $text-tertiary;
						}
					}

					.rate_stars {
						display: flex;
						justify-content: center;
					}
				}

				.comment_section {
					.comment_label {
						display: flex;
						justify-content: space-between;
						align-items: center;
						font-size: 26rpx;
						color: $text-primary;
						font-weight: 500;
						margin-bottom: 20rpx;

						.comment_count {
							font-size: 24rpx;
							color: $text-tertiary;
							font-weight: normal;
						}
					}

					.comment_input {
						width: 100%;
						min-height: 200rpx;
						padding: 24rpx;
						background: $bg-subtle;
						border-radius: $radius-sm;
						font-size: 28rpx;
						color: $text-primary;
						line-height: 1.5;
						box-sizing: border-box;

						&:focus {
							background: $bg-card;
							box-shadow: 0 0 0 4rpx rgba($brand-primary, 0.15);
						}
					}

					.comment_placeholder {
						color: $text-tertiary;
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
					border-radius: $radius-pill;
					font-size: 30rpx;
					font-weight: 600;
					color: $text-on-primary;
					background: $bg-hover;
					border: none;

					&[disabled] {
						opacity: 0.6;
						background: $bg-hover !important;
						box-shadow: none !important;
					}

					&_active:not([disabled]) {
						background: $brand-primary;

						&:active {
							background: $brand-primary-deep;
						}
					}
				}
			}
		}
	}
</style>