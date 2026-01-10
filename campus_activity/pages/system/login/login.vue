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
			
			<!-- 微信登录按钮 -->
			<view class="wx-login-section">
				<button class="wx-login-btn" @click="handleWxLogin">
					<text>微信一键登录</text>
				</button>
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
		apiUserLogin,
		apiUserWxLogin
	} from '@/api/user/index.js'

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
			handleLoginSuccess(res.data.user)
		}

	}
	
	const handleWxLogin = () => {
		uni.login({
			provider: 'weixin',
			success: async (loginRes) => {
				if (loginRes.code) {
					try {
						let res = await apiUserWxLogin({
							code: loginRes.code
						})
						if (res.code === 200) {
							handleLoginSuccess(res.data.user)
						}
					} catch (e) {
						uni.showToast({
							title: '微信登录失败',
							icon: 'none'
						})
					}
				}
			}
		})
	}
	
	const handleLoginSuccess = (user) => {
		const token = user.token
		
		if (user.isCompleted) {
			uni.setStorageSync('token', token)
			uni.setStorageSync('userInfo', user)
			uni.showToast({
				title: '登录成功',
				icon: 'success'
			})
			uni.reLaunch({
				url: '/pages/index/index'
			})
		} else {
			// 保存token以便后续请求使用
			uni.setStorageSync('token', token)
			uni.navigateTo({
				url: `/pages/system/userInfo/userInfo?id=${user.id}`,
				success() {
					uni.showToast({
						title: '请先完善个人信息',
						icon: 'none'
					})
				}
			})
		}
	}

	const goToRegister = () => {
		uni.navigateTo({
			url: '/pages/system/registration/registration'
		})
	}
</script>

<style lang="scss" scoped>
	.login-container {
		height: 100vh;
		background: linear-gradient(180deg, #e6f4ff 0%, #f0f8ff 100%);
		padding: 80rpx 60rpx;
		display: flex;
		flex-direction: column;
	}

	.login-header {
		text-align: center;
		margin-top: 100rpx;
		margin-bottom: 100rpx;

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

	.login-form {
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

	.login-btn {
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
	
	.wx-login-section {
		margin-top: 60rpx;
		display: flex;
		justify-content: center;
		
		.wx-login-btn {
			background-color: #07c160;
			color: #fff;
			font-size: 30rpx;
			border-radius: 44rpx;
			padding: 0 60rpx;
			height: 80rpx;
			line-height: 80rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			border: none;
			
			&::after {
				border: none;
			}
			
			&:active {
				opacity: 0.9;
			}
		}
	}
</style>