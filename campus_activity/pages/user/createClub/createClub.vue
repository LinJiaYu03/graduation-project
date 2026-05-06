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

				<!-- 社团标签 -->
				<uni-forms-item label="社团级别" name="tags" required>
					<view class="tags-container">
						<uni-tag v-for="(tag, index) in levelTags" :key="index" :text="tag"
							:type="tag===form.levelTag? 'primary' : 'default'" :inverted="!(tag===form.levelTag)"
							@click="toggleLevelTag(tag)" class="tag-item" />
					</view>
					<view class="tip-text">请至少选择1个标签</view>
				</uni-forms-item>

				<!-- 社团标签 -->
				<uni-forms-item label="社团标签" name="tags" required>
					<view class="tags-container">
						<uni-tag v-for="(tag, index) in availableTags" :key="index" :text="tag"
							:type="isTagSelected(tag) ? 'primary' : 'default'" :inverted="!isTagSelected(tag)"
							@click="toggleTag(tag)" class="tag-item" />
					</view>
				</uni-forms-item>
			</uni-forms>

			<!-- 提交按钮 -->
			<button class="submit-btn" type="primary" @click="handleSubmit">提交</button>
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

	const levelTags = ['班级', '院级', '校级']
	// 可用的标签列表
	const availableTags = ['团支部', '音乐', '文艺', '传媒', '社团与协会', '公益志愿']
	const formRef = ref(null)
	const form = reactive({
		iconUrl: [],
		name: '',
		description: '',
		levelTag: '',
		tags: []
	})
	const coverImageUrl = ref('')
	const filesName = ref('')
	const filePath = ref('')

	// 判断标签是否被选中
	function isTagSelected(tagValue) {
		return form.tags.includes(tagValue)
	}

	// 切换标签选中状态
	function toggleTag(tagValue) {
		const index = form.tags.indexOf(tagValue)
		if (index > -1) {
			// 取消选中
			form.tags.splice(index, 1)
		} else {
			// 选中
			form.tags.push(tagValue)
		}
	}

	function toggleLevelTag(value) {
		form.levelTag = value
	}

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
		},
		tags: {
			required: true,
			errorMessage: '请至少选择1个标签',
			validator: (rule, value, callback) => {
				if (!Array.isArray(value) || value.length < 1) {
					callback('请至少选择1个标签')
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

					// 获取当前登录用户ID
					const userInfo = uni.getStorageSync('userInfo')

					// 构建提交数据
					const formData = {
						name: form.name,
						description: form.description || undefined,
						levelTag:form.levelTag,
						tags: form.tags.length > 0 ? form.tags.join(',') : undefined,
						userId: userInfo?.id
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
	$primary-color: #FCB857;
	$bg-color: #F8F9FA;
	$text-primary: #333333;
	$text-secondary: #666666;
	$text-light: #999999;
	$border-color: #F0F0F0;
	$white: #FFFFFF;

	.create-club {
		background: $bg-color;
		min-height: 100vh;
		padding: 0;
	}

	.form-container {
		background: $white;
		border-radius: 20rpx;
		margin: 30rpx;
		padding: 40rpx 32rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.04);
		border: 1rpx solid $border-color;
	}

	.input {
		width: 100%;
		height: 88rpx;
		background: #fafafa;
		border-radius: 8rpx;
		padding: 0 24rpx;
		font-size: 28rpx;
		color: $text-primary;
		box-sizing: border-box;
		border: 1rpx solid $border-color;
		transition: all 0.3s ease;

		&::placeholder {
			color: $text-light;
		}
	}

	.textarea {
		width: 100%;
		min-height: 200rpx;
		background: #fafafa;
		border-radius: 8rpx;
		padding: 20rpx 24rpx;
		font-size: 28rpx;
		color: $text-primary;
		box-sizing: border-box;
		border: 1rpx solid $border-color;
		line-height: 1.6;
		transition: all 0.3s ease;

		&::placeholder {
			color: $text-light;
		}
	}

	.char-count {
		margin-top: 12rpx;
		text-align: right;
		font-size: 24rpx;
		color: $text-light;
	}

	.tags-container {
		display: flex;
		flex-wrap: wrap;
		gap: 20rpx;
		margin-top: 12rpx;

		.tag-item {
			margin: 0;
			cursor: pointer;
			transition: all 0.3s ease;
		}
	}

	.tip-text {
		margin-top: 12rpx;
		font-size: 24rpx;
		color: $text-light;
		line-height: 1.5;
	}

	.submit-btn {
		margin-top: 60rpx;
		width: 100%;
		height: 100rpx;
		background: linear-gradient(135deg, $primary-color 0%, #E6A33D 100%);
		border: none;
		border-radius: 50rpx;
		font-size: 34rpx;
		font-weight: 600;
		color: $white;
		box-shadow: 0 8rpx 30rpx rgba(252, 184, 87, 0.3);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		display: flex;
		align-items: center;
		justify-content: center;

		&:active {
			transform: scale(0.98);
			opacity: 0.9;
		}
	}

	// uni-forms 样式覆盖
	:deep(.uni-forms-item) {
		margin-bottom: 40rpx;
	}

	:deep(.uni-forms-item__label) {
		font-size: 30rpx;
		font-weight: 500;
		color: $text-primary;
		margin-bottom: 16rpx;
	}
</style>