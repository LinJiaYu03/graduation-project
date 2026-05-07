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
	

	const userId = ref('')
	const userInfo = uni.getStorageSync('userInfo')
	const isManager = userInfo.isBoss || userInfo.isManager // 判断是否为管理员
	const clubList = ref([])
	const searchData = ref({
		keyword: '',
		type: 'join',
		currentPage: '1',
		pageSize: '10'
	})

	const btnList = computed(() => {
		if (isManager) {
			return [
				{ name: '加入的', value: 'join' },
				{ name: '管理的', value: 'management' }
			]
		}
		return [{ name: '加入的', value: 'join' }]
	})

	function onChangeActive(item) {
		if (!isManager && item.value === 'management') return // 非管理员不能切换到管理 tab
		searchData.value.type = item.value
		getClubList()
	}

	async function getClubList() {
		let {
			data
		} = await apiQueryJoinClubList({
			userId: userId.value,
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

	onLoad(async (e) => {
		userId.value = e.id
		getClubList()
	})
</script>

<style lang="scss" scoped>
	.my-club {
		.my-club_seach {
			margin-bottom: 30rpx;
		}

		.my-club_btn {
			display: flex;
			flex: 1;
			gap: 20rpx;
			overflow-x: auto;
			padding-bottom: 30rpx;
			scrollbar-width: none;

			.btn {
				padding: 0 32rpx;
				height: 64rpx;
				min-width: 120rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				border: 2rpx solid #e0e0e0;
				border-radius: 16rpx;
				font-size: 28rpx;
				color: #666;
				background: #ffffff;
				white-space: nowrap;
				font-weight: 500;
			}

			.active {
				background: linear-gradient(135deg,
						lighten($uni-topic-color, 5%) 0%,
						$uni-topic-color 100%);
				color: #ffffff;
				border: none;
				box-shadow: 0 6rpx 20rpx rgba($uni-topic-color, 0.25);
				font-weight: 600;
			}
		}

		.my-club_container {}
	}
</style>