<template>
	<view class="registration-container">
		<view class="registration-header">
			<text class="title">创建账号</text>
			<text class="subtitle">注册新用户</text>
		</view>

		<view class="registration-form">
			<uni-forms ref="form" :rules="rules" :modelValue="formData" label-position="top">
				<uni-forms-item label="账号" name="username" required>
					<input class="input" type="text" v-model="formData.username" placeholder="请输入账号" maxlength="20"
						@input="onInput('username', $event)" />
				</uni-forms-item>

				<uni-forms-item label="密码" name="password" required>
					<input class="input" password v-model="formData.password" placeholder="请输入密码（至少6位）"
						maxlength="20" @input="onInput('password', $event)" />
				</uni-forms-item>

				<uni-forms-item label="确认密码" name="confirmPassword" required>
					<input class="input" password v-model="formData.confirmPassword" placeholder="请再次输入密码"
						maxlength="20" @input="onInput('confirmPassword', $event)" />
				</uni-forms-item>
			</uni-forms>

			<button class="register-btn" @click="handleRegister">注册</button>

			<view class="link-section">
				<text class="link-text" @click="()=>uni.redirectTo({
			url:'/pages/system/login/login'
		})">已有账号？立即登录</text>
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
		apiUserRegistration
	} from '@/api/user/index.js'

	const form = ref(null)
	const formData = reactive({
		username: '',
		password: '',
		confirmPassword: ''
	})

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
						if (value !== formData.password) {
							callback('两次密码不一致')
						}
						return true
					}
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

	const handleRegister = async () => {
		try {
			await form.value.validate()

			let res = await apiUserRegistration(formData)

			if (res.code === 200) {
				uni.showToast({
					title: '注册成功',
					icon: 'success'
				})

				// 注册成功后跳转到个人信息完善页面
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

	.registration-form {
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

	.register-btn {
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