<template>
	<view class="login-container">
		<view class="login-header">
			<text class="title">欢迎回来</text>
			<text class="subtitle">登录您的账号</text>
		</view>

		<view class="login-form">
			<uni-forms ref="form" :rules="rules" :modelValue="formData" label-position="top">
				<uni-forms-item label="账号" name="username" required>
					<input class="input" type="text" v-model="formData.username" placeholder="请输入账号" maxlength="20"
						@input="onInput('username', $event)" />
				</uni-forms-item>

				<uni-forms-item label="密码" name="password" required>
					<input class="input" password  v-model="formData.password" placeholder="请输入密码" maxlength="20"
						@input="onInput('password', $event)" />
				</uni-forms-item>
			</uni-forms>

			<button class="login-btn" @click="handleLogin">登录</button>

			<view class="link-section">
				<text class="link-text" @click="goToRegister">还没有账号？立即注册</text>
			</view>
		</view>
	</view>
</template>

<script setup>
	import {
		ref,
		reactive
	} from 'vue'
	import {
		apiUserLogin
	} from '@/api/user/index.js'
	import { useUserStore } from '@/stores/user.js'

	const userStore = useUserStore()

	const form = ref(null)
	const formData = reactive({
		username: '',
		password: ''
	})

	const rules = {
		username: {
			rules: [{
				required: true,
				errorMessage: '请输入账号'
			}]
		},
		password: {
			rules: [{
					required: true,
					errorMessage: '请输入密码'
				},
				{
					minLength: 6,
					errorMessage: '密码至少6位'
				}
			]
		}
	}

	const onInput = (name, e) => {
		const value = e.detail ? e.detail.value : e.target.value
		formData[name] = value
		if (form.value) {
			form.value.setValue(name, value)
		}
	}

	const handleLogin = async () => {

		await form.value.validate()

		let res = await apiUserLogin(formData)

		if (res.code === 200) {
			await handleLoginSuccess(res.data.accessToken, res.data.refreshToken)
		}

	}

	const handleLoginSuccess = async (token, refreshToken) => {
		uni.setStorageSync('token', token)
		uni.setStorageSync('refreshToken', refreshToken)

		try {
			await userStore.fetchMe()
		} catch (e) {
			uni.showToast({
				title: '获取用户信息失败',
				icon: 'none'
			})
			return
		}

		uni.showToast({
			title: '登录成功',
			icon: 'success'
		})
		uni.reLaunch({
			url: '/pages/index/index'
		})
	}

	const goToRegister = () => {
		uni.navigateTo({
			url: '/pages/system/registration/registration'
		})
	}
</script>

<style lang="scss" scoped>
	.login-container {
		min-height: 100vh;
		background: $bg-page;
		padding: 80rpx 60rpx;
		display: flex;
		flex-direction: column;
	}

	.login-header {
		text-align: center;
		margin-top: 80rpx;
		margin-bottom: 80rpx;

		.title {
			display: block;
			font-size: 52rpx;
			font-weight: 600;
			color: $text-primary;
			margin-bottom: 16rpx;
		}

		.subtitle {
			display: block;
			font-size: 26rpx;
			color: $text-secondary;
		}
	}

	.login-form {
		background: $bg-card;
		border: 1rpx solid $border-base;
		border-radius: $radius-md;
		padding: 56rpx 40rpx;
		box-shadow: $shadow-card;
	}

	.input {
		width: 100%;
		height: 88rpx;
		background: $bg-subtle;
		border-radius: $radius-sm;
		padding: 0 24rpx;
		font-size: 28rpx;
		color: $text-primary;
		box-sizing: border-box;
		border: 2rpx solid transparent;

		&::placeholder {
			color: $text-tertiary;
		}
	}

	.login-btn {
		width: 100%;
		height: 88rpx;
		background: $brand-primary;
		border-radius: $radius-pill;
		color: $text-on-primary;
		font-size: 30rpx;
		font-weight: 500;
		margin-top: 40rpx;
		border: none;
		display: flex;
		align-items: center;
		justify-content: center;

		&::after {
			border: none;
		}

		&:active {
			background: $brand-primary-deep;
		}
	}

	.link-section {
		text-align: center;
		margin-top: 40rpx;

		.link-text {
			font-size: 26rpx;
			color: $brand-primary-ink;
		}
	}
</style>