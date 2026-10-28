<template>
	<view class="com-filter-btn">
		<view :class="{'filter_tag':true,'active':isActive}" @click="goFilter">
			{{ title?title:text }}
		</view>
		<uni-popup ref="popup" type="top" is-mask-click>
			<com-filter-tag-list :type="props.type" @close="closePopup"></com-filter-tag-list>
		</uni-popup>
	</view>
</template>

<script setup>
	import {
		ref,
		onMounted,
		onUnmounted
	} from 'vue'
	import comFilterTagList from '@/components/com-filter-tag-list/com-filter-tag-list.vue'

	const props = defineProps(['title', 'type', 'text'])
	const $emit = defineEmits(['update:title', 'update:type'])
	const initTitle = ref(props.title)
	const isActive = ref(false)
	const popup = ref(null)

	function goFilter() {
		popup.value.open()
	}

	function closePopup() {
		popup.value.close()
	}

	function onChangeTitle(e) {
		if (e.value === '全部') {
			isActive.value = false
			$emit('update:title', '')
		} else {
			isActive.value = true
			$emit('update:title', e.value)
		}
	}

	onMounted(() => uni.$on(`filterBack_${props.type}`, onChangeTitle))
	onUnmounted(() => uni.$off(`filterBack_${props.type}`, onChangeTitle))
</script>

<style lang="scss" scoped>
	.com-filter-btn {

		.filter_tag {
			margin-right: 16rpx;
			padding: 0 28rpx;
			height: 64rpx;
			text-align: center;
			line-height: 64rpx;
			background: $bg-card;
			border: 2rpx solid $border-base;
			border-radius: $radius-pill;
			font-size: 26rpx;
			color: $text-secondary;
		}

		.active {
			background: $brand-primary-soft;
			border-color: transparent;
			color: $brand-primary-ink;
			font-weight: 500;
		}
	}
</style>