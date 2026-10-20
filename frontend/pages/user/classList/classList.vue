<template>
	<view class="page container">
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<uni-load-more status="loading" :content-text="loadMoreText"></uni-load-more>
		</view>

		<!-- 学校列表 -->
		<view v-else class="school-list">
			<view v-for="(school, schoolIndex) in schoolData" :key="schoolIndex" class="school-item">
				<!-- 学校标题 -->
				<view class="school-header" @click="toggleSchool(schoolIndex)">
					<view class="school-info">
						<uni-icons :type="school.expanded ? 'arrowdown' : 'arrowright'" size="20" color="#666"></uni-icons>
						<text class="school-name">{{ school.name }}</text>
						<text class="school-count">({{ getSchoolCount(school) }})</text>
					</view>
				</view>

				<!-- 学院列表 -->
				<view v-if="school.expanded" class="college-list">
					<view v-for="(college, collegeIndex) in school.colleges" :key="collegeIndex" class="college-item">
						<!-- 学院标题 -->
						<view class="college-header" @click="toggleCollege(schoolIndex, collegeIndex)">
							<view class="college-info">
								<uni-icons :type="college.expanded ? 'arrowdown' : 'arrowright'" size="18" color="#888"></uni-icons>
								<text class="college-name">{{ college.name }}</text>
								<text class="college-count">({{ college.classes ? college.classes.length : 0 }})</text>
							</view>
						</view>

						<!-- 班级列表 -->
						<view v-if="college.expanded && college.classes" class="class-list">
							<view v-for="(cls, classIndex) in college.classes" :key="classIndex" class="class-item">
								<text class="class-name">{{ cls.name }}</text>
							</view>
							<view v-if="!college.classes || college.classes.length === 0" class="empty-class">
								<text class="empty-text">暂无班级</text>
							</view>
						</view>
					</view>
					<view v-if="!school.colleges || school.colleges.length === 0" class="empty-college">
						<text class="empty-text">暂无学院</text>
					</view>
				</view>
			</view>
			<view v-if="!schoolData || schoolData.length === 0" class="empty-container">
				<text class="empty-text">暂无学校数据</text>
			</view>
		</view>
	</view>
</template>

<script setup>
	import {
		ref,
		onMounted
	} from 'vue'
	import {
		apiGetSchoolInfoTree
	} from '@/api/school/index.js'

	const schoolData = ref([])
	const loading = ref(false)
	const loadMoreText = {
		contentdown: '上拉加载更多',
		contentrefresh: '加载中...',
		contentnomore: '没有更多了'
	}

	// 获取学校信息树
	async function getSchoolInfoTree() {
		loading.value = true
		try {
			let res = await apiGetSchoolInfoTree()
			if (res.code === 200) {
				// 为每个学校添加 expanded 属性
				schoolData.value = (res.data.items || []).map(school => ({
					...school,
					expanded: false,
					colleges: (school.colleges || []).map(college => ({
						...college,
						expanded: false
					}))
				}))
			}
		} catch (e) {
			console.error('获取学校信息失败', e)
			uni.showToast({
				title: '加载失败',
				icon: 'none'
			})
		} finally {
			loading.value = false
		}
	}

	// 切换学校展开/收起
	function toggleSchool(index) {
		schoolData.value[index].expanded = !schoolData.value[index].expanded
	}

	// 切换学院展开/收起
	function toggleCollege(schoolIndex, collegeIndex) {
		schoolData.value[schoolIndex].colleges[collegeIndex].expanded = 
			!schoolData.value[schoolIndex].colleges[collegeIndex].expanded
	}

	// 获取学校总数（包括所有学院和班级）
	function getSchoolCount(school) {
		let count = 0
		if (school.colleges) {
			school.colleges.forEach(college => {
				if (college.classes) {
					count += college.classes.length
				}
			})
		}
		return count
	}

	onMounted(() => {
		getSchoolInfoTree()
	})
</script>

<style lang="scss" scoped>
	$primary-color: #FCB857;
	$bg-color: #F8F9FA;
	$text-primary: #333333;
	$text-secondary: #666666;
	$text-light: #999999;
	$border-color: #F0F0F0;
	$white: #FFFFFF;

	.page {
		background-color: $bg-color;
		min-height: 100vh;
	}

	.page-header {
		background: linear-gradient(135deg, #FCB857 0%, #FF9800 100%);
		padding: 60rpx 30rpx 40rpx;
		margin: 0 -24rpx 30rpx -24rpx;

		.page-title {
			font-size: 44rpx;
			font-weight: 600;
			color: $white;
			letter-spacing: 1rpx;
		}
	}

	.loading-container {
		padding: 100rpx 0;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.school-list {
		margin-top: 10rpx;
		padding: 40rpx 32rpx;
		background-color: #FFFFFF;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.04);
		border: 1rpx solid $border-color;
	}

	.school-item {
		background: $white;
		border-radius: 20rpx;
		margin-bottom: 24rpx;
		overflow: hidden;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.04);
		border: 1rpx solid $border-color;
	}

	.school-header {
		padding: 32rpx;
		border-bottom: 1rpx solid $border-color;
		background: linear-gradient(135deg, rgba(252, 184, 87, 0.1) 0%, rgba(255, 152, 0, 0.1) 100%);

		.school-info {
			display: flex;
			align-items: center;
			gap: 16rpx;

			.school-name {
				font-size: 36rpx;
				font-weight: 600;
				color: $text-primary;
			}

			.school-count {
				font-size: 28rpx;
				color: $text-secondary;
			}
		}
	}

	.college-list {
		padding: 0;
	}

	.college-item {
		border-bottom: 1rpx solid $border-color;

		&:last-child {
			border-bottom: none;
		}
	}

	.college-header {
		padding: 24rpx 32rpx;
		background: rgba(248, 249, 250, 0.5);

		.college-info {
			display: flex;
			align-items: center;
			gap: 12rpx;

			.college-name {
				font-size: 32rpx;
				font-weight: 500;
				color: $text-primary;
			}

			.college-count {
				font-size: 26rpx;
				color: $text-secondary;
			}
		}
	}

	.class-list {
		padding: 0 32rpx 16rpx 64rpx;
	}

	.class-item {
		padding: 20rpx 0;
		border-bottom: 1rpx solid rgba(240, 240, 240, 0.5);

		&:last-child {
			border-bottom: none;
		}

		.class-name {
			font-size: 30rpx;
			color: $text-secondary;
		}
	}

	.empty-container,
	.empty-college,
	.empty-class {
		padding: 40rpx;
		text-align: center;

		.empty-text {
			font-size: 28rpx;
			color: $text-light;
		}
	}
</style>

