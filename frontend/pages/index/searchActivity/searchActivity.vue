<template>
	<view class="com-search-activity_container">

		<view class="search-activity">
			<com-search v-model:value="searchValue" @click="onSearch"></com-search>
		</view>

		<view class="activity_history">
			<view class="title" v-if="!isShowSearchHistory">
				<view class="left">
					历史搜索
				</view>
				<view class="right" @click="onClear">
					清空
				</view>
			</view>

			<view class="history_list">
				<view class="history_item" v-for="(item,index) in searchHistory" :key="item+index"
					@click="onClickHistory(item)">
					{{item}}
				</view>
			</view>
		</view>

		<view class="search-activity_list">
			<view class="activity_item_wrap" v-for="item in activityList" :key="item.id">
				<com-activity-item :activiyInfo="item"></com-activity-item>
			</view>
		</view>

	</view>
</template>

<script setup>
	import {
		computed,
		onMounted,
		ref
	} from 'vue'
	import comSearch from '@/components/com-search/com-search.vue';
	import comActivityItem from '@/components/com-activity-item/com-activity-item.vue';
	import {
		apiGetActivityList
	} from '@/api/activity/index.js'

	const searchValue = ref('')
	const searchHistory = ref(uni.getStorageSync('searchHistory') || [])
	const activityList = ref([])

	const isShowSearchHistory = computed(() => searchHistory.value.length === 0)

	async function onSearch() {
		if (searchValue.value == '') return
		searchHistory.value.unshift(searchValue.value)
		searchHistory.value = [...new Set(searchHistory.value)]
		if (searchHistory.value.length > 10) {
			searchHistory.value.pop()
		}
		let res= await apiGetActivityList({
			keyword: searchValue.value
		})
		
		
		if(res.code==200){
			activityList.value= res.data.page.records
			
			
			uni.setStorageSync('searchHistory', searchHistory.value)
		}
	}

	function onClear() {
		searchHistory.value = []
		uni.clearStorageSync('searchHistory')
	}

	function onClickHistory(item) {
		searchValue.value = item
	}
</script>

<style lang="scss" scoped>
	.com-search-activity_container {
		padding: 24rpx;
		min-height: 100vh;

		.search-activity {
			margin-bottom: 32rpx;
		}

		.activity_history {

			.title {
				margin-bottom: 24rpx;
				display: flex;
				align-items: center;
				justify-content: space-between;
				font-size: 30rpx;
				font-weight: 600;
				color: $text-primary;

				.left {
					font-weight: 600;
				}

				.right {
					font-size: 24rpx;
					font-weight: 400;
					color: $brand-primary-ink;
				}
			}

			.history_list {
				.history_item {
					display: inline-block;
					margin: 0 16rpx 16rpx 0;
					padding: 0 24rpx;
					height: 56rpx;
					line-height: 56rpx;
					text-align: center;
					background-color: $bg-card;
					border: 1rpx solid $border-base;
					border-radius: $radius-pill;
					box-sizing: border-box;
					font-size: 26rpx;
					color: $text-secondary;
				}
			}

		}

		.search-activity_list {
			display: flex;
			flex-wrap: wrap;
			align-items: flex-start;
			justify-content: space-between;
		}
	}
</style>