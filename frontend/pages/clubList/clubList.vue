<template>
	<view class="tribe_list container">
		<view class="tribe_seach">
			<com-search v-model:value="searchData.keyword" @click="onSearch"></com-search>
		</view>
		<view class="tribe_list_container">
			<view class="title">
				全部社团
			</view>
			<view class="club_list">
				<view class="club_card" v-for="item in clubList" :key="item.id" @click="goDetail(item)">
					<image class="club_avatar" :src="item.iconUrl" mode="aspectFill"></image>
					<view class="club_info">
						<view class="club_name">{{ item.name }}</view>
					</view>
					<view class="club_count">
						<text class="num">{{ item.memberCount }}</text>
						<text class="unit">人</text>
					</view>
				</view>
			</view>
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

	function goDetail(item) {
		uni.navigateTo({
			url: `/pages/clubList/clubDetails/clubDetails?info=${encodeURIComponent(JSON.stringify(item))}`
		})
	}

	onShow(() => {
		getClubList()
	})
</script>

<style lang="scss" scoped>
	.tribe_list {
		.tribe_seach {
			margin-bottom: 24rpx;
		}

		.tribe_list_container {
			.title {
				margin: 24rpx 0;
				font-size: 32rpx;
				font-weight: 600;
				color: $text-primary;
			}

			.club_card {
				display: flex;
				align-items: center;
				background: $bg-card;
				border: 1rpx solid $border-base;
				border-radius: $radius-md;
				padding: 24rpx;
				margin-bottom: 20rpx;
				box-shadow: $shadow-card;

				&:active {
					background: $bg-subtle;
				}

				.club_avatar {
					width: 96rpx;
					height: 96rpx;
					border-radius: $radius-sm;
					background: $bg-subtle;
					flex-shrink: 0;
				}

				.club_info {
					flex: 1;
					min-width: 0;
					margin-left: 20rpx;

					.club_name {
						font-size: 28rpx;
						font-weight: 500;
						color: $text-primary;
						margin-bottom: 10rpx;
						overflow: hidden;
						white-space: nowrap;
						text-overflow: ellipsis;
					}
				}

				.club_count {
					flex-shrink: 0;
					margin-left: 20rpx;
					display: flex;
					align-items: baseline;

					.num {
						font-size: 30rpx;
						font-weight: 600;
						color: $brand-primary-ink;
					}

					.unit {
						font-size: 20rpx;
						color: $text-tertiary;
						margin-left: 4rpx;
					}
				}
			}
		}
	}
</style>