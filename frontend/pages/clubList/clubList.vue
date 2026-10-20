<template>
	<view class="tribe_list container">
		<view class="tribe_seach">
			<com-search v-model:value="searchData.keyword" @click="onSearch"></com-search>
		</view>
		<view class="tribe_list_container">
			<view class="title">
				全部社团
			</view>
			<uni-list>
				<uni-list-item clickable @click="uni.navigateTo({
					url:`/pages/clubList/clubDetails/clubDetails?info=${encodeURIComponent(JSON.stringify(item))}`
				})" style="height: 170rpx;" v-for="item in clubList" :key="item.id" :title="item.name" :note="item.levelTag+'#'+item.tags"
					:thumb="item.iconUrl" thumb-size="lg" :rightText="String(item.memberCount)">
				</uni-list-item>
			</uni-list>

		</view>
	</view>
	<!-- 自定义tabBar -->
	<custom-tabbar></custom-tabbar>
</template>

<script setup>
	import {
		onMounted,
		ref
	} from 'vue';
	import { onShow } from '@dcloudio/uni-app'
	import comSearchVue from '../../components/com-search/com-search.vue';
	import customTabbar from '../../components/custom-tabbar/custom-tabbar.vue';
	import {
		apiGetClubList
	} from '@/api/club/index.js'

	const searchData = ref({
		keyword: '',
		currentPage: '1',
		pageSize: '10'
	})
	const clubList = ref([])

	async function getClubList() {
		let {
			data
		} = await apiGetClubList(searchData.value)
		if (searchData.value.currentPage == data.page.currentPage && searchData.value.pageSize == data.page.pageSize) {
			clubList.value = data.page.records
		} else {
			clubList.value = [...clubList.value, ...data.page.records]
		}
	}

	function onSearch() {
		getClubList()
	}

	onShow(() => {
		getClubList()
	})
</script>

<style lang="scss" scoped>
	.tribe_list {
		.tribe_seach {}

		.tribe_list_container {
			.title {
				margin-top: 50rpx;
				margin-bottom: 50rpx;
				font-size: 20px;
				font-weight: 600;
			}
		}
	}
</style>