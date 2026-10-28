<template>
	<view class="registration container">
		<view class="registration_search">
			<com-search v-model:value="searchValue" @click="onSearch"></com-search>
		</view>
		<view class="registration_filter">
			<view class="left">
				<view v-for="tab in tabs" :key="tab.value" class="btn" :class="{ active: activeTab === tab.value }"
					@click="OnChangeActiveTab(tab.value)">
					{{ tab.label }}
				</view>
			</view>

		</view>
		<view class="registration_activity_list">
			<view v-if="activeTab==='participated'">
				<com-activity-item v-for="item in activity_participated" :key="item.id" :activeInfo="item">
				</com-activity-item>
			</view>
			<view v-else>
				<com-activity-item-managed v-for="item in activity_managed" :key="item.id" :activeInfo="item"
					@updataActivityList="getJoinOrManangeActivityList">
				</com-activity-item-managed>
			</view>

		</view>
	</view>
</template>

<script setup>
	import comSearch from '@/components/com-search/com-search.vue';
	import comActivityItem from './components/com-activity-item/com-activity-item.vue';
	import comActivityItemManaged from './components/com-activity-item-managed/com-activity-item-managed.vue';
	import {
		ref,
		computed
	} from 'vue'
	import {
		onShow
	} from '@dcloudio/uni-app'
	import {
		apiGetJoinOrManangeActivity
	} from '@/api/activity/index.js'

	const searchValue = ref('')
	const activeTab = ref('participated')
	const userInfo = uni.getStorageSync('userInfo')
	const userId = userInfo.id
	const isManager = (userInfo.roles || []).some(role =>
		role.code === 'ADMIN' || role.code === 'CLUB_MANAGER'
	)
	const activity_participated = ref([])
	const activity_managed = ref([])

	const tabs = computed(() => {
		if (isManager) {
			return [
				{ label: '参与', value: 'participated' },
				{ label: '管理', value: 'managed' }
			]
		}
		return [{ label: '参与', value: 'participated' }]
	})

	function onSearch() {
		getJoinOrManangeActivityList()
	}

	function OnChangeActiveTab(tab) {
		if (!isManager && tab === 'managed') return // 非管理员不能切换到管理 tab
		activeTab.value = tab
		getJoinOrManangeActivityList()
	}


	async function getJoinOrManangeActivityList() {
		let res = await apiGetJoinOrManangeActivity({
			id: userId,
			type: activeTab.value,
			keyword: searchValue.value
		})
		if (res.code == 200) {
			let {
				activities
			} = res.data

			activeTab.value === 'participated' ? activity_participated.value = activities : activity_managed.value =
				activities
		}
	}

	onShow(() => {
		getJoinOrManangeActivityList()
	})
</script>

<style lang="scss" scoped>
	.registration {
		padding: 24rpx;
		padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
		min-height: 100vh;

		.registration_search {
			margin-bottom: 24rpx;
		}

		.registration_filter {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 32rpx;
			padding: 0 0 20rpx;
			position: relative;

			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 0;
				right: 0;
				height: 1rpx;
				background: $border-light;
			}

			.left {
				display: flex;
				flex: 1;
				gap: 16rpx;
				overflow-x: auto;
				padding-bottom: 8rpx;
				scrollbar-width: none;

				&::-webkit-scrollbar {
					display: none;
				}

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

			.right {
				flex-shrink: 0;
				margin-left: 24rpx;
			}
		}

	}
</style>