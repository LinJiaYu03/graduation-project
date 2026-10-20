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
						<uni-icons type="image" size="40" color="#c0c4cc"></uni-icons>
					</view>
				</view>
				
				<view class="activity-content">
					<view class="activity-header">
						<text class="activity-title">{{ item.name }}</text>
						<view class="activity-type">{{ item.activityType }}</view>
					</view>
					
					<view class="activity-time">
						<uni-icons type="calendar" size="16" color="#999"></uni-icons>
						<text class="time-text">
							{{ formatTime(item.startTime, 'YYYY.MM.DD hh:mm') }} - 
							{{ formatTime(item.endTime, 'hh:mm') }}
						</text>
					</view>
					
					<view v-if="item.location" class="activity-location">
						<uni-icons type="location" size="16" color="#999"></uni-icons>
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
	const userId = uni.getStorageSync('userInfo').id
	
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
		padding: 32rpx;
		background: linear-gradient(180deg, #f5f7fa 0%, #f0f2f5 100%);
		min-height: 100vh;
	}

	.activity-card {
		position: relative;
		background: #ffffff;
		border-radius: 24rpx;
		padding: 40rpx;
		margin-bottom: 32rpx;
		box-shadow: 0 8rpx 40rpx rgba(0, 0, 0, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.2);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		overflow: hidden;
		animation: slideInUp 0.5s ease-out forwards;
		opacity: 0;

		&:hover {
			transform: translateY(-4rpx);
			box-shadow: 0 16rpx 48rpx rgba(0, 0, 0, 0.12);
		}

		&::before {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			height: 6rpx;
			background: linear-gradient(90deg, #3498db, #2ecc71);
			opacity: 0.8;
		}
	}

	.activity-status {
		position: absolute;
		top: 24rpx;
		right: 24rpx;
		padding: 6rpx 20rpx;
		border-radius: 20rpx;
		font-size: 22rpx;
		font-weight: 600;
		letter-spacing: 0.5rpx;
		z-index: 2;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
		background: linear-gradient(135deg, #ff9500, #ffaa33);
		color: #fff;
	}

	.activity-info {
		display: flex;
		gap: 32rpx;
		margin-bottom: 40rpx;

		.activity-image {
			flex-shrink: 0;
			width: 280rpx;
			height: 200rpx;
			border-radius: 20rpx;
			overflow: hidden;
			position: relative;
			background: linear-gradient(135deg, #f8f9fa, #e9ecef);
			box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);

			image {
				width: 100%;
				height: 100%;
				object-fit: cover;
				transition: transform 0.6s ease;
				opacity: 0;

				&.loaded {
					opacity: 1;
					animation: fadeIn 0.5s ease-out;
				}
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
				background: linear-gradient(135deg, #f8f9fa, #e9ecef);
			}
		}

		.activity-content {
			flex: 1;
			min-width: 0;
			display: flex;
			flex-direction: column;
			gap: 16rpx;

			.activity-header {
				display: flex;
				align-items: flex-start;
				justify-content: space-between;
				gap: 16rpx;

				.activity-title {
					flex: 1;
					font-size: 36rpx;
					font-weight: 700;
					color: #1a1a1a;
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
					background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(52, 152, 219, 0.2));
					color: #3498db;
					font-size: 24rpx;
					border-radius: 12rpx;
					font-weight: 600;
				}
			}

			.activity-time,
			.activity-location {
				display: flex;
				align-items: center;
				gap: 12rpx;
				font-size: 26rpx;
				color: #666;

				.time-text,
				.location-text {
					flex: 1;
					line-height: 1.4;
				}
			}

			.activity-footer {
				margin-top: auto;
				padding-top: 16rpx;
				border-top: 1px solid #eee;

				.participant-count {
					display: flex;
					align-items: center;
					gap: 8rpx;
					font-size: 26rpx;
					color: #666;
				}
			}
		}
	}

	.activity-actions {
		display: flex;
		gap: 24rpx;
		padding-top: 32rpx;
		border-top: 1px solid #f0f0f0;

		button {
			flex: 1;
			height: 80rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			gap: 12rpx;
			border-radius: 20rpx;
			font-size: 28rpx;
			font-weight: 600;
			transition: all 0.3s ease;
			border: none;
			position: relative;
			overflow: hidden;

			&::after {
				display: none;
			}

			&.btn-detail {
				background: linear-gradient(135deg, #f8f9fa, #e9ecef);
				color: #666;
				border: 2rpx solid #e0e0e0;

				&:active {
					background: linear-gradient(135deg, #e9ecef, #dee2e6);
					transform: scale(0.98);
				}
			}

			&.btn-review {
				background: linear-gradient(135deg, #3498db, #2980b9);
				color: #fff;
				box-shadow: 0 8rpx 24rpx rgba(52, 152, 219, 0.3);

				&:active {
					background: linear-gradient(135deg, #2980b9, #2573a7);
					transform: scale(0.98);
				}
			}
		}
	}

	.divider {
		height: 1px;
		background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
		margin: 40rpx -40rpx 0;
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
			font-size: 32rpx;
			color: #666;
			font-weight: 600;
			margin-bottom: 16rpx;
		}

		.empty-tip {
			font-size: 26rpx;
			color: #999;
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