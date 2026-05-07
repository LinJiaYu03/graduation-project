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
	const isManager = userInfo.isBoss || userInfo.isManager // 判断是否为管理员
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
		padding: 24rpx 32rpx;
		padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
		min-height: 100vh;
		background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);

		.registration_search {
			margin-bottom: 40rpx;
			box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
			border-radius: 16rpx;
			overflow: hidden;
		}

		.registration_filter {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 40rpx;
			padding: 20rpx 0;
			position: relative;

			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 0;
				right: 0;
				height: 2rpx;
				background: linear-gradient(90deg,
						rgba($uni-topic-color, 0.1) 0%,
						rgba($uni-topic-color, 0.3) 50%,
						rgba($uni-topic-color, 0.1) 100%);
			}

			.left {
				display: flex;
				flex: 1;
				gap: 20rpx;
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
					border: 2rpx solid #e0e0e0;
					border-radius: 16rpx;
					font-size: 28rpx;
					color: #666;
					background: #ffffff;
					transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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

			.right {
				flex-shrink: 0;
				margin-left: 24rpx;
			}
		}

	}
</style>