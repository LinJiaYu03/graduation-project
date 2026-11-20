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

		<!-- 个人信息 -->
		<view class="quick-section">
			<text class="section-title">个人信息</text>
			<view class="quick-grid">
				<!-- 基本信息 -->
				<view class="quick-item" @click="() => uni.navigateTo({
					url: '/pages/user/userInfo/userInfo'
				})">
					<view class="quick-icon">
						<uni-icons type="person" size="24" color="#E9A23C"></uni-icons>
					</view>
					<text class="quick-label">基本信息</text>
				</view>
				<!-- 账户安全 -->
				<view class="quick-item" @click="openAccountSecurity">
					<view class="quick-icon">
						<uni-icons type="locked-filled" size="24" color="#E9A23C"></uni-icons>
					</view>
					<text class="quick-label">账户安全</text>
				</view>
			</view>
		</view>

		<!-- 活动信息 -->
		<view class="services-section">
			<text class="section-title">活动信息</text>
			<view class="services-grid">
				<!-- 活动审核 -->
				<view v-if="isBoss" class="service-item" @click="uni.navigateTo({
					url:'/pages/user/clubReview/clubReview'
				})">
					<view class="service-icon">
						<uni-icons type="calendar" size="24" color="#E9A23C"></uni-icons>
					</view>
					<text class="service-label">活动审核</text>
				</view>

				<!-- 我的活动 -->
				<view class="service-item" @click="() => {
					uni.navigateTo({
						url: '/pages/user/myActivity/myActivity'
					})
				}">
					<view class="service-icon">
						<uni-icons type="star" size="24" color="#E9A23C"></uni-icons>
					</view>
					<text class="service-label">我的活动</text>
				</view>

				<!-- 我的社团 -->
				<view class="service-item" @click="() => {
					uni.navigateTo({
						url: '/pages/user/myClub/myClub'
					})
				}">
					<view class="service-icon">
						<uni-icons type="medal" size="24" color="#E9A23C"></uni-icons>
					</view>
					<text class="service-label">我的社团</text>
				</view>
			</view>
		</view>
	</view>
	<uni-popup ref="logoutPopup" type="dialog" background-color="#fff">
		<uni-popup-dialog type="info" title="退出登录" content="确认退出当前账号？" confirmText="退出" cancelText="取消"
			@confirm="confirmLogout" />
	</uni-popup>
	<!-- 账户安全抽屉 -->
	<uni-popup ref="securityPopup" type="right" background-color="transparent" @change="onSecurityPopupChange">
		<view class="security-drawer">
			<view class="drawer-header">
				<view class="drawer-heading">
					<text class="drawer-title">{{ securityView === 'password' ? '修改密码' : '账户安全' }}</text>
					<text class="drawer-subtitle">{{ securityView === 'password' ? '修改后需使用新密码重新登录' : '管理你的账号与登录安全' }}</text>
				</view>
				<view class="drawer-close" @click="closeSecurityDrawer">
					<uni-icons type="closeempty" size="22" color="#6E675D"></uni-icons>
				</view>
			</view>

			<scroll-view scroll-y class="drawer-body">
				<!-- 安全概览 -->
				<template v-if="securityView === 'overview'">
					<view class="security-status">
						<view class="status-icon">
							<uni-icons type="locked-filled" size="30" color="#E9A23C"></uni-icons>
						</view>
						<view class="status-info">
							<text class="status-title">账号保护中</text>
							<text class="status-desc">定期更换登录密码，不与他人共享账号</text>
						</view>
					</view>

					<text class="drawer-section-title">安全设置</text>
					<view class="setting-list">
						<view class="setting-item" @click="securityView = 'password'">
							<view class="setting-icon">
								<uni-icons type="locked" size="20" color="#E9A23C"></uni-icons>
							</view>
							<view class="setting-main">
								<text class="setting-label">登录密码</text>
								<text class="setting-value">建议定期修改</text>
							</view>
							<text class="setting-action">修改</text>
							<uni-icons type="right" size="14" color="#A39B90"></uni-icons>
						</view>
					</view>

					<text class="drawer-tip">如发现账号存在异常登录或信息被篡改，请立即修改密码并联系管理员。</text>
				</template>

				<!-- 修改密码 -->
				<template v-else>
					<view class="form-back" @click="securityView = 'overview'">
						<uni-icons type="left" size="14" color="#6E675D"></uni-icons>
						<text class="form-back-text">返回安全设置</text>
					</view>
					<com-base-form :model="passwordForm" :fields="passwordFields" :rules="passwordRules"
						submit-text="确认修改" :loading="submittingPassword" @submit="submitPasswordChange">
						<template #hint>
							<text class="form-hint">修改成功后当前登录状态将失效，需要使用新密码重新登录。</text>
						</template>
					</com-base-form>
				</template>
			</scroll-view>

			<view v-if="securityView === 'overview'" class="drawer-footer">
				<view class="logout-btn" @click="onOutLogin">
					<text class="logout-text">退出登录</text>
				</view>
			</view>
		</view>
	</uni-popup>
	<!-- 自定义tabBar -->
	<custom-tabbar v-if="!securityDrawerOpen"></custom-tabbar>
</template>

<script setup>
import {
	ref,
	computed
} from 'vue';
import customTabbar from '@/components/custom-tabbar/custom-tabbar.vue';
import comBaseForm from '@/components/com-base-form/com-base-form.vue';
import { storeToRefs } from 'pinia'
import { apiUserLogout, apiUpdatePassword } from '@/api/user/index.js'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()
const token = uni.getStorageSync('token')
const userInfo = computed(() => userStore.user || {})
const { isBoss } = storeToRefs(userStore)

const logoutPopup = ref(null)

// 账户安全抽屉
const securityPopup = ref(null)
const securityDrawerOpen = ref(false)
const securityView = ref('overview')
const passwordForm = ref({
	oldPassword: '',
	newPassword: '',
	confirmPassword: ''
})
const passwordFields = [
	{ name: 'oldPassword', label: '原密码', placeholder: '请输入原密码', password: true, maxlength: 20 },
	{ name: 'newPassword', label: '新密码', placeholder: '请输入新密码（至少 6 位）', password: true, maxlength: 20 },
	{ name: 'confirmPassword', label: '确认新密码', placeholder: '请再次输入新密码', password: true, maxlength: 20 }
]
const passwordRules = {
	oldPassword: {
		rules: [{
			required: true,
			errorMessage: '请输入原密码'
		}]
	},
	newPassword: {
		rules: [{
				required: true,
				errorMessage: '请输入新密码'
			},
			{
				minLength: 6,
				errorMessage: '新密码至少 6 位'
			},
			{
				validateFunction: (rule, value, data, callback) => {
					if (value && value === data.oldPassword) {
						callback('新密码不能与原密码相同')
					}
					return true
				}
			}
		]
	},
	confirmPassword: {
		rules: [{
				required: true,
				errorMessage: '请再次输入新密码'
			},
			{
				validateFunction: (rule, value, data, callback) => {
					if (value !== data.newPassword) {
						callback('两次输入的新密码不一致')
					}
					return true
				}
			}
		]
	}
}
const submittingPassword = ref(false)

function openAccountSecurity() {
	if (!token) {
		uni.navigateTo({
			url: '/pages/system/login/login'
		})
		return
	}
	securityView.value = 'overview'
	securityPopup.value?.open()
}

function closeSecurityDrawer() {
	securityPopup.value?.close()
}

function onSecurityPopupChange(e) {
	securityDrawerOpen.value = !!e.show
	if (!e.show) {
		securityView.value = 'overview'
		passwordForm.value = {
			oldPassword: '',
			newPassword: '',
			confirmPassword: ''
		}
	}
}

async function submitPasswordChange() {
	if (submittingPassword.value) return
	const { oldPassword, newPassword } = passwordForm.value

	submittingPassword.value = true
	try {
		const res = await apiUpdatePassword({
			oldPassword,
			password: newPassword
		})
		if (res.code === 200) {
			uni.showToast({ title: '密码修改成功', icon: 'success' })
			setTimeout(() => {
				userStore.clear()
				uni.clearStorageSync()
				uni.reLaunch({
					url: '/pages/system/login/login'
				})
			}, 1200)
		}
	} catch (e) {
		uni.showToast({ title: e?.message || '修改失败', icon: 'none' })
	} finally {
		submittingPassword.value = false
	}
}

function onOutLogin() {
	closeSecurityDrawer()
	setTimeout(() => {
		logoutPopup.value?.open()
	}, 320)
}

async function confirmLogout() {
	await apiUserLogout({
		refreshToken: uni.getStorageSync('refreshToken')
	})
	userStore.clear()
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
}

// 用户信息
.user-info {
	background: linear-gradient(135deg, $brand-primary-soft 0%, $brand-primary-fade 100%);
	border: 1rpx solid $border-base;
	border-radius: $radius-md;
	padding: 40rpx 32rpx;
	margin-bottom: 24rpx;
	display: flex;
	flex-direction: column;
	position: relative;
	overflow: hidden;
	box-shadow: $shadow-card;

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
			background: $bg-card;
			border: 4rpx solid $bg-card;
		}

		.user-detail {
			flex: 1;

			.name-row {
				display: flex;
				align-items: center;
				gap: 20rpx;
				margin-bottom: 12rpx;

				.name {
					font-size: 36rpx;
					font-weight: 600;
					color: $text-primary;
					letter-spacing: 1rpx;
				}

			}

			.student-id {
				font-size: 26rpx;
				color: $text-secondary;
				display: block;
			}
		}
	}
}

// 快捷入口
.quick-section {
	background: $bg-card;
	border: 1rpx solid $border-base;
	border-radius: $radius-md;
	padding: 32rpx 24rpx;
	margin-bottom: 24rpx;
	box-shadow: $shadow-card;

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
				border-radius: $radius-md;
				background: $brand-primary-soft;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 16rpx;
			}

			.quick-label {
				font-size: 26rpx;
				color: $text-secondary;
				font-weight: 500;
				line-height: 1.4;
			}
		}
	}
}

// 区块标题
.section-title {
	display: block;
	font-size: 30rpx;
	font-weight: 600;
	color: $text-primary;
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
		height: 24rpx;
		background: $brand-primary;
		border-radius: 3rpx;
	}
}

// 我的服务
.services-section {
	background: $bg-card;
	border: 1rpx solid $border-base;
	border-radius: $radius-md;
	padding: 32rpx 24rpx;
	box-shadow: $shadow-card;

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
				border-radius: $radius-sm;
				background: $brand-primary-soft;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 16rpx;
			}

			.service-label {
				font-size: 26rpx;
				color: $text-secondary;
				text-align: center;
				line-height: 1.4;
				font-weight: 500;
			}
		}
	}
}

// 账户安全抽屉
.security-drawer {
	width: 84vw;
	height: 100vh;
	background: $bg-page;
	display: flex;
	flex-direction: column;
	box-sizing: border-box;
	overflow: hidden;

	.drawer-header {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		padding: 40rpx 32rpx 28rpx;
		background: linear-gradient(135deg, $brand-primary-soft 0%, $brand-primary-fade 100%);
		border-bottom: 1rpx solid $border-base;

		.drawer-heading {
			display: flex;
			flex-direction: column;
			gap: 8rpx;

			.drawer-title {
				font-size: 36rpx;
				font-weight: 600;
				color: $text-primary;
				letter-spacing: 1rpx;
			}

			.drawer-subtitle {
				font-size: 24rpx;
				color: $text-secondary;
			}
		}

		.drawer-close {
			width: 60rpx;
			height: 60rpx;
			border-radius: 50%;
			background: rgba(255, 255, 255, 0.72);
			display: flex;
			align-items: center;
			justify-content: center;

			&:active {
				background: $bg-hover;
			}
		}
	}

	.drawer-body {
		flex: 1;
		height: 0;
		padding: 32rpx 28rpx calc(40rpx + env(safe-area-inset-bottom));
		box-sizing: border-box;
	}

	.drawer-footer {
		flex-shrink: 0;
		padding: 8rpx 28rpx calc(32rpx + env(safe-area-inset-bottom));

		.logout-btn {
			height: 88rpx;
			background: $bg-card;
			border: 1rpx solid $border-base;
			border-radius: $radius-pill;
			display: flex;
			align-items: center;
			justify-content: center;
			box-shadow: $shadow-card;

			&:active {
				background: $bg-subtle;
			}

			.logout-text {
				font-size: 28rpx;
				font-weight: 500;
				color: $text-secondary;
				letter-spacing: 0.5rpx;
			}
		}
	}

	.drawer-section-title {
		display: block;
		font-size: 26rpx;
		font-weight: 600;
		color: $text-tertiary;
		margin: 32rpx 0 16rpx 8rpx;
		letter-spacing: 2rpx;
	}

	.security-status {
		display: flex;
		align-items: center;
		gap: 20rpx;
		padding: 28rpx 24rpx;
		background: $bg-card;
		border: 1rpx solid $border-base;
		border-radius: $radius-md;
		box-shadow: $shadow-card;

		.status-icon {
			width: 84rpx;
			height: 84rpx;
			flex-shrink: 0;
			border-radius: 50%;
			background: $brand-primary-soft;
			display: flex;
			align-items: center;
			justify-content: center;
		}

		.status-info {
			display: flex;
			flex-direction: column;
			gap: 8rpx;
			min-width: 0;

			.status-title {
				font-size: 30rpx;
				font-weight: 600;
				color: $text-primary;
			}

			.status-desc {
				font-size: 24rpx;
				color: $text-secondary;
				line-height: 1.5;
			}
		}
	}

	.setting-list {
		background: $bg-card;
		border: 1rpx solid $border-base;
		border-radius: $radius-md;
		box-shadow: $shadow-card;
		overflow: hidden;

		.setting-item {
			display: flex;
			align-items: center;
			gap: 20rpx;
			padding: 26rpx 24rpx;
			position: relative;

			& + .setting-item::before {
				content: '';
				position: absolute;
				top: 0;
				left: 24rpx;
				right: 24rpx;
				height: 1rpx;
				background: $border-base;
			}

			&:active {
				background: $bg-subtle;
			}

			.setting-icon {
				width: 64rpx;
				height: 64rpx;
				flex-shrink: 0;
				border-radius: $radius-sm;
				background: $brand-primary-soft;
				display: flex;
				align-items: center;
				justify-content: center;
			}

			.setting-main {
				flex: 1;
				min-width: 0;
				display: flex;
				flex-direction: column;
				gap: 6rpx;

				.setting-label {
					font-size: 28rpx;
					color: $text-primary;
					font-weight: 500;
				}

				.setting-value {
					font-size: 24rpx;
					color: $text-tertiary;
					overflow: hidden;
					text-overflow: ellipsis;
					white-space: nowrap;
				}
			}

			.setting-action {
				font-size: 26rpx;
				color: $brand-primary-deep;
				font-weight: 500;
			}
		}
	}

	.drawer-tip {
		display: block;
		margin-top: 32rpx;
		padding: 0 8rpx;
		font-size: 22rpx;
		color: $text-tertiary;
		line-height: 1.7;
	}

	.form-back {
		display: flex;
		align-items: center;
		gap: 8rpx;
		padding: 4rpx 8rpx 24rpx;

		.form-back-text {
			font-size: 24rpx;
			color: $text-secondary;
		}
	}

	.form-hint {
		display: block;
		margin: 4rpx 8rpx 0;
		font-size: 22rpx;
		color: $text-tertiary;
		line-height: 1.7;
	}
}
</style>