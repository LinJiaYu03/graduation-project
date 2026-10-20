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
		background: linear-gradient(180deg, #e6f4ff 0%, #f0f8ff 100%);
		padding: 80rpx 60rpx;
		display: flex;
		flex-direction: column;
	}

	.registration-header {
		text-align: center;
		margin: 100rpx 0;

		.title {
			display: block;
			font-size: 56rpx;
			font-weight: bold;
			color: #1890ff;
			margin-bottom: 20rpx;
		}

		.subtitle {
			display: block;
			font-size: 28rpx;
			color: #409eff;
		}
	}

	.registration-form {
		background: #ffffff;
		border-radius: 16rpx;
		padding: 60rpx 40rpx;
		box-shadow: 0 4rpx 20rpx rgba(24, 144, 255, 0.15);
	}

	.input {
		width: 100%;
		height: 88rpx;
		background: #fafafa;
		border-radius: 8rpx;
		padding: 0 24rpx;
		font-size: 28rpx;
		color: #333333;
		box-sizing: border-box;
		border: 1rpx solid #d9ecff;

		&::placeholder {
			color: #999999;
		}
	}

	.register-btn {
		width: 100%;
		height: 88rpx;
		background: #1890ff;
		border-radius: 8rpx;
		color: #ffffff;
		font-size: 32rpx;
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
			opacity: 0.8;
			background: #40a9ff;
		}
	}

	.link-section {
		text-align: center;
		margin-top: 40rpx;

		.link-text {
			font-size: 26rpx;
			color: #1890ff;
		}
	}
</style>