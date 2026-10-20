<template>
	<view class="com-filter-list">
		<uni-list :border="false">
			<uni-list-item v-for="item in filterList" :key="item" clickable :title="item"
				@click="onGoTo(item)"></uni-list-item>
		</uni-list>

	</view>
</template>

<script setup>
	import {
		computed
	} from 'vue'

	const props = defineProps({
		type: {
			type: String,
			required: true
		}
	})

	const filterListData = {
		status: ['全部', '审核中', '等待中', '报名中', '进行中', '已结束'],
		category: ['全部', '思想成长', '实践实习', '公益志愿', '创业创新', '文化艺体','电影鉴赏'],
		level: ['全部', '校级', '院级', '班级']
	}

	const filterList = computed(() => filterListData[props.type])

	const emit = defineEmits(['close'])

	function onGoTo(value) {
		uni.$emit(`filterBack_${props.type}`, {
			value
		})
		emit('close')
	}
</script>

<style lang="scss" scoped>
	.com-filter-list {
		background-color: #fff;
		padding: 20rpx 0;
		max-height: 60vh;
		overflow-y: auto;
	}
</style>