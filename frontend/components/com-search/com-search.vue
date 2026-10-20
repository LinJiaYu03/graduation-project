<template>
	<view class="com_search_container">
		<view class="search_input">
			<view class="search_box">
				<uni-icons type="search" size="20" color="#999"></uni-icons>
				<input :value="value" @input="onInput" class="text" placeholder="搜索"></input>
			</view>
			<uni-icons type="close" size="20" v-if="isShowCloseIcon" @click="onClearSearchText"></uni-icons>
			<view class="btn" @click="onSearch">搜索</view>
		</view>
	</view>
</template>

<script setup>
	import {
		computed,
		ref,
	} from 'vue';

	const props = defineProps({
		value: {
			type: String,
			default: ''
		}
	})
	const emit = defineEmits(['update:value', 'click'])

	const isShowCloseIcon = computed(() => props.value != '')

	// 处理输入事件
	function onInput(e) {
		emit('update:value', e.detail.value)
	}

	function onSearch() {
		emit('click')
	}

	function onClearSearchText() {
		emit('update:value', '')
	}
</script>

<style lang="scss" scoped>
	.com_search_container {

		.search_input {
			display: flex;
			align-items: center;
			justify-content: space-between;
			height: 80rpx;
			background: #fff;
			border-radius: 16rpx;
			padding: 0 24rpx;
			box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);

			.search_box {
				display: flex;
				align-items: center;
				flex: 1;
				color: #999;
				font-size: 28rpx;

				.text {
					margin-left: 16rpx;
				}
			}

			.btn {
				width: 120rpx;
				height: 56rpx;
				background: $uni-topic-color;
				color: #fff;
				font-size: 26rpx;
				border-radius: 12rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-left: 20rpx;
			}
		}
	}
</style>