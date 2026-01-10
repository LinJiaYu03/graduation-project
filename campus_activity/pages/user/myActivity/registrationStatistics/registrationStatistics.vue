<template>
	<view class="registration-statistics">
		<!-- 报名统计 -->
		<view class="chart-container">
			<view class="chart-title">报名状态</view>
			<view class="chart-content">
				<l-echart ref="registrationChartRef" @finished="initRegistrationChart"></l-echart>
			</view>
			<view class="chart-info">
				<text>总报名人数: {{ registrationData.total || 0 }}</text>
				<text>当前参与人数:
					{{ registrationData.currentParticipants || 0 }}/{{ registrationData.maxParticipants || 0 }}</text>
			</view>
		</view>

		<!-- 签到统计 -->
		<view class="chart-container">
			<view class="chart-title">签到情况</view>
			<view class="chart-content">
				<l-echart ref="checkinChartRef" @finished="initCheckinChart"></l-echart>
			</view>
			<view class="chart-info">
				<text>已签到人数: {{ checkinData.checkedIn || 0 }}</text>
				<text>未签到人数: {{ checkinData.notCheckedIn || 0 }}</text>
				<text>签到率: {{ checkinData.checkinRate || 0 }}%</text>
			</view>
		</view>

		<!-- 评分统计 -->
		<view class="chart-container">
			<view class="chart-title">评分情况</view>
			<view class="chart-content">
				<l-echart ref="scoreChartRef" @finished="initScoreChart"></l-echart>
			</view>
			<view class="chart-info">
				<text>平均评分: {{ scoreData.averageScore || 0 }}</text>
				<text>已评分人数: {{ scoreData.scoredCount || 0 }}</text>
				<text>未评分人数: {{ scoreData.notScoredCount || 0 }}</text>
				<text>评分率: {{ scoreData.scoreRate || 0 }}%</text>
			</view>
		</view>
	</view>
</template>

<script setup>
	import {
		ref,
		onMounted
	} from 'vue';
	import {
		apiGetRegistrationStatistics,
		apiGetCheckinStatistics,
		apiGetScoreStatistics
	} from '@/api/activity/index.js'

	const props = defineProps(['id'])
	const managerUserId = uni.getStorageSync('userInfo').id

	// 图表引用
	const registrationChartRef = ref(null)
	const checkinChartRef = ref(null)
	const scoreChartRef = ref(null)

	// 活动信息
	const activityInfo = ref({})

	// 报名统计数据
	const registrationData = ref({
		pending: 0,
		approved: 0,
		rejected: 0,
		total: 0,
		maxParticipants: 0,
		currentParticipants: 0
	})

	// 签到统计数据
	const checkinData = ref({
		checkedIn: 0,
		notCheckedIn: 0,
		totalApproved: 0,
		checkinRate: 0
	})

	// 评分统计数据
	const scoreData = ref({
		scoreDistribution: {
			'0.5-1.0': 0,
			'1.5-2.0': 0,
			'2.5-3.0': 0,
			'3.5-4.0': 0,
			'4.5-5.0': 0
		},
		averageScore: 0,
		scoredCount: 0,
		notScoredCount: 0,
		totalApproved: 0,
		scoreRate: 0
	})

	// 仅在小程序环境下引入 ECharts
	// #ifdef MP
	const echarts = require('../../../../static/echarts.min.js')
	// #endif
	// #ifndef MP
	const echarts = null // H5 和 App 环境不需要手动引入
	// #endif

	// 获取活动统计数据
	const getActivityStatistics = async () => {
		// 获取报名统计
		const registrationResponse = await apiGetRegistrationStatistics({
			activityId: props.id,
			managerUserId
		});

		if (registrationResponse.code === 200) {
			const statistics = registrationResponse.data.statistics;
			activityInfo.value = statistics.activityInfo;
			registrationData.value = {
				pending: statistics.statusStats.pending,
				approved: statistics.statusStats.approved,
				rejected: statistics.statusStats.rejected,
				total: statistics.statusStats.total,
				maxParticipants: statistics.maxParticipants,
				currentParticipants: statistics.currentParticipants
			};
			// 初始化报名图表
			await initRegistrationChart();
		}

		// 获取签到统计
		const checkinResponse = await apiGetCheckinStatistics({
			activityId: props.id,
			managerUserId
		});

		if (checkinResponse.code === 200) {
			const statistics = checkinResponse.data.statistics;
			checkinData.value = {
				checkedIn: statistics.checkedIn,
				notCheckedIn: statistics.notCheckedIn,
				totalApproved: statistics.totalApproved,
				checkinRate: statistics.checkinRate
			};
			// 初始化签到图表
			await initCheckinChart();
		}

		// 获取评分统计
		const scoreResponse = await apiGetScoreStatistics({
			activityId: props.id,
			managerUserId
		});

		if (scoreResponse.code === 200) {
			const statistics = scoreResponse.data.statistics;
			scoreData.value = {
				scoreDistribution: statistics.scoreDistribution,
				averageScore: statistics.averageScore,
				scoredCount: statistics.scoredCount,
				notScoredCount: statistics.notScoredCount,
				totalApproved: statistics.totalApproved,
				scoreRate: statistics.scoreRate
			};
			// 初始化评分图表
			await initScoreChart();
		}
	}

	// 创建报名统计饼图配置选项
	const createRegistrationPieChartOption = () => {
		return {
			title: {
				left: 'center',
				textStyle: {
					fontSize: 16
				}
			},
			tooltip: {
				trigger: 'item',
				formatter: '{a} {b}: {c} ({d}%)'
			},
			legend: {
				orient: 'horizontal',
				bottom: '5%',
				data: ['待审核', '已通过', '已拒绝']
			},
			series: [{
				name: '报名状态',
				type: 'pie',
				radius: ['40%', '70%'],
				data: [{
						value: registrationData.value.pending,
						name: '待审核'
					},
					{
						value: registrationData.value.approved,
						name: '已通过'
					},
					{
						value: registrationData.value.rejected,
						name: '已拒绝'
					}
				],
				color: ['#FFA500', '#52C41A', '#FF4D4F'],
				emphasis: {
					itemStyle: {
						shadowBlur: 10,
						shadowOffsetX: 0,
						shadowColor: 'rgba(0, 0, 0, 0.5)'
					}
				}
			}]
		};
	}

	// 创建签到统计饼图配置选项
	const createCheckinPieChartOption = () => {
		return {
			title: {
				left: 'center',
				textStyle: {
					fontSize: 16
				}
			},
			tooltip: {
				trigger: 'item',
				formatter: '{a} {b}: {c} ({d}%)'
			},
			legend: {
				orient: 'horizontal',
				bottom: '5%',
				data: ['已签到', '未签到']
			},
			series: [{
				name: '签到状态',
				type: 'pie',
				radius: ['40%', '70%'],
				data: [{
						value: checkinData.value.checkedIn,
						name: '已签到'
					},
					{
						value: checkinData.value.notCheckedIn,
						name: '未签到'
					}
				],
				color: ['#52C41A', '#FFA500'],
				emphasis: {
					itemStyle: {
						shadowBlur: 10,
						shadowOffsetX: 0,
						shadowColor: 'rgba(0, 0, 0, 0.5)'
					}
				}
			}]
		};
	}

	// 创建评分统计柱状图配置选项
	const createScoreBarChartOption = () => {
		return {
			title: {
				left: 'center',
				textStyle: {
					fontSize: 16
				}
			},
			tooltip: {
				trigger: 'axis',
				axisPointer: {
					type: 'shadow'
				}
			},
			grid: {
				left: '3%',
				right: '4%',
				bottom: '3%',
				containLabel: true
			},
			xAxis: {
				type: 'category',
				data: ['0.5-1.0', '1.5-2.0', '2.5-3.0', '3.5-4.0', '4.5-5.0']
			},
			yAxis: {
				type: 'value',
				name: '人数'
			},
			series: [{
				name: '评分分布',
				type: 'bar',
				data: [
					scoreData.value.scoreDistribution['0.5-1.0'],
					scoreData.value.scoreDistribution['1.5-2.0'],
					scoreData.value.scoreDistribution['2.5-3.0'],
					scoreData.value.scoreDistribution['3.5-4.0'],
					scoreData.value.scoreDistribution['4.5-5.0']
				],
				itemStyle: {
					color: function(params) {
						const colors = ['#FF4D4F', '#FF7A45', '#FFA500', '#52C41A', '#1890FF'];
						return colors[params.dataIndex];
					}
				},
				label: {
					show: true,
					position: 'top'
				}
			}]
		};
	}

	// 初始化报名图表
	const initRegistrationChart = async () => {
		if (!registrationChartRef.value) return

		try {
			const chart = await registrationChartRef.value.init(echarts)
			const option = createRegistrationPieChartOption()
			chart.setOption(option)
		} catch (error) {
			console.error('报名图表初始化失败:', error)
		}
	}

	// 初始化签到图表
	const initCheckinChart = async () => {
		if (!checkinChartRef.value) return

		try {
			const chart = await checkinChartRef.value.init(echarts)
			const option = createCheckinPieChartOption()
			chart.setOption(option)
		} catch (error) {
			console.error('签到图表初始化失败:', error)
		}
	}

	// 初始化评分图表
	const initScoreChart = async () => {
		if (!scoreChartRef.value) return

		try {
			const chart = await scoreChartRef.value.init(echarts)
			const option = createScoreBarChartOption()
			chart.setOption(option)
		} catch (error) {
			console.error('评分图表初始化失败:', error)
		}
	}

	// 页面加载时获取数据
	onMounted(() => {
		getActivityStatistics()
	})
</script>

<style lang="scss" scoped>
	.registration-statistics {
		min-height: 100vh;
		padding: 30rpx;
		display: flex;
		flex-direction: column;
		gap: 30rpx;
	}

	.chart-container {
		background: rgba(255, 255, 255, 0.95);
		border-radius: 20rpx;
		padding: 40rpx;
		box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.2);
		backdrop-filter: blur(10rpx);
		width: 100%;
		max-width: 800rpx;
		margin: 0 auto;
	}

	.chart-title {
		font-size: 32rpx;
		font-weight: 700;
		text-align: center;
		margin-bottom: 30rpx;
		color: #2c3e50;
		position: relative;
		padding-bottom: 15rpx;

		&::after {
			content: '';
			position: absolute;
			bottom: 0;
			left: 50%;
			transform: translateX(-50%);
			width: 100rpx;
			height: 4rpx;
			background: linear-gradient(90deg, #667eea, #764ba2);
			border-radius: 2rpx;
		}
	}

	.chart-content {
		width: 100%;
		height: 550rpx;
		margin-bottom: 30rpx;
	}

	.chart-info {
		display: flex;
		flex-wrap: wrap;
		gap: 20rpx;
		margin-top: 30rpx;
		padding: 25rpx;
		background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
		border-radius: 15rpx;

		text {
			flex: 1;
			min-width: 200rpx;
			font-size: 26rpx;
			color: #34495e;
			font-weight: 500;
			text-align: center;
			padding: 15rpx 0;

			&:nth-child(1) {
				color: #667eea;
			}

			&:nth-child(2) {
				color: #764ba2;
			}

			&:nth-child(3) {
				color: #52C41A;
			}

			&:nth-child(4) {
				color: #FFA500;
			}
		}
	}
</style>