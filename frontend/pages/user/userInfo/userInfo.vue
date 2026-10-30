<template>
	<view class="page container">
		<!-- 信息列表 -->
		<uni-list class="info-card avatar-card">
			<uni-list-item title="头像" clickable class="info-item" @click="openAvatarPreview">
				<template #footer>
					<view class="avatar-preview">
						<image :src="userAvatar || '/static/logo.png'" mode="aspectFill" class="avatar-img" />
					</view>
				</template>
			</uni-list-item>
			<uni-list-item title="姓名" clickable :right-text="userInfo.realName" class="info-item" @click="editField('realName', '姓名', userInfo.realName)" />
			<uni-list-item title="性别" clickable :right-text="userInfo.gender===1?'男':'女'" class="info-item" @click="editGender" />
		</uni-list>

		<uni-list class="info-card contact-card">
			<uni-list-item title="手机号" clickable :right-text="userInfo.phone" class="info-item" @click="editField('phone', '手机号', userInfo.phone)" />
			<uni-list-item title="邮箱" clickable :right-text="userInfo.email" class="info-item" @click="editField('email', '邮箱', userInfo.email)" />
		</uni-list>

		<!-- 优化后的保存按钮 -->
		<view class="save-button-container">
			<button class="save-btn" @click="saveChanges">
				<text class="btn-text">保存修改</text>
			</button>
		</view>

		<!-- 头像预览 -->
		<view v-if="showAvatarPreview" class="avatar-preview-mask" @click="closeAvatarPreview">
			<image :src="userAvatar || '/static/logo.png'" mode="aspectFit" class="avatar-preview-img" />
			<button class="avatar-change-btn" @click.stop="upload">
				<text class="btn-text">更换头像</text>
			</button>
		</view>

	</view>
</template>

<script setup>
	import {
		ref
	} from 'vue'
	import convertCloudPath from '@/utils/convertCloudPath'
	import {
		apiImproveUserInfo
	} from '@/api/user/index.js'
	import { useUserStore } from '@/stores/user.js'

	const userStore = useUserStore()
	const userInfo = ref({ ...(userStore.user || {}) })
	const userAvatar = ref(userInfo.value.avatarUrl)
	const filesName = ref()
	const showAvatarPreview = ref(false)

	// 打开头像预览
	function openAvatarPreview() {
		showAvatarPreview.value = true
	}

	// 关闭头像预览
	function closeAvatarPreview() {
		showAvatarPreview.value = false
	}

	function upload() {
		uni.chooseImage({
			count: 1,
			success(e) {
				userAvatar.value = e.tempFilePaths[0]
				showAvatarPreview.value = false
				// 某些情况下可能没有 name 属性，使用时间戳或文件名
				filesName.value = e.tempFiles[0]?.name || e.tempFilePaths[0].split('/').pop() || 'avatar.jpg'
			}
		})
	}

	// 编辑文本字段（姓名、手机号、邮箱、密码）
	function editField(field, label, currentValue, isPassword = false) {
		uni.showModal({
			title: `编辑${label}`,
			editable: true,
			placeholderText: `请输入${label}`,
			content: currentValue,
			success: (res) => {
				if (res.confirm && res.content !== undefined) {
					const newValue = res.content.trim()
					
					// 验证手机号
					if (field === 'phone' && newValue && !/^1[3-9]\d{9}$/.test(newValue)) {
						uni.showToast({
							title: '手机号格式不正确',
							icon: 'none'
						})
						return
					}
					
					// 验证邮箱
					if (field === 'email' && newValue && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newValue)) {
						uni.showToast({
							title: '邮箱格式不正确',
							icon: 'none'
						})
						return
					}
					
					// 验证姓名
					if (field === 'realName' && !newValue) {
						uni.showToast({
							title: '姓名不能为空',
							icon: 'none'
						})
						return
					}
					
					userInfo.value[field] = newValue
				}
			}
		})
	}

	// 编辑性别
	function editGender() {
		uni.showActionSheet({
			itemList: ['男', '女'],
			success: (res) => {
				userInfo.value.gender = res.tapIndex === 0 ? 1 : 0
			}
		})
	}


	async function saveChanges() {
		// 验证必填字段
		if (!userInfo.value.realName) {
			uni.showToast({
				title: '请输入姓名',
				icon: 'none'
			})
			return
		}

		uni.showLoading({
			title: '保存中...'
		})

		try {
			// 检查是否选择了新头像（本地临时路径 vs 远程URL）
			const isNewAvatar = userAvatar.value && (userAvatar.value.startsWith('http://tmp') || userAvatar.value.startsWith('wxfile://'))

			if (isNewAvatar && filesName.value) {
				await new Promise((resolve, reject) => {
					uniCloud.uploadFile({
						filePath: userAvatar.value,
						cloudPath: `avatar/${new Date().getTime()}_${filesName.value}`,
						fileType: 'image',
						success: (e) => {
							let filePath = convertCloudPath(e.fileID)
							userInfo.value.avatarUrl = filePath
							resolve()
						},
						fail: (err) => reject(err)
					})
				})
			}

			// 保存用户信息
			let res = await apiImproveUserInfo(userInfo.value)
			
			uni.hideLoading()
			
			if (res.code === 200) {
				try {
					await userStore.fetchMe()
				} catch (e) {}
				uni.showToast({
					title: '保存成功',
					icon: 'success'
				})
				setTimeout(() => {
					uni.reLaunch({
						url: '/pages/user/user'
					})
				}, 1500)
			} else {
				uni.showToast({
					title: res.message || '保存失败',
					icon: 'none'
				})
			}
		} catch (e) {
			uni.hideLoading()
			const errorMsg = e.message || e.errMsg || '保存失败'
			uni.showToast({
				title: errorMsg,
				icon: 'none'
			})
			console.error('保存失败', e)
		}
	}
</script>

<style lang="scss" scoped>
	// 主色别名（引用全局设计令牌）
	$primary-color: $brand-primary;
	$primary-light: $brand-primary-soft;
	$primary-dark: $brand-primary-deep;
	$bg-color: $bg-page;
	$border-color: $border-base;
	$white: #FFFFFF;
	$shadow-light: rgba(122, 94, 45, 0.06);
	$shadow-medium: rgba(122, 94, 45, 0.10);

	.page {
		background-color: $bg-color;
		padding: 0;
	}

	// 头像列表项
	.avatar-card {
		margin-top: 24rpx;
	}

	.avatar-preview {
		width: 88rpx;
		height: 88rpx;
		border-radius: 50%;
		overflow: hidden;
		background: $bg-card;
		border: 1rpx solid $border-color;

		.avatar-img {
			width: 100%;
			height: 100%;
			display: block;
		}
	}

	// 头像预览
	.avatar-preview-mask {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(0, 0, 0, 0.75);
		z-index: 999;
	}

	.avatar-preview-img {
		width: 600rpx;
		height: 600rpx;
		border-radius: $radius-md;
		background: $bg-card;
	}

	.avatar-change-btn {
		position: absolute;
		left: 50%;
		bottom: 100rpx;
		transform: translateX(-50%);
		width: 480rpx;
		height: 88rpx;
		line-height: 88rpx;
		background: $brand-primary;
		border-radius: $radius-pill;
		color: $text-on-primary;
		font-size: 30rpx;
		text-align: center;

		&::after {
			border: none;
		}

		&:active {
			background: $brand-primary-deep;
		}

		.btn-text {
			letter-spacing: 2rpx;
		}
	}

	// 信息卡片
	.info-card {
		background: $bg-card;
		border-radius: $radius-md;
		overflow: hidden;
		margin: 0 24rpx 24rpx;
		box-shadow: $shadow-card;
		border: 1rpx solid $border-color;

		:deep(.uni-list-item) {
			padding: 28rpx 32rpx;
			border-bottom: 1rpx solid $border-color;
			position: relative;
			background: $bg-card;

			&:last-child {
				border-bottom: none;
			}

			&:not(:last-child):after {
				content: '';
				position: absolute;
				left: 32rpx;
				right: 32rpx;
				bottom: 0;
				height: 1rpx;
				background: $border-color;
			}

			.uni-list-item__container {
				align-items: center;

				.uni-list-item__content {
					.uni-list-item__content-title {
						font-size: 30rpx;
						color: $text-primary;
						font-weight: 500;
						letter-spacing: 1rpx;
					}
				}

				.uni-list-item__extra {
					.uni-list-item__extra-text {
						font-size: 28rpx;
						color: $text-secondary;
						max-width: 400rpx;
						text-align: right;
						overflow: hidden;
						text-overflow: ellipsis;
						white-space: nowrap;
						font-weight: 400;
					}
				}
			}
		}
	}

	.contact-card {
		margin-bottom: 40rpx;
	}

	// 保存按钮容器
	.save-button-container {
		padding: 20rpx 24rpx 60rpx;
		background: linear-gradient(to top, $bg-page 70%, transparent);
		position: sticky;
		bottom: 0;
		z-index: 10;
	}

	// 保存按钮样式
	.save-btn {
		background: $brand-primary;
		border: none;
		border-radius: $radius-pill;
		height: 96rpx;
		line-height: 96rpx;
		font-size: 32rpx;
		font-weight: 500;
		color: $text-on-primary;
		display: flex;
		align-items: center;
		justify-content: center;

		&:active {
			background: $brand-primary-deep;
		}

		.btn-text {
			letter-spacing: 2rpx;
		}
	}
</style>