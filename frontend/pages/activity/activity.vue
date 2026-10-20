<template>
	<view class="activity container">
		<view class="activity_search">
			<com-search v-model:value="searchValue" @click="onSearch"></com-search>
		</view>

		<view class="activity_filter_tag_list">
			<com-filter-btn v-model:title="filterRes.status" text='状态' type="status"></com-filter-btn>
			<com-filter-btn v-model:title="filterRes.category" text='分类' type="category"></com-filter-btn>
			<com-filter-btn v-model:title="filterRes.level" text='等级' type="level"></com-filter-btn>
		</view>

		<view class="activity_list">
			<com-activity-item v-for="item in activityList" :activiyInfo="item"></com-activity-item>
		</view>
	</view>
	<!-- 自定义tabBar -->
	<custom-tabbar></custom-tabbar>
</template>

<script setup>
	import {
		onShow
	} from '@dcloudio/uni-app'
	import {
		reactive,
		ref
	} from 'vue'
	import comSearch from '@/components/com-search/com-search.vue';
	import comActivityItem from '@/components/com-activity-item/com-activity-item.vue';
	import comFilterBtn from '@/components/com-filter-btn/com-filter-btn.vue';
	import customTabbar from '@/components/custom-tabbar/custom-tabbar.vue';
	import {
		apiGetActivityList
	} from '@/api/activity/index.js'

	const searchValue = ref('')
	const activityList = ref()
	const filterRes = reactive({
		status: '',
		category: '',
		level: ''
	})

	function onSearch() {
		getActivityList()
	}

	async function getActivityList() {
		let res = await apiGetActivityList({
			...filterRes,
			keyword: searchValue.value
		})
		if (res.code == 200) {
			activityList.value = res.data.page.records
		}
	}

	onShow(() => {
		getActivityList()
	})
</script>

<style lang="scss" scoped>
	.activity {
		padding-bottom: calc(120rpx + env(safe-area-inset-bottom));

		.activity_search {
			margin-bottom: 30rpx;
		}

		.activity_filter_tag_list {
			margin-bottom: 30rpx;
			display: flex;
		}

		.activity_list {
			display: flex;
			flex-wrap: wrap;
			align-items: center;
			justify-content: space-between;
		}

	}
</style>