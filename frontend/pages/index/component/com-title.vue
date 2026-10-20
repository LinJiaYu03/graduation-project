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
		margin-bottom: 25rpx;
		font-size: 40rpx;
		display: flex;
		align-items: center;
		justify-content: space-between;

		.left {
			display: flex;
			align-items: center;
			font-weight: 500;
			
			.box{
				margin-right: 10rpx;
				width: 10rpx;
				height: 40rpx;
				background-color: $uni-topic-color;
			}
		}
		
		.right{
			font-size: 35rpx;
		}
	}
</style>