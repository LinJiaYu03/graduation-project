<template>
	<view class="my-club container">
		<view class="my-club_seach">
			<com-search v-model:value="searchData.keyword" @click="onSearch"></com-search>

		</view>
		<view class="my-club_btn">
			<view class="btn" :class="{ active: item.value===searchData.type}" v-for="item in btnList" :key="item.value"
				@click="onChangeActive(item)">
				{{ item.name }}
			</view>
		</view>
		<view class="my-club_container">
			<uni-list>
				<uni-list-item clickable @click="uni.navigateTo({
					url:`/pages/clubList/clubDetails/clubDetails?info=${encodeURIComponent(JSON.stringify(item))}`
				})" style="height: 170rpx;" v-for="item in clubList" :key="item.id" :title="item.name" :note="item.tags"
					:thumb="item.iconUrl" thumb-size="lg" :rightText="String(item.memberCount)">
				</uni-list-item>
			</uni-list>
		</view>
	</view>
</template>

<script setup>
	import {
		ref,
		computed
	} from 'vue';
	import {
		onLoad
	} from '@dcloudio/uni-app'
	import comSearchVue from '@/components/com-search/com-search.vue';
	import {
		apiQueryJoinClubList
	} from '@/api/club/index.js'
	import { storeToRefs } from 'pinia'
	import { useUserStore } from '@/stores/user.js'

	const userStore = useUserStore()
	const { isManager } = storeToRefs(userStore)
	const clubList = ref([])
	const searchData = ref({
		keyword: '',
		type: 'join',
		currentPage: '1',
		pageSize: '10'
	})

	const btnList = computed(() => {
		if (isManager.value) {
			return [
				{ name: '加入的', value: 'join' },
				{ name: '管理的', value: 'management' }
			]
		}
		return [{ name: '加入的', value: 'join' }]
	})

	function onChangeActive(item) {
		if (!isManager.value && item.value === 'management') return // 非管理员不能切换到管理 tab
		searchData.value.type = item.value
		getClubList()
	}

	async function getClubList() {
		let {
			data
		} = await apiQueryJoinClubList({
			...searchData.value
		})
		if (searchData.value.currentPage == data.page.currentPage && searchData.value.pageSize == data.page.pageSize) {
			clubList.value = data.page.records
		} else {
			clubList.value = [...clubList.value, ...data.page.records]
		}
	}

	function onSearch() {
		getClubList()
	}

	onLoad(() => {
		getClubList()
	})
</script>

<style lang="scss" scoped>
	.my-club {
		.my-club_seach {
			margin-bottom: 24rpx;
		}

		.my-club_btn {
			display: flex;
			flex: 1;
			gap: 16rpx;
			overflow-x: auto;
			padding-bottom: 24rpx;
			scrollbar-width: none;

			.btn {
				padding: 0 32rpx;
				height: 64rpx;
				min-width: 120rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				border: 2rpx solid $border-base;
				border-radius: $radius-pill;
				font-size: 26rpx;
				color: $text-secondary;
				background: $bg-card;
				white-space: nowrap;
				font-weight: 500;
			}

			.active {
				background: $brand-primary-soft;
				color: $brand-primary-ink;
				border-color: transparent;
				font-weight: 600;
			}
		}

		.my-club_container {}
	}
</style>