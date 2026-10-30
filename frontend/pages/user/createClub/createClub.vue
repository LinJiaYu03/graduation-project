<template>
	<view class="create-club container">
		<view class="form-container">
			<uni-forms ref="formRef" :modelValue="form" :rules="rules" label-position="top" label-width="120"
				validate-trigger="bind">
				<!-- 图片上传 -->
				<uni-forms-item label="社团图标" name="iconUrl" required>
					<uni-file-picker v-model="form.iconUrl" fileMediatype="image" limit="1" :auto-upload="false"
						mode="grid" title="上传图标" @select="select" />
				</uni-forms-item>

				<!-- 社团名称 -->
				<uni-forms-item label="社团名称" name="name" required>
					<input class="input" type="text" v-model="form.name" placeholder="请输入社团名称" maxlength="50" />
				</uni-forms-item>

				<!-- 社团简介 -->
				<uni-forms-item label="社团简介" name="description" required>
					<textarea class="textarea" v-model="form.description" placeholder="请输入社团简介" maxlength="500"
						:auto-height="true" />
					<view class="char-count">{{ form.description.length }}/500</view>
				</uni-forms-item>

			</uni-forms>

			<!-- 提交按钮 -->
			<button class="submit-btn" @click="handleSubmit">提交</button>
		</view>
	</view>
</template>

<script setup>
	import {
		ref,
		reactive
	} from 'vue'
	import convertCloudPath from '@/utils/convertCloudPath'
	import {
		apiCreateClub
	} from '@/api/club/index.js'

	const formRef = ref(null)
	const form = reactive({
		iconUrl: [],
		name: '',
		description: ''
	})
	const coverImageUrl = ref('')
	const filesName = ref('')
	const filePath = ref('')

	// 表单验证规则
	const rules = {
		iconUrl: {
			required: true,
			errorMessage: '请上传封面图片',
			validator: (rule, value, callback) => {
				if (!Array.isArray(value) || value.length < 1) {
					callback('请至少上传1张封面图片')
					return
				}
				callback()
			}
		},
		name: {
			required: true,
			errorMessage: '请输入活动名称'
		},
		description: {
			required: true,
			errorMessage: '请输入活动简介',
			validator: (rule, value, callback) => {
				if (!value || value.trim().length === 0) {
					callback('请输入活动简介')
					return
				}
				if (value.length < 10) {
					callback('活动简介至少需要10个字符')
					return
				}
				callback()
			}
		}
	}

	//
	function select(e) {
		coverImageUrl.value = e.tempFilePaths[0]
		filesName.value = e.tempFiles[0].name
	}

	// 提交表单
	async function handleSubmit() {
		formRef.value
			.validate()
			.then(async () => {
				uni.showLoading({
					title: '提交中...'
				})

				try {
					// 如果有图片，先上传图片
					if (coverImageUrl.value) {
						await new Promise((resolve, reject) => {
							uniCloud.uploadFile({
								filePath: coverImageUrl.value,
								cloudPath: `club/${new Date().getTime()}_${filesName.value}`,
								fileType: 'image',
								success: (e) => {
									filePath.value = convertCloudPath(e.fileID)
									resolve()
								},
							})
						})
					}

					// 构建提交数据
					const formData = {
						name: form.name,
						description: form.description || undefined
					}

					// 如果有上传的图片，添加 iconUrl
					if (filePath.value) {
						formData.iconUrl = filePath.value
					}

					// 调用 API 创建社团
					const res = await apiCreateClub(formData)
					uni.hideLoading()

					if (res.code === 200) {
						uni.showToast({
							title: '创建成功',
							icon: 'success'
						})

						// 延迟返回上一页
						setTimeout(() => {
							uni.reLaunch({
								url:'/pages/user/user'
							})
						}, 1500)
					} else {
						uni.showToast({
							title: res.message || '创建失败',
							icon: 'none'
						})
					}
				} catch (e) {
					uni.hideLoading()
					uni.showToast({
						title: '创建失败',
						icon: 'none'
					})
					console.error('创建社团失败', e)
				}
			})
			.catch((err) => {
				console.warn('表单校验未通过', err)
			})
	}
</script>

<style lang="scss" scoped>
	$primary-color: $brand-primary;
	$bg-color: $bg-page;
	$border-color: $border-base;
	$white: #FFFFFF;

	.create-club {
		background: $bg-color;
		min-height: 100vh;
		padding: 0;
	}

	.form-container {
		background: $white;
		border-radius: $radius-md;
		margin: 24rpx;
		padding: 40rpx 32rpx;
		box-shadow: $shadow-card;
		border: 1rpx solid $border-color;
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

	.textarea {
		width: 100%;
		min-height: 200rpx;
		background: $bg-subtle;
		border-radius: $radius-sm;
		padding: 20rpx 24rpx;
		font-size: 28rpx;
		color: $text-primary;
		box-sizing: border-box;
		border: 2rpx solid transparent;
		line-height: 1.6;

		&::placeholder {
			color: $text-tertiary;
		}
	}

	.char-count {
		margin-top: 12rpx;
		text-align: right;
		font-size: 24rpx;
		color: $text-tertiary;
	}

	.submit-btn {
		margin-top: 60rpx;
		width: 100%;
		height: 96rpx;
		background: $brand-primary;
		border: none;
		border-radius: $radius-pill;
		font-size: 32rpx;
		font-weight: 500;
		color: $text-on-primary;
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

	// uni-forms 样式覆盖
	:deep(.uni-forms-item) {
		margin-bottom: 40rpx;
	}

	:deep(.uni-forms-item__label) {
		font-size: 28rpx;
		font-weight: 500;
		color: $text-primary;
		margin-bottom: 16rpx;
	}
</style>