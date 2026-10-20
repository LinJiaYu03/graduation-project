<template>
	<view class="user container">

		<!-- 用户信息 -->
		<view class="user-info">
			<view class="avatar-section">
				<image v-if="!userInfo.avatarUrl" class="avatar" src="/static/logo.png" mode=""></image>
				<image v-else class="avatar" :src="userInfo.avatarUrl" mode="aspectFill"></image>
				<view class="user-detail">
					<view class="name-row">
						<view class="name" v-if="!token">
							<navigator url="/pages/system/login/login">立即登录</navigator>
						</view>
						<text class="name" v-else>{{ userInfo.realName }}</text>
					</view>
					<text class="student-id" v-if="token">学号：{{ userInfo.studentNo }}</text>
				</view>
			</view>
		</view>

		<!-- 快捷入口 -->
		<view class="quick-section">
			<view class="quick-grid">
				<!-- 基本信息 -->
				<view class="quick-item" @click="() => uni.navigateTo({
					url: '/pages/user/userInfo/userInfo'
				})">
					<view class="quick-icon green">
						<uni-icons type="person" size="24" color="#fff"></uni-icons>
					</view>
					<text class="quick-label">基本信息</text>
				</view>
				<!-- 发布活动 -->
				<view v-if="isManager" class="quick-item" @click="() => uni.navigateTo({
					url: '/pages/user/publishActivity/publishActivity'
				})">
					<view class="quick-icon purple">
						<uni-icons type="plusempty" size="24" color="#fff"></uni-icons>
					</view>
					<text class="quick-label">发布活动</text>
				</view>
				<!-- 创建社团 -->
				<view v-if="isBoss" class="quick-item" @click="()=>uni.navigateTo({
					url:'/pages/user/createClub/createClub'
				})">
					<view class="quick-icon blue">
						<uni-icons type="plusempty" size="24" color="#fff"></uni-icons>
					</view>
					<text class="quick-label">创建社团</text>
				</view>
				<!-- 创建班级 -->
				<view v-if="isBoss" class="quick-item" @click="() => uni.navigateTo({
					url: '/pages/user/createClass/createClass'
				})">
					<view class="quick-icon grey">
						<uni-icons type="plusempty" size="24" color="#fff"></uni-icons>
					</view>
					<text class="quick-label">添加班级</text>
				</view>
			</view>
		</view>

		<!-- 我的服务 -->
		<view class="services-section">
			<text class="section-title">我的服务</text>
			<view class="services-grid">
				<!-- 活动审核 -->
				<view v-if="isBoss" class="service-item" @click="uni.navigateTo({
					url:'/pages/user/clubReview/clubReview'
				})">
					<view class="service-icon blue">
						<uni-icons type="calendar" size="24" color="#fff"></uni-icons>
					</view>
					<text class="service-label">活动审核</text>
				</view>

				<!-- 我的活动 -->
				<view class="service-item" @click="() => {
					uni.navigateTo({
						url: '/pages/user/myActivity/myActivity'
					})
				}">
					<view class="service-icon purple">
						<uni-icons type="star" size="24" color="#fff"></uni-icons>
					</view>
					<text class="service-label">我的活动</text>
				</view>

				<!-- 我的社团 -->
				<view class="service-item" @click="() => {
					uni.navigateTo({
						url: `/pages/user/myClub/myClub?id=${userInfo.id}`
					})
				}">
					<view class="service-icon green">
						<uni-icons type="medal" size="24" color="#fff"></uni-icons>
					</view>
					<text class="service-label">我的社团</text>
				</view>

				<!-- 班级列表 -->
				<view v-if="isBoss" class="service-item" @click="() => uni.navigateTo({
					url: '/pages/user/classList/classList'
				})">
					<view class="service-icon red">
						<uni-icons type="contact" size="24" color="#fff"></uni-icons>
					</view>
					<text class="service-label">班级列表</text>
				</view>
			</view>
		</view>

		<view v-if="token" class="logout-container">
			<view class="logout-btn" @click="onOutLogin">
				<text class="logout-text">退出登录</text>
			</view>
		</view>
	</view>
	<uni-popup ref="logoutPopup" type="dialog" background-color="#fff">
		<uni-popup-dialog type="info" title="退出登录" content="确认退出当前账号？" confirmText="退出" cancelText="取消"
			@confirm="confirmLogout" />
	</uni-popup>
	<!-- 自定义tabBar -->
	<custom-tabbar></custom-tabbar>
</template>

<script setup>
import {
	ref
} from 'vue';
import customTabbar from '@/components/custom-tabbar/custom-tabbar.vue';
import useUserPermission from '@/hooks/useUserPermission.js'

const token = uni.getStorageSync('token')
const userInfo = uni.getStorageSync('userInfo')
const { isBoss,isManager }=useUserPermission()

const logoutPopup = ref(null)

function onOutLogin() {
	logoutPopup.value?.open()
}

function confirmLogout() {
	uni.clearStorageSync()
	uni.reLaunch({
		url: '/pages/index/index'
	})
}
</script>

<style lang="scss" scoped>
.user {
	position: relative;
	padding-bottom: calc(120rpx + env(safe-area-inset-bottom));

	.logout-container {
		margin: 350rpx 24rpx;
		display: flex;
		justify-content: center;

		.logout-btn {
			width: 100%;
			max-width: 400rpx;
			height: 88rpx;
			background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
			border: 2rpx solid #fff;
			border-radius: 44rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			gap: 12rpx;
			transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
			box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);

			.logout-text {
				font-size: 30rpx;
				font-weight: 500;
				letter-spacing: 0.5rpx;
			}

		}
	}
}

// 用户信息
.user-info {
	height: 280rpx;
	background: linear-gradient(135deg, #FCB857 0%, #FF9800 100%);
	padding: 60rpx 30rpx 40rpx;
	margin: 0 -24rpx 30rpx -24rpx;
	display: flex;
	flex-direction: column;
	position: relative;
	overflow: hidden;
	box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);

	.avatar-section {
		display: flex;
		align-items: center;
		gap: 24rpx;
		position: relative;
		z-index: 1;

		.avatar {
			width: 120rpx;
			height: 120rpx;
			border-radius: 50%;
			background: #fff;
			border: 4rpx solid rgba(255, 255, 255, 0.3);
			box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.2);
		}

		.user-detail {
			flex: 1;

			.name-row {
				display: flex;
				align-items: center;
				gap: 20rpx;
				margin-bottom: 12rpx;

				.name {
					font-size: 40rpx;
					font-weight: 600;
					color: #fff;
					letter-spacing: 1rpx;
				}

			}

			.student-id {
				font-size: 28rpx;
				color: rgba(255, 255, 255, 0.9);
				display: block;
			}
		}
	}
}

// 快捷入口
.quick-section {
	background: #fff;
	border-radius: 20rpx;
	padding: 32rpx 24rpx;
	margin-bottom: 24rpx;
	box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);

	.quick-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 32rpx;

		.quick-item {
			display: flex;
			flex-direction: column;
			align-items: center;

			.quick-icon {
				width: 88rpx;
				height: 88rpx;
				border-radius: 20rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 16rpx;
				transition: all 0.2s ease;

				&.purple {
					background: #8b5cf6;
				}

				&.blue {
					background: #3b82f6;
				}

				&.green {
					background: #10b981;
				}

				&.grey {
					background: #f5e63b;
				}
			}

			.quick-label {
				font-size: 26rpx;
				color: #333;
				font-weight: 500;
				line-height: 1.4;
			}
		}
	}
}

// 我的服务
.services-section {
	background: #fff;
	border-radius: 20rpx;
	padding: 32rpx 24rpx;
	box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);

	.section-title {
		display: block;
		font-size: 32rpx;
		font-weight: 600;
		color: #1f2937;
		margin-bottom: 32rpx;
		padding-left: 16rpx;
		position: relative;

		&::before {
			content: '';
			position: absolute;
			left: 0;
			top: 50%;
			transform: translateY(-50%);
			width: 6rpx;
			height: 28rpx;
			background: $uni-topic-color;
			border-radius: 3rpx;
		}
	}

	.services-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 32rpx 24rpx;

		.service-item {
			display: flex;
			flex-direction: column;
			align-items: center;

			.service-icon {
				width: 76rpx;
				height: 76rpx;
				border-radius: 16rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 16rpx;
				transition: all 0.2s ease;


				&.blue {
					background: #3b82f6;
				}

				&.red {
					background: #ef4444;
				}

				&.orange {
					background: #f97316;
				}

				&.purple {
					background: #8b5cf6;
				}

				&.green {
					background: #10b981;
				}

				&.cyan {
					background: #06b6d4;
				}

				&.grey {
					background: #9ca3af;
				}

				&.dark-grey {
					background: #6b7280;
				}
			}

			.service-label {
				font-size: 26rpx;
				color: #374151;
				text-align: center;
				line-height: 1.4;
				font-weight: 500;
			}
		}
	}
}
</style>