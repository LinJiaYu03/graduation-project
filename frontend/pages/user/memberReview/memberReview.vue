<template>
	<view class="member-review container">
		<uni-list v-if="userList.length!=0">
			<uni-list-item style="height: 170rpx;" v-for="item in userList" :key="item.id" :title="item.realName"
				:note="item.schoolName+item.collegeName+item.className" :thumb="item.avatarUrl" thumb-size="lg">
				<!-- 自定义 footer-->
				<template v-slot:footer>
					<uni-tag v-for="tagItem in tagList" class="tag" :text="tagItem.title"
						:type="tagItem.value?'primary':'error'" @click="handleReview(tagItem.value,item.id)" />
				</template>
			</uni-list-item>
		</uni-list>
		<view v-else class="empty-container">
			<uni-icons type="info" size="60" color="#c0c4cc"></uni-icons>
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
	const managerUserId = uni.getStorageSync('userInfo').id
	const userList = ref([])
	const changeValue = ref()

	async function getMemberReviewList() {
		let res = await apiGetMemberReviewList({
			activityId: activeId.value,
			userId: managerUserId
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
			managerUserId,
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
	.empty-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 60vh;
		padding: 40rpx;

		.empty-text {
			margin-top: 30rpx;
			font-size: 28rpx;
			color: #909399;
			text-align: center;
		}
	}

	.tag {
		margin-top: 30rpx;
		margin-left: 15rpx;
		height: 30rpx;
		text-align: center;
		line-height: 30rpx;
	}
</style>