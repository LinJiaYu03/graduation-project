<template>
	<view class="com-activity-item_cotainer" @click="onToActivitDetail">
		<view class="activity_tag" :class="statusClass">{{ activiyInfo.status }}</view>
		<view class="activity_image">
			<image :src="activiyInfo.imageUrls[0]" mode="aspectFill"></image>
		</view>
		<view class="activity_time">
			<text class="time_start">{{ formatTime(activiyInfo.startTime, 'YYYY-MM-DD hh:mm') }}</text>
			<text class="time_separator">至</text>
			<text class="time_end">{{ formatTime(activiyInfo.endTime, 'YYYY-MM-DD hh:mm') }}</text>
		</view>
		<view class="activity_title">{{ activiyInfo.name }}</view>
		<view class="activity_category">{{ activiyInfo.activityType }}</view>
	</view>
</template>

<script setup>
	import { computed } from 'vue'
	import formatTime from '@/utils/dateUtil.js'
	const props=defineProps(['activiyInfo'])
	const statusClass = computed(() => {
		const status = props.activiyInfo.status || ''
		if (status.includes('进行')) return 'tag--ongoing'
		if (status.includes('结束') || status.includes('拒绝')) return 'tag--ended'
		if (status.includes('审核') || status.includes('通过')) return 'tag--review'
		return 'tag--pending'
	})
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
		width: 100%;
		background: $bg-card;
		border: 1rpx solid $border-base;
		border-radius: $radius-md;
		padding: 12rpx;
		box-shadow: $shadow-card;
		overflow: hidden;

		.activity_tag {
			position: absolute;
			top: 20rpx;
			left: 20rpx;
			z-index: 2;
			padding: 6rpx 16rpx;
			background: $brand-primary-soft;
			color: $brand-primary-ink;
			font-size: 20rpx;
			font-weight: 500;
			border-radius: $radius-pill;
			line-height: 1.4;

			&.tag--ongoing {
				background: $color-success-soft;
				color: $color-success;
			}

			&.tag--ended {
				background: $bg-subtle;
				color: $text-tertiary;
			}

			&.tag--review {
				background: $color-info-soft;
				color: $color-info;
			}
		}

		.activity_image {
			width: 100%;
			height: 200rpx;
			border-radius: $radius-sm;
			overflow: hidden;
			margin-bottom: 16rpx;
			background: $bg-subtle;

			image {
				width: 100%;
				height: 100%;
			}
		}

		.activity_time {
			display: flex;
			flex-direction: column;
			align-items: flex-start;
			font-size: 22rpx;
			color: $brand-primary-ink;
			margin-bottom: 12rpx;
			line-height: 1.5;
			gap: 2rpx;

			.time_start,
			.time_end {
				font-weight: 500;
				letter-spacing: 0.5rpx;
				white-space: nowrap;
			}

			.time_separator {
				color: rgba($brand-primary-ink, 0.55);
				margin: 0;
				font-weight: 400;
			}
		}

		.activity_title {
			font-size: 26rpx;
			font-weight: 500;
			color: $text-primary;
			line-height: 1.4;
			margin-bottom: 12rpx;
			display: -webkit-box;
			-webkit-line-clamp: 2;
			-webkit-box-orient: vertical;
			overflow: hidden;
			height: 72rpx;
		}

		.activity_category {
			font-size: 22rpx;
			color: $text-tertiary;
			padding-top: 12rpx;
			border-top: 1rpx solid $border-light;
		}
	}
</style>