<template>
	<view class="com_search_container">
		<view class="search_input">
			<view class="search_box">
				<uni-icons type="search" size="20" color="#A39B90"></uni-icons>
				<input :value="value" @input="onInput" class="text" placeholder="搜索" placeholder-style="color:#A39B90" confirm-type="search"></input>
			</view>
			<uni-icons type="close" size="20" color="#A39B90" v-if="isShowCloseIcon" @click="onClearSearchText"></uni-icons>
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
			background: $bg-card;
			border: 2rpx solid $border-light;
			border-radius: $radius-pill;
			padding: 0 20rpx 0 28rpx;

			.search_box {
				display: flex;
				align-items: center;
				flex: 1;
				color: $text-tertiary;
				font-size: 28rpx;

				.text {
					margin-left: 16rpx;
					flex: 1;
					color: $text-primary;
				}
			}

			.btn {
				width: 112rpx;
				height: 56rpx;
				background: $brand-primary;
				color: $text-on-primary;
				font-size: 24rpx;
				font-weight: 500;
				border-radius: $radius-pill;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-left: 16rpx;

				&:active {
					background: $brand-primary-deep;
				}
			}
		}
	}
</style>