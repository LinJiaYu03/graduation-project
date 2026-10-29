<template>
	<view class="club-review container">
		<view v-for="(item, index) in activityList" :key="item.id" class="activity-card" 
			:style="{ animationDelay: `${index * 0.05}s` }">
			
			<!-- 状态标签 -->
			<view class="activity-status ">
				{{ item.status }}
			</view>
			
			<!-- 活动信息 -->
			<view class="activity-info">
				<view class="activity-image">
					<image 
						:src="item.imageUrls[0] || '/static/images/default-activity.png'" 
						mode="aspectFill"
						@load="onImageLoad(index)"
						:class="{ loaded: imageLoaded[index] }"
					/>
					<view v-if="!item.imageUrls[0]" class="image-placeholder">
						<uni-icons type="image" size="40" color="#A39B90"></uni-icons>
					</view>
				</view>
				
				<view class="activity-content">
					<view class="activity-header">
						<text class="activity-title">{{ item.name }}</text>
						<view class="activity-type">{{ item.activityType }}</view>
					</view>
					
					<view class="activity-time">
						<uni-icons type="calendar" size="16" color="#A39B90"></uni-icons>
						<text class="time-text">
							{{ formatTime(item.startTime, 'YYYY.MM.DD hh:mm') }} - 
							{{ formatTime(item.endTime, 'hh:mm') }}
						</text>
					</view>
					
					<view v-if="item.location" class="activity-location">
						<uni-icons type="location" size="16" color="#A39B90"></uni-icons>
						<text class="location-text">{{ item.location }}</text>
					</view>
					
				</view>
			</view>
			
			<!-- 操作按钮 -->
			<view class="activity-actions">
				<button class="btn-detail" @click="handleViewDetail(item.id)">
					<uni-icons type="eye" size="18"></uni-icons>
					查看详情
				</button>
			</view>
			
			<!-- 分割线 -->
			<view v-if="index < activityList.length - 1" class="divider"></view>
		</view>
		
		<!-- 空状态 -->
		<view v-if="activityList.length === 0" class="empty-state">
			<image src="/static/images/empty-review.svg" class="empty-image" />
			<text class="empty-text">暂无待审核活动</text>
			<text class="empty-tip">所有活动审核已完成</text>
		</view>
	</view>
</template>

<script setup>
	import {
		ref
	} from 'vue';
	import { onShow } from '@dcloudio/uni-app'
	import {
		apiActivityReviewList
	} from '@/api/activity/index.js'
	import formatTime from '@/utils/dateUtil.js'

	const activityList = ref([])
	const imageLoaded = ref({})
	
	async function getActivityReviewList() {
		try {
			const res = await apiActivityReviewList()
			if (res.code === 200) {
				activityList.value = res.data.page.records
			}
		} catch (error) {
			console.error('获取活动列表失败:', error)
			uni.showToast({
				title: '加载失败',
				icon: 'error'
			})
		}
	}

	function handleViewDetail(activityId) {
		uni.navigateTo({
			url:`/pages/activity/activityDetail/activityDetail?id=${activityId}`
		})
	}

	function onImageLoad(index) {
		imageLoaded.value[index] = true
	}

	onShow(() => {
		getActivityReviewList()
	})
</script>

<style lang="scss" scoped>
	.club-review {
		padding: 24rpx;
		background: $bg-page;
		min-height: 100vh;
	}

	.activity-card {
		position: relative;
		background: $bg-card;
		border-radius: $radius-md;
		padding: 28rpx;
		margin-bottom: 24rpx;
		box-shadow: $shadow-card;
		border: 1rpx solid $border-base;
		overflow: hidden;
	}

	.activity-status {
		position: absolute;
		top: 24rpx;
		right: 24rpx;
		padding: 6rpx 20rpx;
		border-radius: $radius-pill;
		font-size: 22rpx;
		font-weight: 500;
		letter-spacing: 0.5rpx;
		z-index: 2;
		background: $brand-primary-soft;
		color: $brand-primary-ink;
	}

	.activity-info {
		display: flex;
		gap: 24rpx;
		margin-bottom: 24rpx;

		.activity-image {
			flex-shrink: 0;
			width: 240rpx;
			height: 180rpx;
			border-radius: $radius-sm;
			overflow: hidden;
			position: relative;
			background: $bg-subtle;

			image {
				width: 100%;
				height: 100%;
				object-fit: cover;
			}

			.image-placeholder {
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				height: 100%;
				display: flex;
				align-items: center;
				justify-content: center;
				background: $bg-subtle;
			}
		}

		.activity-content {
			flex: 1;
			min-width: 0;
			display: flex;
			flex-direction: column;
			gap: 12rpx;

			.activity-header {
				display: flex;
				align-items: flex-start;
				justify-content: space-between;
				gap: 16rpx;

				.activity-title {
					flex: 1;
					font-size: 30rpx;
					font-weight: 600;
					color: $text-primary;
					line-height: 1.4;
					display: -webkit-box;
					-webkit-line-clamp: 2;
					-webkit-box-orient: vertical;
					overflow: hidden;
					text-overflow: ellipsis;
				}

				.activity-type {
					flex-shrink: 0;
					padding: 6rpx 20rpx;
					background: $brand-primary-soft;
					color: $brand-primary-ink;
					font-size: 22rpx;
					border-radius: $radius-pill;
					font-weight: 500;
				}
			}

			.activity-time,
			.activity-location {
				display: flex;
				align-items: center;
				gap: 12rpx;
				font-size: 24rpx;
				color: $text-secondary;

				.time-text,
				.location-text {
					flex: 1;
					line-height: 1.4;
				}
			}

			.activity-footer {
				margin-top: auto;
				padding-top: 12rpx;
				border-top: 1rpx solid $border-light;

				.participant-count {
					display: flex;
					align-items: center;
					gap: 8rpx;
					font-size: 24rpx;
					color: $text-secondary;
				}
			}
		}
	}

	.activity-actions {
		display: flex;
		gap: 16rpx;
		padding-top: 24rpx;
		border-top: 1rpx solid $border-light;

		button {
			flex: 1;
			height: 76rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			gap: 12rpx;
			border-radius: $radius-pill;
			font-size: 26rpx;
			font-weight: 500;
			border: none;
			overflow: hidden;

			&::after {
				display: none;
			}

			&.btn-detail {
				background: $bg-card;
				color: $text-secondary;
				border: 2rpx solid $border-base;

				&:active {
					background: $bg-subtle;
				}
			}

			&.btn-review {
				background: $brand-primary;
				color: $text-on-primary;

				&:active {
					background: $brand-primary-deep;
				}
			}
		}
	}

	.divider {
		height: 1rpx;
		background: $border-light;
		margin: 32rpx -28rpx 0;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 120rpx 40rpx;
		text-align: center;

		.empty-image {
			width: 300rpx;
			height: 300rpx;
			opacity: 0.6;
			margin-bottom: 40rpx;
		}

		.empty-text {
			font-size: 30rpx;
			color: $text-secondary;
			font-weight: 600;
			margin-bottom: 16rpx;
		}

		.empty-tip {
			font-size: 26rpx;
			color: $text-tertiary;
		}
	}

	@keyframes slideInUp {
		from {
			opacity: 0;
			transform: translateY(40rpx);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}


	/* 响应式设计 */
	@media (max-width: 768px) {
		.club-review {
			padding: 24rpx;
		}

		.activity-card {
			padding: 32rpx;
		}

		.activity-info {
			flex-direction: column;
			gap: 24rpx;

			.activity-image {
				width: 100%;
				height: 300rpx;
			}
		}

		.activity-actions {
			flex-direction: column;

			button {
				width: 100%;
			}
		}
	}

</style>