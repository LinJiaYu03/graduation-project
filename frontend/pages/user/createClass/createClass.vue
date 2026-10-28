<template>
	<view class="page container">
		<!-- 表单区域 -->
		<view class="form-container">
			<uni-forms ref="form" :modelValue="formData" label-position="top" label-width="120">
				<!-- 学校选择 -->
				<uni-forms-item label="学校" name="schoolName" required>
					<view class="school-selector">
						<picker mode="selector" :range="schoolOptions" :value="schoolOptionIndex" @change="onSchoolOptionChange">
							<view class="picker-input">
								<text :class="schoolOptionIndex !== null ? 'picker-text' : 'picker-placeholder'">
									{{ schoolOptions[schoolOptionIndex] || '请选择或新建学校' }}
								</text>
								<uni-icons type="arrowdown" size="16" color="#A39B90"></uni-icons>
							</view>
						</picker>
						<!-- 新建学校输入框 -->
						<input 
							v-if="isNewSchool"
							class="input input-new" 
							type="text" 
							v-model="formData.schoolName" 
							placeholder="请输入新学校名称" 
							maxlength="50"
							@input="onNewSchoolInput"
						/>
					</view>
				</uni-forms-item>

				<!-- 学院选择 -->
				<uni-forms-item label="学院" name="collegeName">
					<view class="college-selector">
						<picker 
							mode="selector" 
							:range="collegeOptions" 
							:value="collegeOptionIndex" 
							@change="onCollegeOptionChange"
							:disabled="!formData.schoolName"
						>
							<view class="picker-input" :class="{ 'picker-disabled': !formData.schoolName }">
								<text :class="collegeOptionIndex !== null ? 'picker-text' : 'picker-placeholder'">
									{{ collegeOptions[collegeOptionIndex] || '请选择或新建学院（可选）' }}
								</text>
								<uni-icons type="arrowdown" size="16" color="#A39B90"></uni-icons>
							</view>
						</picker>
						<!-- 新建学院输入框 -->
						<input 
							v-if="isNewCollege && formData.schoolName"
							class="input input-new" 
							type="text" 
							v-model="formData.collegeName" 
							placeholder="请输入新学院名称" 
							maxlength="50"
							@input="onNewCollegeInput"
						/>
					</view>
				</uni-forms-item>

				<!-- 班级名称输入 -->
				<uni-forms-item label="班级名称" name="className">
					<input 
						class="input" 
						:class="{ 'input-disabled': !formData.collegeName }"
						type="text" 
						v-model="formData.className" 
						placeholder="请输入班级名称（可选，需先选择学院）" 
						maxlength="50"
						:disabled="!formData.collegeName"
					/>
				</uni-forms-item>
			</uni-forms>

			<!-- 提示信息 -->
			<view class="tips-container">
			<view class="tips-item">
				<uni-icons type="info" size="16" color="#FCB857"></uni-icons>
				<text class="tips-text">学校名称为必填项，可选择已有学校或新建</text>
			</view>
			</view>

			<!-- 提交按钮 -->
			<view class="submit-container">
				<button class="submit-btn" @click="handleSubmit">
					<text class="btn-text">创建</text>
				</button>
			</view>
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
		apiGetSchoolInfoTree,
		apiCreateCampus
	} from '@/api/school/index.js'

	const form = ref(null)
	const formData = reactive({
		schoolName: '',
		collegeName: '',
		className: ''
	})

	const schoolData = ref([])
	const schoolOptionIndex = ref(null)
	const collegeOptionIndex = ref(null)
	const isNewSchool = ref(false)
	const isNewCollege = ref(false)

	// 学校选项列表（包含"新建学校"选项）
	const schoolOptions = computed(() => {
		const list = schoolData.value.map(item => item.name)
		return [...list, '新建学校']
	})

	// 学院选项列表（根据选中的学校，包含"新建学院"选项）
	const collegeOptions = computed(() => {
		// 如果没有选择学校（包括新建学校状态），返回空数组
		if (!formData.schoolName && !isNewSchool.value) {
			return []
		}
		
		// 如果是新建学校，只显示"新建学院"选项
		if (isNewSchool.value) {
			return ['新建学院']
		}
		
		// 如果选择的是已有学校，显示该学校的学院列表
		const school = schoolData.value.find(s => s.name === formData.schoolName)
		if (school && school.colleges && school.colleges.length > 0) {
			const list = school.colleges.map(item => item.name)
			return [...list, '新建学院']
		}
		// 如果已有学校但没有学院，只显示"新建学院"选项
		return ['新建学院']
	})

	// 获取学校信息树
	async function getSchoolInfoTree() {
		try {
			let res = await apiGetSchoolInfoTree()
			if (res.code === 200) {
				schoolData.value = res.data.items || []
			}
		} catch (e) {
			console.error('获取学校信息失败', e)
			uni.showToast({
				title: '加载失败',
				icon: 'none'
			})
		}
	}

	// 学校选项变化
	function onSchoolOptionChange(e) {
		const index = e.detail.value
		schoolOptionIndex.value = index
		
		// 判断是否选择"新建学校"
		if (index === schoolOptions.value.length - 1) {
			// 选择新建学校
			isNewSchool.value = true
			formData.schoolName = ''
		} else {
			// 选择已有学校
			isNewSchool.value = false
			formData.schoolName = schoolData.value[index].name
		}
		
		// 重置学院和班级
		formData.collegeName = ''
		formData.className = ''
		collegeOptionIndex.value = null
		isNewCollege.value = false
	}

	// 新建学校输入
	function onNewSchoolInput(e) {
		formData.schoolName = e.detail.value
		// 如果学校名称变化，重置学院和班级
		if (!formData.schoolName) {
			formData.collegeName = ''
			formData.className = ''
			collegeOptionIndex.value = null
			isNewCollege.value = false
		}
	}

	// 学院选项变化
	function onCollegeOptionChange(e) {
		const index = e.detail.value
		collegeOptionIndex.value = index
		
		// 判断是否选择"新建学院"
		if (index === collegeOptions.value.length - 1) {
			// 选择新建学院
			isNewCollege.value = true
			formData.collegeName = ''
		} else {
			// 选择已有学院
			isNewCollege.value = false
			formData.collegeName = collegeOptions.value[index]
		}
		
		// 重置班级
		formData.className = ''
	}

	// 新建学院输入
	function onNewCollegeInput(e) {
		formData.collegeName = e.detail.value
		// 如果学院名称变化，重置班级
		if (!formData.collegeName) {
			formData.className = ''
		}
	}

	// 提交表单
	async function handleSubmit() {
		// 验证必填项
		if (!formData.schoolName) {
			uni.showToast({
				title: '请选择学校',
				icon: 'none'
			})
			return
		}

		// 验证至少填写学院或班级
		if (!formData.collegeName && !formData.className) {
			uni.showToast({
				title: '请至少填写学院或班级名称',
				icon: 'none'
			})
			return
		}

		uni.showLoading({
			title: '创建中...'
		})

		try {
			const submitData = {
				schoolName: formData.schoolName
			}
			
			if (formData.collegeName) {
				submitData.collegeName = formData.collegeName
			}
			
			if (formData.className) {
				submitData.className = formData.className
			}

			let res = await apiCreateCampus(submitData)
			uni.hideLoading()

			if (res.code === 200) {
				uni.showToast({
					title: '创建成功',
					icon: 'success'
				})
				
				// 重置表单
				formData.schoolName = ''
				formData.collegeName = ''
				formData.className = ''
				schoolOptionIndex.value = null
				collegeOptionIndex.value = null
				isNewSchool.value = false
				isNewCollege.value = false

				// 延迟返回
				setTimeout(() => {
					uni.navigateBack()
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
			console.error('创建失败', e)
		}
	}

	onMounted(() => {
		getSchoolInfoTree()
	})
</script>

<style lang="scss" scoped>
	$primary-color: $brand-primary;
	$primary-dark: $brand-primary-deep;
	$bg-color: $bg-page;
	$border-color: $border-base;
	$white: #FFFFFF;

	.page {
		background-color: $bg-color;
		min-height: 100vh;
	}

	.form-container {
		background: $white;
		border-radius: $radius-md;
		margin: 24rpx;
		padding: 40rpx 32rpx;
		box-shadow: $shadow-card;
		border: 1rpx solid $border-color;
	}

	.picker-input {
		width: 100%;
		height: 88rpx;
		background: $bg-subtle;
		border-radius: $radius-sm;
		padding: 0 24rpx;
		display: flex;
		align-items: center;
		justify-content: space-between;
		box-sizing: border-box;
		border: 2rpx solid transparent;

		&.picker-disabled {
			opacity: 0.6;
		}

		.picker-text {
			font-size: 28rpx;
			color: $text-primary;
			flex: 1;
		}

		.picker-placeholder {
			font-size: 28rpx;
			color: $text-tertiary;
			flex: 1;
		}
	}

	.school-selector,
	.college-selector {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
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

		&.input-new {
			margin-top: 20rpx;
		}

		&.input-disabled {
			opacity: 0.6;
			color: $text-tertiary;
		}

		&::placeholder {
			color: $text-tertiary;
		}
	}

	.tips-container {
		margin-top: 32rpx;
		padding: 24rpx;
		background: $brand-primary-soft;
		border-radius: $radius-sm;
		border-left: 4rpx solid $primary-color;

		.tips-item {
			display: flex;
			align-items: center;
			gap: 12rpx;
			margin-bottom: 12rpx;

			&:last-child {
				margin-bottom: 0;
			}

			.tips-text {
				font-size: 26rpx;
				color: $text-secondary;
				line-height: 1.5;
			}
		}
	}

	.submit-container {
		margin-top: 48rpx;
	}

	.submit-btn {
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

		.btn-text {
			letter-spacing: 2rpx;
		}

		&:active {
			background: $brand-primary-deep;
		}
	}
</style>

