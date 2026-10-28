<template>
	<view class="com-title_container">
		<view class="left">
			<view class="box"></view>
			<slot name="left"></slot>
		</view>
		<view class="right">
			<view>
				<slot name="right"></slot>
			</view>
		</view>
	</view>
</template>

<script setup>

</script>

<style lang="scss" scoped>
	.com-title_container {
		margin-bottom: 24rpx;
		font-size: 32rpx;
		display: flex;
		align-items: center;
		justify-content: space-between;

		.left {
			display: flex;
			align-items: center;
			font-weight: 600;
			color: $text-primary;

			.box{
				margin-right: 12rpx;
				width: 6rpx;
				height: 24rpx;
				border-radius: 3rpx;
				background-color: $brand-primary;
			}
		}
		
		.right{
			font-size: 24rpx;
			color: $text-secondary;
		}
	}
</style>