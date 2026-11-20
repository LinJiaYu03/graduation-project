<template>
	<view class="login-container">
		<view class="login-header">
			<text class="title">欢迎回来</text>
			<text class="subtitle">登录您的账号</text>
		</view>

		<com-base-form :model="formData" :fields="fields" :rules="rules" submit-text="登录" @submit="handleLogin">
			<view class="link-section">
				<text class="link-text" @click="goToRegister">还没有账号？立即注册</text>
			</view>
		</com-base-form>
	</view>
</template>

<script setup>
	import {
		reactive
	} from 'vue'
	import comBaseForm from '@/components/com-base-form/com-base-form.vue'
	import {
		apiUserLogin
	} from '@/api/user/index.js'
	import { useUserStore } from '@/stores/user.js'

	const userStore = useUserStore()

	const formData = reactive({
		username: '',
		password: ''
	})

	const fields = [
		{ name: 'username', label: '账号', placeholder: '请输入账号', maxlength: 20 },
		{ name: 'password', label: '密码', placeholder: '请输入密码', password: true, maxlength: 20 }
	]

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

	const handleLogin = async () => {
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

	.link-section {
		text-align: center;
		margin-top: 40rpx;

		.link-text {
			font-size: 26rpx;
			color: $brand-primary-ink;
		}
	}
</style>
