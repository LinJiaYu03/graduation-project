<template>
	<view class="member-review container">
		<view class="list-card" v-if="userList.length!=0">
			<uni-list>
				<uni-list-item style="height: 170rpx;" v-for="item in userList" :key="item.id" :title="item.realName"
					:note="item.studentNo" :thumb="item.avatarUrl" thumb-size="lg">
					<!-- 自定义 footer-->
					<template v-slot:footer>
						<view v-for="tagItem in tagList" :key="tagItem.title" class="tag"
							:class="tagItem.value ? 'tag--agree' : 'tag--reject'"
							@click="handleReview(tagItem.value,item.id)">{{ tagItem.title }}</view>
					</template>
				</uni-list-item>
			</uni-list>
		</view>
		<view v-else class="empty-container">
			<uni-icons type="info" size="60" color="#A39B90"></uni-icons>
			<text class="empty-text">暂无人员需要审核</text>
		</view>

		<uni-popup ref="managerReviewDialog" type="dialog">
			<uni-popup-dialog type="info" confirmText="同意" cancelText="取消" content="是否确认此操作" @confirm="managerReview" />
		</uni-popup>
	</view>
</template>

<script setup>
	import {
		onLoad
	} from '@dcloudio/uni-app'
	import {
		onMounted,
		ref
	} from 'vue'
	import {
		apiGetMemberReviewList,
		apiMemberReview
	} from '@/api/activity/index.js'

	const tagList = [{
			title: '同意',
			value: true
		},
		{
			title: '拒绝',
			value: false
		}
	]

	const managerReviewDialog = ref(null)
	const activeId = ref('')
	const userId = ref('')
	const userList = ref([])
	const changeValue = ref()

	async function getMemberReviewList() {
		let res = await apiGetMemberReviewList({
			activityId: activeId.value
		})

		if (res.code == 200) {
			userList.value = res.data.items
		}
	}

	async function handleReview(value, id) {
		changeValue.value = value
		userId.value = id
		managerReviewDialog.value.open()
	}

	async function managerReview() {
		let res = await apiMemberReview({
			activityId: activeId.value,
			userId: userId.value,
			pass: changeValue.value,
		})

		if (res.code == 200) {
			uni.showToast({
				title: res.message,
				icon: 'success'
			})
		}
		getMemberReviewList()

	}

	onLoad((e) => {
		activeId.value = e.id
	})

	onMounted(() => {
		getMemberReviewList()
	})
</script>

<style lang="scss" scoped>
	.list-card {
		background: $bg-card;
		border: 1rpx solid $border-base;
		border-radius: $radius-md;
		overflow: hidden;
		box-shadow: $shadow-card;
	}

	.empty-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 60vh;
		padding: 40rpx;

		.empty-text {
			margin-top: 30rpx;
			font-size: 26rpx;
			color: $text-tertiary;
			text-align: center;
		}
	}

	.tag {
		margin-top: 24rpx;
		margin-left: 12rpx;
		padding: 0 20rpx;
		height: 52rpx;
		line-height: 52rpx;
		text-align: center;
		font-size: 24rpx;
		font-weight: 500;
		border-radius: $radius-pill;

		&--agree {
			background: $color-success-soft;
			color: $color-success;
		}

		&--reject {
			background: $color-danger-soft;
			color: $color-danger;
		}
	}
</style>