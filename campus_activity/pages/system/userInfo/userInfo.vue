<template>
	<view class="userinfo-container">
		<view class="userinfo-header">
			<text class="title">完善个人信息</text>
			<text class="subtitle">请填写以下信息以继续使用</text>
		</view>

		<view class="userinfo-form">
			<uni-forms ref="form" :rules="rules" :modelValue="formData" label-position="top" label-width="120">
				<uni-forms-item label="姓名" name="realName" required>
					<input class="input" type="text" v-model="formData.realName" placeholder="请输入真实姓名" maxlength="20"
						@input="onInput('realName', $event)" />
				</uni-forms-item>

				<uni-forms-item label="学号" name="studentNo" required>
					<input class="input" type="text" v-model="formData.studentNo" placeholder="请输入学号" maxlength="20"
						@input="onInput('studentNo', $event)" />
				</uni-forms-item>

				<uni-forms-item label="性别" name="gender" required>
					<radio-group @change="onGenderChange" class="radio-group">
						<label class="radio-item">
							<radio value="1" :checked="formData.gender === '1'" color="#1890ff" />
							<text class="radio-text">男</text>
						</label>
						<label class="radio-item">
							<radio value="0" :checked="formData.gender === '0'" color="#1890ff" />
							<text class="radio-text">女</text>
						</label>
					</radio-group>
				</uni-forms-item>

				<uni-forms-item label="学校/学院/班级" name="schoolInfo" required>
					<picker mode="multiSelector" :range="multiArray" :value="multiIndex" @change="onPickerChange"
						@columnchange="onPickerColumnChange" class="picker-wrapper">
						<view class="picker-input">
							<text :class="pickerDisplayText ? 'picker-text' : 'picker-placeholder'">
								{{ pickerDisplayText || '请选择学校、学院、班级' }}
							</text>
							<text class="picker-arrow">›</text>
						</view>
					</picker>
				</uni-forms-item>

				<uni-forms-item label="手机号" name="phone">
					<input class="input" type="number" v-model="formData.phone" placeholder="请输入手机号（选填）" maxlength="11"
						@input="onInput('phone', $event)" />
				</uni-forms-item>

				<uni-forms-item label="邮箱" name="email">
					<input class="input" type="text" v-model="formData.email" placeholder="请输入邮箱（选填）" maxlength="50"
						@input="onInput('email', $event)" />
				</uni-forms-item>
			</uni-forms>

			<button class="submit-btn" @click="handleSubmit">提交</button>
		</view>
	</view>
</template>

<script setup>
	import {
		ref,
		reactive,
		computed,
		onMounted
	} from 'vue'
	import {
		onLoad
	} from '@dcloudio/uni-app'
	import {
		apiGetSchoolInfoTree
	} from '@/api/school/index.js'
	import {
		apiImproveUserInfo
	} from '@/api/user/index.js'

	const form = ref(null)
	const formData = reactive({
		realName: '',
		studentNo: '',
		schoolName: '',
		collegeName: '',
		className: '',
		gender: '1',
		phone: '',
		email: ''
	})
	const userId = ref()

	// 三级联动数据（示例数据，可根据实际情况修改）
	const schoolData = ref([])

	// 初始化 multiIndex，兼容后端返回的对象结构
	const initMultiIndex = () => {
		if (formData.schoolName && formData.collegeName && formData.className && schoolData.value.length > 0) {
			const schoolIndex = schoolData.value.findIndex(school => school.name === formData.schoolName)
			if (schoolIndex !== -1) {
				const colleges = schoolData.value[schoolIndex].colleges || []
				const collegeIndex = colleges.findIndex(college => college.name === formData.collegeName)
				if (collegeIndex !== -1) {
					const classes = colleges[collegeIndex].classes || []
					const classIndex = classes.findIndex(cls => cls.name === formData.className)
					if (classIndex !== -1) {
						return [schoolIndex, collegeIndex, classIndex]
					}
				}
			}
		}
		return [0, 0, 0]
	}

	const multiIndex = ref(initMultiIndex())

	// 构建三级联动的数组（使用 name 字段）
	const multiArray = computed(() => {
		if (!schoolData.value || schoolData.value.length === 0) {
			return [
				[],
				[],
				[]
			]
		}
		const schools = schoolData.value.map(item => item.name)
		const colleges = (schoolData.value[multiIndex.value[0]]?.colleges || []).map(item => item.name)
		const classes = (schoolData.value[multiIndex.value[0]]?.colleges?.[multiIndex.value[1]]?.classes || [])
			.map(
				item => item.name)
		return [schools, colleges, classes]
	})
	const pickerDisplayText = computed(() => {
		if (!formData.schoolName || !formData.collegeName || !formData.className) {
			return ''
		}
		return `${formData.schoolName} - ${formData.collegeName} - ${formData.className}`
	})

	const rules = {
		realName: {
			rules: [{
				required: true,
				errorMessage: '请输入姓名'
			}]
		},
		studentNo: {
			rules: [{
					required: true,
					errorMessage: '请输入学号'
				},
				{
					pattern: /^\d+$/,
					errorMessage: '学号格式不正确，只能输入数字'
				}
			]
		},
		gender: {
			rules: [{
				required: true,
				errorMessage: '请选择性别'
			}]
		},
		schoolInfo: {
			rules: [{
				validateFunction: (rule, value, data, callback) => {
					if (!formData.schoolName || !formData.collegeName || !formData.className) {
						callback('请选择学校、学院、班级')
					}
					return true
				}
			}]
		},
		phone: {
			rules: [{
				validateFunction: (rule, value, data, callback) => {
					if (value && !/^1[3-9]\d{9}$/.test(value)) {
						callback('手机号格式不正确')
					}
					return true
				}
			}]
		},
		email: {
			rules: [{
				validateFunction: (rule, value, data, callback) => {
					if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
						callback('邮箱格式不正确')
					}
					return true
				}
			}]
		}
	}

	const onInput = (name, e) => {
		const value = e.detail ? e.detail.value : e.target.value
		formData[name] = value
		if (form.value) {
			form.value.setValue(name, value)
		}
	}

	// 性别选择变化
	const onGenderChange = (e) => {
		formData.gender = e.detail.value
		if (form.value) {
			form.value.setValue('gender', e.detail.value)
		}
	}

	// 三级联动选择器变化
	const onPickerChange = (e) => {
		const values = e.detail.value
		multiIndex.value = values

		const schoolIndex = values[0]
		const collegeIndex = values[1]
		const classIndex = values[2]

		const school = schoolData.value[schoolIndex]
		if (school) {
			formData.schoolName = school.name

			const college = (school.colleges || [])[collegeIndex]
			if (college) {
				formData.collegeName = college.name

				const cls = (college.classes || [])[classIndex]
				if (cls) {
					formData.className = cls.name
				} else {
					formData.className = ''
				}
			} else {
				formData.collegeName = ''
				formData.className = ''
			}
		}

		// 更新表单验证
		if (form.value) {
			form.value.setValue('schoolInfo', pickerDisplayText.value)
		}
	}

	// 列变化时处理联动
	const onPickerColumnChange = (e) => {
		const column = e.detail.column
		const value = e.detail.value

		// 更新当前列的索引（需要创建新数组以触发响应式更新）
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

		// 避免越界：当学校或学院没有数据时，保持索引为 0
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

	const handleSubmit = async () => {
		try {
			await form.value.validate()

			let res = await apiImproveUserInfo(userId.value, formData)

			if (res.code === 200) {
				console.log(res.data);
				uni.setStorageSync('userInfo', res.data.user)
				uni.setStorageSync('token', res.data.user.token)
				uni.showToast({
					title: '保存成功',
					icon: 'success'
				})

				// 跳转到主页
				setTimeout(() => {
					uni.reLaunch({
						url: '/pages/system/login/login'
					})
				}, 1500)
			}
		} catch (e) {
			console.log('表单校验失败', e)
		}
	}

	// 获取学校信息树
	async function getSchoolInfoTree() {

		let res = await apiGetSchoolInfoTree()
		schoolData.value = res.data.items || []

		// 数据加载后重新初始化索引
		multiIndex.value = initMultiIndex()
	}

	onMounted(async () => {
		getSchoolInfoTree()
	})

	onLoad((e) => {
		userId.value = e.id
	})
</script>

<style lang="scss" scoped>
	.userinfo-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #e6f4ff 0%, #f0f8ff 100%);
		padding: 80rpx 60rpx;
	}

	.userinfo-header {
		text-align: center;
		margin-bottom: 60rpx;

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

	.userinfo-form {
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

	.radio-group {
		display: flex;
		gap: 60rpx;

		.radio-item {
			display: flex;
			align-items: center;
			gap: 12rpx;

			.radio-text {
				font-size: 28rpx;
				color: #333333;
			}
		}
	}

	.picker-wrapper {
		width: 100%;

		.picker-input {
			width: 100%;
			height: 88rpx;
			background: #fafafa;
			border-radius: 8rpx;
			padding: 0 24rpx;
			display: flex;
			align-items: center;
			justify-content: space-between;
			box-sizing: border-box;
			border: 1rpx solid #d9ecff;

			.picker-text {
				font-size: 28rpx;
				color: #333333;
				flex: 1;
			}

			.picker-placeholder {
				font-size: 28rpx;
				color: #999999;
				flex: 1;
			}

			.picker-arrow {
				font-size: 32rpx;
				color: #999999;
				transform: rotate(90deg);
			}
		}
	}

	.submit-btn {
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
</style>