<template>
	<view class="registration-container">
		<view class="registration-header">
			<text class="title">创建账号</text>
			<text class="subtitle">注册新用户</text>
		</view>

		<com-base-form :model="formData" :fields="fields" :rules="rules" submit-text="注册" @submit="handleRegister">
			<view class="link-section">
				<text class="link-text" @click="()=>uni.redirectTo({
			url:'/pages/system/login/login'
		})">已有账号？立即登录</text>
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
		apiUserRegistration
	} from '@/api/user/index.js'

	const formData = reactive({
		username: '',
		password: '',
		confirmPassword: ''
	})

	const fields = [
		{ name: 'username', label: '账号', placeholder: '请输入账号', maxlength: 20 },
		{ name: 'password', label: '密码', placeholder: '请输入密码（至少6位）', password: true, maxlength: 20 },
		{ name: 'confirmPassword', label: '确认密码', placeholder: '请再次输入密码', password: true, maxlength: 20 }
	]

	const rules = {
		username: {
			rules: [{
					required: true,
					errorMessage: '请输入账号'
				},
				{
					minLength: 3,
					errorMessage: '账号至少3位'
				}
			]
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
		},
		confirmPassword: {
			rules: [{
					required: true,
					errorMessage: '请再次输入密码'
				},
				{
					validateFunction: (rule, value, data, callback) => {
						if (value !== data.password) {
							callback('两次密码不一致')
						}
						return true
					}
				}
			]
		}
	}

	const handleRegister = async () => {
		try {
			let res = await apiUserRegistration(formData)

			if (res.code === 200) {
				uni.showToast({
					title: '注册成功',
					icon: 'success'
				})

				// 注册成功后跳转到登录页
				setTimeout(() => {
					uni.redirectTo({
						url: '/pages/system/login/login'
					})
				}, 1500)
			}
		} catch (e) {}
	}
</script>

<style lang="scss" scoped>
	.registration-container {
		min-height: 100vh;
		background: $bg-page;
		padding: 80rpx 60rpx;
		display: flex;
		flex-direction: column;
	}

	.registration-header {
		text-align: center;
		margin: 80rpx 0;

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
