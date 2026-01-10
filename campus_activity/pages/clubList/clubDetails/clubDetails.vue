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
			<view class="activity_list">
				<com-activity-item v-if="activityList.length!=0" v-for="item in activityList"
					:activiyInfo="item">
				</com-activity-item>
				<view v-else>社团暂无活动</view>
			</view>
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
						:thumb="item.user.avatarUrl" thumb-size="lg" @click="onShowSettingManagerDialog(item.userId)">
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
	import useUserPermission from '@/hooks/useUserPermission';

	const {
		isBoss
	} = useUserPermission()

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
	const userInfo = ref(uni.getStorageSync('userInfo'))
	const settingManagerUserid = ref('')

	function onShowDialog() {
		alertDialog.value?.open()
	}

	async function onJoinClub() {
		let res = await apiJoinClub({
			clubId: clubInfo.value.id,
			userId: userInfo.value.id
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

	function onShowSettingManagerDialog(id) {
		settingManagerUserid.value = id
		showRight.value?.close()
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
			font-size: 40rpx;
			font-weight: 500;
			color: #333;
			margin-bottom: 50rpx;
		}

		.text {
			font-size: 28rpx;
			color: #666;
			line-height: 1.6;
		}

		// 社团信息区块
		.clubDetails_info {
			margin-bottom: 60rpx;
			padding-bottom: 50rpx;
			border-bottom: 1rpx solid #f0f0f0;

			.title {
				font-size: 44rpx;
				color: #1a1a1a;
				margin-bottom: 30rpx;
			}

			.id {
				font-size: 26rpx;
				color: #999;
				margin-bottom: 40rpx;
			}

			.btn {
				padding: 16rpx 32rpx;
				display: inline-block;
				color: #fff;
				font-size: 28rpx;
				background: linear-gradient(135deg, #0083F4, #0066CC);
				border-radius: 50rpx;
				box-shadow: 0 4rpx 12rpx rgba(0, 131, 244, 0.3);
				transition: all 0.3s ease;

				&:active {
					transform: scale(0.98);
					box-shadow: 0 2rpx 8rpx rgba(0, 131, 244, 0.4);
				}
			}
		}

		// 社团成员区块
		.clubDetails_member {
			margin-bottom: 90rpx;
			border-bottom: 1rpx solid #f0f0f0;

			.text {
				display: flex;
				align-items: center;
				justify-content: space-between;
				margin-bottom: 45rpx;
				font-size: 30rpx;
				color: #333;
			}

			.details {
				font-size: 28rpx;
				color: #0083F4;
				font-weight: 500;
				display: inline-block;
				padding: 8rpx 16rpx;
				border-radius: 8rpx;
				background-color: rgba(0, 131, 244, 0.1);

				&:active {
					background-color: rgba(0, 131, 244, 0.2);
				}
			}


		}

		// 社团简介区块
		.clubDatails_info {
			margin-bottom: 90rpx;
			padding-bottom: 50rpx;
			border-bottom: 1rpx solid #f0f0f0;

			.text {
				background: linear-gradient(135deg, #f8f9fa, #e9ecef);
				padding: 40rpx;
				border-radius: 20rpx;
			}
		}

		// 社团活动区块
		.clubDatails_activity {
			.activity_list {
				display: flex;
				flex-wrap: wrap;
				align-items: stretch;
				justify-content: space-between;

				// 为活动项添加统一的卡片效果
				::v-deep .activity-item {
					border-radius: 20rpx;
					overflow: hidden;
					box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
					transition: all 0.3s ease;

					&:active {
						transform: translateY(-4rpx);
						box-shadow: 0 8rpx 30rpx rgba(0, 0, 0, 0.12);
					}
				}
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
					width: 8rpx;
					height: 32rpx;
					background: linear-gradient(135deg, #0083F4, #00A3FF);
					border-radius: 4rpx;
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