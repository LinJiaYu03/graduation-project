<template>
	<view class="clubDetails container">
		<!-- 社团基本信息 -->
		<view class="clubDetails_info">
			<view class="title">{{ clubInfo.name }}</view>
			<view class="id">#ID:{{ clubInfo.id }}</view>
			<view class="btn" @click="onShowDialog">加入社团</view>
		</view>

		<!-- 社团成员 -->
		<view class="clubDetails_member">
			<view class="title">社团成员</view>
			<view class="text">当前社团共有{{ clubInfo.memberCount }}位成员 <view class="details" @click="onCheckUserList">查看
				</view>
			</view>

		</view>

		<!-- 社团简介 -->
		<view class="clubDatails_info">
			<view class="title">社团简介</view>
			<view class="text">{{ clubInfo.description }}</view>
		</view>

		<!-- 社团活动 -->
		<view class="clubDatails_activity">
			<view class="title">社团活动</view>
			<view class="activity_list" v-if="activityList.length!=0">
				<view class="activity_item_wrap" v-for="item in activityList" :key="item.id">
					<com-activity-item :activiyInfo="item"></com-activity-item>
				</view>
			</view>
			<view v-else>社团暂无活动</view>
		</view>
	</view>

	<!-- 提示窗示例 -->
	<uni-popup ref="alertDialog" type="dialog">
		<uni-popup-dialog type="info" confirmText="加入" cancelText="取消" content="是否确认加入该社团" @confirm="onJoinClub" />
	</uni-popup>


	<uni-drawer ref="showRight" mode="right" :width="300">
		<view class="scroll-view">
			<scroll-view class="scroll-view-box" scroll-y>
				<uni-list>
					<uni-list-item :clickable="isBoss" style="height: 170rpx;" v-for="item in userList" :key="item.userId"
						:title="item.user.realName"
						:note="item.user.schoolName+item.user.collegeName+item.user.className"
						:thumb="item.user.avatarUrl" thumb-size="lg" @click="onShowSettingManagerDialog(item)">
						<!-- 自定义 footer-->
						<template v-slot:footer>
							<uni-tag class="tag" v-if="item.isManager" text="管理" type="error" />
							<uni-tag class="tag" v-else text="成员" type="primary" />
						</template>
					</uni-list-item>
				</uni-list>
			</scroll-view>
		</view>
	</uni-drawer>

	<uni-popup ref="settingManagerDialog" type="dialog">
		<uni-popup-dialog type="info" confirmText="设置" cancelText="取消" content="是否设置该成员为管理员"
			@confirm="settingManager" />
	</uni-popup>

</template>

<script setup>
	import {
		onLoad
	} from '@dcloudio/uni-app'
	import comActivityItem from '@/components/com-activity-item/com-activity-item.vue';
	import {
		ref,
		defineProps,
		onMounted
	} from 'vue';
	import {
		apiJoinClub,
		apiGetJoinClubUserList,
		apiSettingClubManager
	} from '@/api/club/index.js'
	import {
		apiGetClubActivity
	} from '@/api/activity/index.js'
	import { storeToRefs } from 'pinia';
	import { useUserStore } from '@/stores/user.js';

	const userStore = useUserStore()
	const { isBoss } = storeToRefs(userStore)

	const props = defineProps({
		info: {
			type: String,
			default: ''
		}
	})

	const alertDialog = ref(null)
	const settingManagerDialog = ref(null)
	const showRight = ref(null)
	const activityList = ref([])
	const clubInfo = ref([])
	const userList = ref([])
	const settingManagerUserid = ref('')

	function onShowDialog() {
		alertDialog.value?.open()
	}

	async function onJoinClub() {
		let res = await apiJoinClub({
			clubId: clubInfo.value.id
		})

		if (res.code == 200) {
			uni.showToast({
				icon: 'success',
				title: res.message
			})


			setTimeout(() => {
				uni.reLaunch({
					url: '/pages/clubList/clubList'
				})
			}, 1500)
		}
	}

	async function getJoinClubUserList() {
		let res = await apiGetJoinClubUserList(clubInfo.value.id)
		if (res.code == 200) {
			userList.value = res.data.items
		}
	}

	function onShowSettingManagerDialog(item) {
		settingManagerUserid.value = item.userId
		showRight.value?.close()
		settingManagerDialog.value?.open()
	}

	async function settingManager() {
		let res = await apiSettingClubManager({
			clubId: clubInfo.value.id,
			userId: settingManagerUserid.value,
			isManager: true
		})

		if (res.code == 200) {
			uni.showToast({
				icon: 'success',
				title: res.message
			})
		}
	}

	async function getClubActivity() {
		let res = await apiGetClubActivity(clubInfo.value.id)
		if (res.code == 200) {
			activityList.value = res.data.page.records
		}
	}

	function onCheckUserList() {
		showRight.value?.open()
		getJoinClubUserList()
	}

	onLoad((e) => {
		// 兼容：优先使用路由参数，其次使用组件 props 传入的 info，避免 H5 模式下出现多余属性警告
		const rawInfo = (e && e.info) || props.info
		if (rawInfo) {
			clubInfo.value = JSON.parse(decodeURIComponent(rawInfo))
		}
	})

	onMounted(() => {
		getClubActivity()
	})
</script>

<style lang="scss" scoped>
	.clubDetails {

		// 公共样式
		.title {
			font-size: 32rpx;
			font-weight: 600;
			color: $text-primary;
			margin-bottom: 24rpx;
		}

		.text {
			font-size: 28rpx;
			color: $text-secondary;
			line-height: 1.6;
		}

		// 社团信息区块
		.clubDetails_info {
			margin-bottom: 24rpx;
			padding: 32rpx;
			background: $bg-card;
			border: 1rpx solid $border-base;
			border-radius: $radius-md;
			box-shadow: $shadow-card;

			.title {
				font-size: 40rpx;
				margin-bottom: 12rpx;
			}

			.id {
				font-size: 24rpx;
				color: $text-tertiary;
				margin-bottom: 28rpx;
			}

			.btn {
				padding: 16rpx 40rpx;
				display: inline-block;
				color: $text-on-primary;
				font-size: 26rpx;
				font-weight: 500;
				background: $brand-primary;
				border-radius: $radius-pill;

				&:active {
					background: $brand-primary-deep;
				}
			}
		}

		// 社团成员区块
		.clubDetails_member {
			margin-bottom: 24rpx;
			padding: 32rpx;
			background: $bg-card;
			border: 1rpx solid $border-base;
			border-radius: $radius-md;
			box-shadow: $shadow-card;

			.text {
				display: flex;
				align-items: center;
				justify-content: space-between;
				font-size: 28rpx;
				color: $text-primary;
			}

			.details {
				font-size: 24rpx;
				color: $brand-primary-ink;
				font-weight: 500;
				display: inline-block;
				padding: 6rpx 18rpx;
				border-radius: $radius-pill;
				background-color: $brand-primary-soft;

				&:active {
					background-color: $bg-hover;
				}
			}
		}

		// 社团简介区块
		.clubDatails_info {
			margin-bottom: 24rpx;
			padding: 32rpx;
			background: $bg-card;
			border: 1rpx solid $border-base;
			border-radius: $radius-md;
			box-shadow: $shadow-card;

			.text {
				background: $bg-subtle;
				padding: 28rpx;
				border-radius: $radius-sm;
			}
		}

		// 社团活动区块
		.clubDatails_activity {
			margin-bottom: 24rpx;

			.activity_list {
				display: flex;
				flex-wrap: wrap;
				align-items: flex-start;
				justify-content: space-between;
			}
		}

		// 区块通用样式
		.clubDetails_member,
		.clubDatails_info,
		.clubDatails_activity {
			.title {
				position: relative;
				padding-left: 20rpx;

				&::before {
					content: '';
					position: absolute;
					left: 0;
					top: 50%;
					transform: translateY(-50%);
					width: 6rpx;
					height: 24rpx;
					background: $brand-primary;
					border-radius: 3rpx;
				}
			}
		}

	}

	.scroll-view {
		/* #ifndef APP-NVUE */
		width: 100%;
		height: 100%;
		/* #endif */
		flex: 1
	}

	// 处理抽屉内容滚动
	.scroll-view-box {
		flex: 1;
		position: absolute;
		top: 0;
		right: 0;
		bottom: 0;
		left: 0;

		.info-content {
			padding: 5px 15px;
		}
	}

	.tag {
		margin-top: 40rpx;
		height: 30rpx;
		text-align: center;
		line-height: 30rpx;
	}
</style>