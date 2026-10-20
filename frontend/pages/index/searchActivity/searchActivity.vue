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
			<com-activity-item v-for="item in activityList" :activiyInfo="item"></com-activity-item>
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
		padding: 20rpx 24rpx;
		min-height: 100vh;

		.search-activity {
			margin-bottom: 50rpx;
		}

		.activity_history {

			.title {
				margin-bottom: 50rpx;
				display: flex;
				align-items: center;
				justify-content: space-between;
				font-size: 16px;

				.left {
					font-weight: 500;
				}

				.right {
					color: $uni-topic-color;
				}
			}

			.history_list {
				.history_item {
					display: inline-block;
					margin: 0 20rpx 20rpx 0;
					padding: 10rpx 30rpx;
					height: 40rpx;
					line-height: 40rpx;
					text-align: center;
					background-color: #F0F0F0;
					border-radius: 15rpx;
					box-sizing: content-box;
					font-size: 25rpx;
				}
			}

		}

		.search-activity_list {
			display: flex;
			flex-wrap: wrap;
			align-items: center;
			justify-content: space-between;
		}
	}
</style>