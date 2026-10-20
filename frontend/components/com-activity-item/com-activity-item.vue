<template>
	<view class="com-activity-item_cotainer" @click="onToActivitDetail">
		<view class="activity_tag">{{ activiyInfo.status }}</view>
		<view class="activity_image">
			<image :src="activiyInfo.imageUrls[0]" mode="aspectFill"></image>
		</view>
		<view class="activity_time">
			<text class="time_start">{{ formatTime(activiyInfo.startTime) }}</text>
			<text class="time_separator">至</text>
			<text class="time_end">{{ formatTime(activiyInfo.endTime) }}</text>
		</view>
		<view class="activity_title">{{ activiyInfo.name }}</view>
		<view class="activity_category">{{ activiyInfo.activityType }}</view>
	</view>
</template>

<script setup>
	import formatTime from '@/utils/dateUtil.js'
	const props=defineProps(['activiyInfo'])
	function onToActivitDetail(){
		uni.navigateTo({
			url:`/pages/activity/activityDetail/activityDetail?id=${props.activiyInfo.id}`
		})
	}
</script>

<style lang="scss" scoped>
	.com-activity-item_cotainer {
		margin-bottom: 20rpx;
		position: relative;
		width: 342rpx;
		background: #fff;
		border-radius: 16rpx;
		padding: 10rpx;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);

		.activity_tag {
			position: absolute;
			top: 24rpx;
			left: 24rpx;
			z-index: 2;
			padding: 8rpx 20rpx;
			background: #FF6B35;
			color: #fff;
			font-size: 20rpx;
			border-radius: 10rpx;
			line-height: 1;

			&--class {
				background: #4CAF50;
			}
		}

		.activity_image {
			width: 100%;
			height: 200rpx;
			border-radius: 12rpx;
			overflow: hidden;
			margin-bottom: 20rpx;
			background: #f0f0f0;

			image {
				width: 100%;
				height: 100%;
			}
		}

		.activity_time {
			display: flex;
			align-items: center;
			font-size: 22rpx;
			color: $uni-topic-color;
			margin-bottom: 16rpx;
			line-height: 1.5;
			flex-wrap: wrap;
			gap: 8rpx;

			.time_start,
			.time_end {
				font-weight: 500;
				letter-spacing: 0.5rpx;
			}

			.time_separator {
				color: rgba(255, 107, 53, 0.6);
				margin: 0 4rpx;
				font-weight: 400;
			}
		}

		.activity_title {
			font-size: 26rpx;
			font-weight: 500;
			color: #333;
			line-height: 1.4;
			margin-bottom: 16rpx;
			display: -webkit-box;
			-webkit-line-clamp: 2;
			-webkit-box-orient: vertical;
			overflow: hidden;
			height: 72rpx;
		}

		.activity_category {
			font-size: 22rpx;
			color: #999;
			padding-top: 8rpx;
			border-top: 1rpx solid #f0f0f0;
		}
	}
</style>