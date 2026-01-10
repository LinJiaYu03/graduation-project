<template>
	<view class="page container">
		<!-- 头像区域 -->
		<view class="avatar-section">
			<view class="avatar-wrapper">
				<image :src="userAvatar" mode="aspectFill" class="avatar" @click="upload" />
			</view>
		</view>

		<!-- 信息列表 -->
		<uni-list class="info-card">
			<uni-list-item title="姓名" clickable :right-text="userInfo.realName" class="info-item" @click="editField('realName', '姓名', userInfo.realName)" />
			<uni-list-item title="性别" clickable :right-text="userInfo.gender===1?'男':'女'" class="info-item" @click="editGender" />
			<view class="info-item-wrapper">
				<uni-list-item title="学校" :right-text="userInfo.schoolName" class="info-item" />
				<picker 
					mode="multiSelector" 
					:range="multiArray" 
					:value="multiIndex" 
					@change="onPickerChange"
					@columnchange="onPickerColumnChange"
					class="overlay-picker"
				>
					<view class="picker-overlay"></view>
				</picker>
			</view>
			<view class="info-item-wrapper">
				<uni-list-item title="学院" :right-text="userInfo.collegeName" class="info-item" />
				<picker 
					mode="multiSelector" 
					:range="multiArray" 
					:value="multiIndex" 
					@change="onPickerChange"
					@columnchange="onPickerColumnChange"
					class="overlay-picker"
				>
					<view class="picker-overlay"></view>
				</picker>
			</view>
			<view class="info-item-wrapper">
				<uni-list-item title="班级" :right-text="userInfo.className" class="info-item" />
				<picker 
					mode="multiSelector" 
					:range="multiArray" 
					:value="multiIndex" 
					@change="onPickerChange"
					@columnchange="onPickerColumnChange"
					class="overlay-picker"
				>
					<view class="picker-overlay"></view>
				</picker>
			</view>
		</uni-list>

		<uni-list class="info-card contact-card">
			<uni-list-item title="密码" clickable :right-text="userInfo.password ? '******' : ''" class="info-item" @click="editField('password', '密码', '', true)" />
			<uni-list-item title="手机号" clickable :right-text="userInfo.phone" class="info-item" @click="editField('phone', '手机号', userInfo.phone)" />
			<uni-list-item title="邮箱" clickable :right-text="userInfo.email" class="info-item" @click="editField('email', '邮箱', userInfo.email)" />
		</uni-list>

		<!-- 优化后的保存按钮 -->
		<view class="save-button-container">
			<button class="save-btn" @click="saveChanges">
				<text class="btn-text">保存修改</text>
			</button>
		</view>

	</view>
</template>

<script setup>
	import {
		ref,
		computed,
		onMounted
	} from 'vue'
	import convertCloudPath from '@/utils/convertCloudPath'
	import {
		apiImproveUserInfo
	} from '@/api/user/index.js'
	import {
		apiGetSchoolInfoTree
	} from '@/api/school/index.js'

	const userInfo = ref(uni.getStorageSync('userInfo'))
	const userAvatar = ref(userInfo.value.avatarUrl)
	const filesName = ref()
	const schoolData = ref([])
	const multiIndex = ref([0, 0, 0])

	// 构建三级联动的数组
	const multiArray = computed(() => {
		if (!schoolData.value || schoolData.value.length === 0) {
			return [[], [], []]
		}
		const schools = schoolData.value.map(item => item.name)
		const colleges = (schoolData.value[multiIndex.value[0]]?.colleges || []).map(item => item.name)
		const classes = (schoolData.value[multiIndex.value[0]]?.colleges?.[multiIndex.value[1]]?.classes || []).map(item => item.name)
		return [schools, colleges, classes]
	})

	// 初始化学校信息索引
	const initMultiIndex = () => {
		if (userInfo.value.schoolName && userInfo.value.collegeName && userInfo.value.className && schoolData.value.length > 0) {
			const schoolIndex = schoolData.value.findIndex(school => school.name === userInfo.value.schoolName)
			if (schoolIndex !== -1) {
				const colleges = schoolData.value[schoolIndex].colleges || []
				const collegeIndex = colleges.findIndex(college => college.name === userInfo.value.collegeName)
				if (collegeIndex !== -1) {
					const classes = colleges[collegeIndex].classes || []
					const classIndex = classes.findIndex(cls => cls.name === userInfo.value.className)
					if (classIndex !== -1) {
						multiIndex.value = [schoolIndex, collegeIndex, classIndex]
						return
					}
				}
			}
		}
		multiIndex.value = [0, 0, 0]
	}

	// 获取学校信息树
	async function getSchoolInfoTree() {
		try {
			let res = await apiGetSchoolInfoTree()
			schoolData.value = res.data.items || []
			initMultiIndex()
		} catch (e) {
			console.error('获取学校信息失败', e)
		}
	}

	onMounted(() => {
		getSchoolInfoTree()
	})

	function upload() {
		uni.chooseImage({
			count: 1,
			success(e) {
				userAvatar.value = e.tempFilePaths[0]
				filesName.value = e.tempFiles[0].name
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
					uni.showToast({
						title: '修改成功',
						icon: 'success'
					})
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
				uni.showToast({
					title: '修改成功',
					icon: 'success'
				})
			}
		})
	}


	// picker 选择变化
	function onPickerChange(e) {
		const values = e.detail.value
		multiIndex.value = values

		const schoolIndex = values[0]
		const collegeIndex = values[1]
		const classIndex = values[2]

		const school = schoolData.value[schoolIndex]
		if (school) {
			userInfo.value.schoolName = school.name
			const college = (school.colleges || [])[collegeIndex]
			if (college) {
				userInfo.value.collegeName = college.name
				const cls = (college.classes || [])[classIndex]
				if (cls) {
					userInfo.value.className = cls.name
				} else {
					userInfo.value.className = ''
				}
			} else {
				userInfo.value.collegeName = ''
				userInfo.value.className = ''
			}
		}
		uni.showToast({
			title: '修改成功',
			icon: 'success'
		})
	}

	// picker 列变化（联动处理）
	function onPickerColumnChange(e) {
		const column = e.detail.column
		const value = e.detail.value

		// 更新当前列的索引
		const newIndex = [...multiIndex.value]
		newIndex[column] = value

		// 如果改变了学校，重置学院和班级
		if (column === 0) {
			newIndex[1] = 0
			newIndex[2] = 0
		}
		// 如果改变了学院，重置班级
		else if (column === 1) {
			newIndex[2] = 0
		}

		// 避免越界
		const schools = schoolData.value || []
		if (!schools[newIndex[0]] || !(schools[newIndex[0]].colleges || []).length) {
			newIndex[1] = 0
			newIndex[2] = 0
		} else {
			const colleges = schools[newIndex[0]].colleges || []
			if (!colleges[newIndex[1]] || !(colleges[newIndex[1]].classes || []).length) {
				newIndex[2] = 0
			}
		}

		multiIndex.value = newIndex
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

			// 保存用户信息
			console.log(userInfo.value.avatarUrl);
			let res = await apiImproveUserInfo(userInfo.value.id, userInfo.value)
			
			uni.hideLoading()
			
			if (res.code === 200) {
				uni.setStorageSync('userInfo', res.data.user)
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
	// 定义主色调变量
	$primary-color: #FCB857;
	$primary-light: #FFE6B7;
	$primary-dark: #E6A33D;
	$bg-color: #F8F9FA;
	$text-primary: #333333;
	$text-secondary: #666666;
	$text-light: #999999;
	$border-color: #F0F0F0;
	$white: #FFFFFF;
	$shadow-light: rgba(0, 0, 0, 0.08);
	$shadow-medium: rgba(0, 0, 0, 0.12);

	.page {
		background-color: $bg-color;
		padding: 0;
	}

	// 头像区域
	.avatar-section {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 60rpx 0 40rpx;
		background: linear-gradient(135deg, #FCB857 0%, #FF9800 100%);
		margin-bottom: 30rpx;
		overflow: hidden;

		.avatar-bg {
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			opacity: 0.5;
		}

		.avatar-wrapper {
			margin-bottom: 30rpx;
			z-index: 1;

			.avatar {
				margin-left: -300rpx;
				width: 180rpx;
				height: 180rpx;
				border-radius: 50%;
				box-shadow: 0 12rpx 40rpx rgba(0, 0, 0, 0.15);
			}
		}

		.user-name {
			font-size: 40rpx;
			font-weight: 600;
			color: $white;
			letter-spacing: 1rpx;
			text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
			z-index: 1;
		}
	}

	// 信息卡片
	.info-card {
		background: $white;
		border-radius: 20rpx;
		overflow: hidden;
		margin: 0 30rpx 30rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.04);
		border: 1rpx solid $border-color;
		transition: all 0.25s ease;

		:deep(.uni-list-item) {
			padding: 30rpx 32rpx;
			border-bottom: 1rpx solid $border-color;
			position: relative;

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
				.uni-list-item__content {
					.uni-list-item__content-title {
						font-size: 32rpx;
						color: $text-primary;
						font-weight: 500;
						letter-spacing: 1rpx;
					}
				}

				.uni-list-item__extra {
					.uni-list-item__extra-text {
						font-size: 30rpx;
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
		margin-bottom: 60rpx;
	}

	// 保存按钮容器
	.save-button-container {
		padding: 20rpx 30rpx 60rpx;
		background: linear-gradient(to top, $bg-color 70%, transparent);
		position: sticky;
		bottom: 0;
		z-index: 10;
	}

	// 保存按钮样式
	.save-btn {
		background: linear-gradient(135deg, $primary-color 0%, $primary-dark 100%);
		border: none;
		border-radius: 50rpx;
		height: 100rpx;
		line-height: 100rpx;
		font-size: 34rpx;
		font-weight: 600;
		color: $white;
		position: relative;
		overflow: hidden;
		box-shadow: 0 8rpx 30rpx rgba(252, 184, 87, 0.3);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 16rpx;


		.btn-text {
			position: relative;
			z-index: 1;
			letter-spacing: 2rpx;
			transition: transform 0.3s ease;
		}
	}

	// 信息项包装器（用于覆盖 picker）
	.info-item-wrapper {
		position: relative;

		.overlay-picker {
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			z-index: 10;

			.picker-overlay {
				width: 100%;
				height: 100%;
			}
		}
	}
</style>