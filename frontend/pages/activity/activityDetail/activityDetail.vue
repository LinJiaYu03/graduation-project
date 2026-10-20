<template>
	<view class="activityDetail">
		<view class="activityDetail_top">
			<view class="banner">
				<swiper autoplay :interval="3000" :duration="1000" circular @change="onSwiperChange">
					<swiper-item v-for="(item, index) in bannerList" :key="index">
						<view class="swiper-item">
							<image :src="item" mode="aspectFill"></image>
						</view>
					</swiper-item>
				</swiper>
				<!-- 轮播图指示器 -->
				<view class="swiper-indicator">
					{{ currentSwiper + 1 }}/{{ bannerList.length }}
				</view>
			</view>

			<view class="info_mask">
				<view class="mask_bg"></view>
				<view class="mask_content">
					<view class="tag status-tag">{{ activityInfo?.status }}</view>
					<view class="title">{{ activityInfo?.name }}</view>
					<view class="address">
						<uni-icons type="location-filled" size="16" color="#fff"></uni-icons>
						<view class="text">{{ activityInfo?.location }}</view>
					</view>
					<view class="number_info">
						<view class="id">ID：{{ activityInfo?.id }}</view>
						<view class="people_count">
							已报人数：{{ activityInfo?.currentParticipants }}/{{activityInfo?.maxParticipants }}</view>
					</view>
				</view>
			</view>
		</view>

		<view class="activityDetail_bottom">
			<scroll-view scroll-y class="detail-scroll">
				<view class="detail_container">
					<!-- 组织者信息 -->
					<view class="organizer_card">
						<view class="organizer_header">
							<image class="organizer_avatar" :src="clubInfo?.iconUrl" mode="aspectFill"></image>
							<view class="organizer_info">
								<view class="organizer_name">{{ clubInfo?.name }}</view>
								<view class="organizer_desc">{{ clubInfo?.description }}</view>
							</view>
							<view>
								{{ clubInfo?.memberCount }}
							</view>
						</view>
					</view>

					<!-- 活动详情 -->
					<view class="detail_section">
						<view class="section_title">活动介绍</view>
						<view class="section_content">
							{{ activityInfo?.description }}
						</view>
					</view>

					<view class="detail_section">
						<view class="section_title">参与须知</view>
						<view class="section_content">
							{{ activityInfo?.notice }}
						</view>
					</view>

					<!-- 活动信息列表 -->
					<view class="info_list">
						<view class="info_item info_item--time">
							<view class="info_label">
								<uni-icons type="calendar" size="16" color="#666"></uni-icons>
								<text>报名时间</text>
							</view>
							<view class="info_value info_value--time">
								<text class="time_start">{{ formatTime(activityInfo?.registrationStartTime) }}</text>
								<text class="time_separator">至</text>
								<text class="time_end">{{ formatTime(activityInfo?.registrationEndTime) }}</text>
							</view>
						</view>
						<view class="info_item info_item--time">
							<view class="info_label">
								<uni-icons type="calendar" size="16" color="#666"></uni-icons>
								<text>活动时间</text>
							</view>
							<view class="info_value info_value--time">
								<text class="time_start">{{ formatTime(activityInfo?.startTime) }}</text>
								<text class="time_separator">至</text>
								<text class="time_end">{{ formatTime(activityInfo?.endTime) }}</text>
							</view>
						</view>
						<view class="info_item">
							<view class="info_label">
								<uni-icons type="flag" size="16" color="#666"></uni-icons>
								<text>活动级别</text>
							</view>
							<view class="info_value">{{ activityInfo?.activityLevel }}</view>
						</view>
						<view class="info_item">
							<view class="info_label">
								<uni-icons type="bars" size="16" color="#666"></uni-icons>
								<text>活动类型</text>
							</view>
							<view class="info_value">{{ activityInfo?.activityType }}</view>
						</view>
						<view class="info_item">
							<view class="info_label">
								<uni-icons type="person" size="16" color="#666"></uni-icons>
								<text>最大报名人数</text>
							</view>
							<view class="info_value">{{ activityInfo?.maxParticipants }}</view>
						</view>
						<view class="info_item">
							<view class="info_label">
								<uni-icons type="star" size="16" color="#666"></uni-icons>
								<text>综合评分</text>
							</view>
							<view class="info_value rating">{{ activityInfo?.score }}</view>
						</view>
					</view>

					<view class="detail_section" v-if="activityInfo?.status==='已结束'">
						<view class="section_title">活动留言</view>
						<view class="section_content">
							<uni-list  v-if="commentedMembersList.length!=0" border>
								<uni-list-chat  v-for="item in commentedMembersList" 
								:key="item.userId" 
								:title="item.realName"
									:avatar="item.avatarUrl"
									:note="item.comment" :time="formatTime(item.commentTime)"></uni-list-chat>
							</uni-list>
							<view v-else>暂无评论</view>
						</view>
					</view>
				</view>
			</scroll-view>
		</view>

		<!-- 底部操作栏 -->
		<view v-if="!isReview&&activityInfo?.status!='已结束'" class="activityDetail_btn">
			<view class="operation_btn">

			</view>

			<view class="primary_btn" @click="handleSignUp">
				立即报名
			</view>
		</view>

		<view v-if="isReview&&activityInfo?.status!='已结束'" class="activityDetail_btn activityDetail_btn--review">
			<view class="review_action review_action--reject" @click="handleReview(false)">
				<uni-icons type="closeempty" size="24" color="#fff"></uni-icons>
				<text class="action_text">拒绝</text>
			</view>

			<view class="review_divider"></view>

			<view class="review_action review_action--approve" @click="handleReview(true)">
				<uni-icons type="checkmarkempty" size="24" color="#fff"></uni-icons>
				<text class="action_text">同意</text>
			</view>
		</view>
	</view>

	<uni-popup ref="popup" type="dialog" background-color="#fff">
		<uni-popup-dialog type="info" title="活动报名" content="确认报名当前活动？" confirmText="确认" cancelText="取消"
			@confirm="handelJoinActivity" />
	</uni-popup>
</template>

<script setup>
	import {
		onMounted,
		ref,
	} from 'vue';
	import {
		onLoad
	} from '@dcloudio/uni-app'
	import {
		apiQueryActivity,
		apiJoinActivity,
		apiActivityReview
	} from '@/api/activity/index.js'
	import {
		apiGetClubDetail
	} from '@/api/club/index.js'
	import formatTime from '@/utils/dateUtil.js'

	const props = defineProps(['id'])

	const isReview = ref(false)
	const popup = ref(null)
	const activityInfo = ref(null)
	const commentedMembersList=ref([])
	const currentSwiper = ref(0)
	const isCollected = ref(true)
	const bannerList = ref([])
	const clubInfo = ref()
	const userId = uni.getStorageSync('userInfo').id

	const onSwiperChange = (e) => {
		currentSwiper.value = e.detail.current
	}

	const handleSignUp = () => {
		popup.value.open()
	}

	async function queryActivity() {
		let res = await apiQueryActivity(props.id)
		bannerList.value = res.data.imageUrls
		activityInfo.value = res.data.activity
		commentedMembersList.value=res.data.activity.commentedMembers
		let clubRes = await apiGetClubDetail(res.data.activity.clubId)
		clubInfo.value = clubRes.data.club
	}

	async function handelJoinActivity() {
		let res = await apiJoinActivity(props.id, {
			userId,
		})

		if (res.code == 200) {
			uni.showToast({
				icon: 'success',
				title: '报名成功'
			})

			setTimeout(() => {
				uni.reLaunch({
					url: '/pages/activity/activity'
				})
			}, 1000)
		}
	}

	function handleReview(value) {
		uni.showModal({
			title: '提示',
			content: value ? '确认通过此活动吗？' : '确认拒绝此活动吗？',
			success: async function(res) {
				if (res.confirm) {
					let res = await apiActivityReview({
						activityId: props.id,
						auditUserId: userId,
						pass: value
					})

					if (res.code == 200) {
						uni.showToast({
							icon: 'success',
							title: value ? '通过成功' : '拒绝成功'
						})

						setTimeout(() => {
							uni.navigateBack()
						}, 1000)
					}
				}
			}
		});
	}

	onLoad(() => {
		// 获取页面栈
		const pages = getCurrentPages();

		// 上一个页面（如果存在）
		const prevPage = pages[pages.length - 2];

		if (prevPage?.route === 'pages/user/clubReview/clubReview') {
			isReview.value = true
		}
	})

	onMounted(() => {
		queryActivity()
	})
</script>

<style lang="scss" scoped>
	.activityDetail {
		position: relative;
		background: #f8f8f8;
		min-height: 100vh;

		.activityDetail_top {
			position: relative;
			overflow: hidden;
			background: #fff;

			.banner {
				width: 100vw;
				height: 652rpx;
				position: relative;

				swiper {
					width: 100%;
					height: 100%;

					.swiper-item {
						width: 100%;
						height: 100%;

						image {
							width: 100%;
							height: 100%;
							display: block;
						}
					}
				}

				.swiper-indicator {
					position: absolute;
					top: 30rpx;
					right: 30rpx;
					background: rgba(0, 0, 0, 0.4);
					color: #fff;
					padding: 8rpx 20rpx;
					border-radius: 20rpx;
					font-size: 24rpx;
					backdrop-filter: blur(10px);
				}
			}

			.info_mask {
				position: absolute;
				left: 0;
				bottom: 0;
				width: 100%;
				color: #fff;
				z-index: 10;
				padding: 40rpx 30rpx 30rpx;
				box-sizing: border-box;

				.mask_bg {
					position: absolute;
					left: 0;
					bottom: 0;
					width: 100%;
					height: 100%;
					background: linear-gradient(to top,
							rgba(60, 60, 60, 0.9) 0%,
							rgba(90, 90, 90, 0.5) 60%,
							rgba(120, 120, 120, 0.2) 85%,
							transparent 100%);
					z-index: -1;
				}

				.mask_content {
					position: relative;
					z-index: 2;

					.status-tag {
						display: inline-block;
						background: linear-gradient(135deg, #0083F4, #0066CC);
						padding: 8rpx 24rpx;
						font-size: 24rpx;
						border-radius: 12rpx;
						font-weight: 500;
						letter-spacing: 1rpx;
						margin-bottom: 24rpx;
						box-shadow: 0 4rpx 12rpx rgba(0, 131, 244, 0.3);
					}

					.title {
						font-size: 36rpx;
						font-weight: 700;
						line-height: 1.4;
						margin-bottom: 24rpx;
						text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.5);
					}

					.address {
						display: flex;
						align-items: center;
						font-size: 28rpx;
						margin-bottom: 24rpx;
						opacity: 0.95;

						.text {
							margin-left: 12rpx;
						}
					}

					.number_info {
						display: flex;
						justify-content: space-between;
						align-items: center;
						font-size: 24rpx;
						opacity: 0.85;

						.id {
							flex: 1;
						}

						.people_count {
							flex: 1;
							text-align: right;
						}
					}
				}
			}
		}

		.activityDetail_bottom {
			padding-bottom: 120rpx;
			height: calc(100vh - 652rpx);

			.detail-scroll {
				height: 100%;

				.detail_container {
					padding: 30rpx;
				}
			}

			.organizer_card {
				background: #fff;
				border-radius: 16rpx;
				padding: 30rpx;
				margin-bottom: 24rpx;
				box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);

				.organizer_header {
					display: flex;
					align-items: center;

					.organizer_avatar {
						width: 80rpx;
						height: 80rpx;
						border-radius: 12rpx;
						margin-right: 20rpx;
					}

					.organizer_info {
						flex: 1;

						.organizer_name {
							font-size: 32rpx;
							font-weight: 600;
							color: #333;
							margin-bottom: 8rpx;
						}

						.organizer_desc {
							font-size: 24rpx;
							color: #999;
						}
					}

					.follow_btn {
						padding: 12rpx 24rpx;
						border: 1rpx solid $uni-topic-color;
						color: $uni-topic-color;
						border-radius: 20rpx;
						font-size: 24rpx;
					}
				}
			}

			.detail_section {
				background: #fff;
				border-radius: 16rpx;
				padding: 30rpx;
				margin-bottom: 24rpx;
				box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);

				.section_title {
					font-size: 32rpx;
					font-weight: 600;
					color: #333;
					margin-bottom: 20rpx;
					position: relative;
					padding-left: 20rpx;

					&::before {
						content: '';
						position: absolute;
						left: 0;
						top: 50%;
						transform: translateY(-50%);
						width: 6rpx;
						height: 28rpx;
						background: $uni-topic-color;
						border-radius: 3rpx;
					}
				}

				.section_content {
					font-size: 28rpx;
					line-height: 1.6;
					color: #666;
				}
			}

			.info_list {
				margin-bottom: 24rpx;
				background: #fff;
				border-radius: 16rpx;
				overflow: hidden;
				box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);

				.info_item {
					display: flex;
					justify-content: space-between;
					align-items: center;
					padding: 28rpx 30rpx;
					border-bottom: 1rpx solid #f0f0f0;

					&:last-child {
						border-bottom: none;
					}

					&--time {
						flex-direction: column;
						align-items: flex-start;
						padding: 32rpx 30rpx;

						.info_label {
							margin-bottom: 16rpx;
							width: 100%;
						}

						.info_value {
							width: 100%;
							text-align: left;
						}
					}

					.info_label {
						display: flex;
						align-items: center;
						font-size: 28rpx;
						color: #666;
						flex-shrink: 0;
						margin-right: 20rpx;

						uni-icons {
							margin-right: 12rpx;
						}
					}

					.info_value {
						font-size: 28rpx;
						color: #333;
						font-weight: 500;
						text-align: right;
						flex: 1;
						min-width: 0;

						&.rating {
							color: #FF6B35;
						}

						&--time {
							display: flex;
							flex-direction: column;
							align-items: flex-start;
							gap: 10rpx;

							.time_start,
							.time_end {
								font-size: 26rpx;
								color: #333;
								font-weight: 500;
								line-height: 1.6;
								word-break: break-all;
								position: relative;
								padding-left: 24rpx;

								&::before {
									content: '';
									position: absolute;
									left: 0;
									top: 50%;
									transform: translateY(-50%);
									width: 8rpx;
									height: 8rpx;
									border-radius: 50%;
									background: $uni-topic-color;
								}
							}

							.time_start::before {
								background: #4CAF50;
							}

							.time_end::before {
								background: #FF6B35;
							}

							.time_separator {
								font-size: 24rpx;
								color: #999;
								margin: 2rpx 0 2rpx 24rpx;
								font-weight: 400;
								opacity: 0.8;
							}
						}
					}
				}
			}
		}

		.activityDetail_btn {
			display: flex;
			justify-content: space-between;
			position: fixed;
			left: 0;
			bottom: 0;
			width: 100vw;
			height: 120rpx;
			background: #fff;
			box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.1);
			padding: 0 30rpx;
			box-sizing: border-box;
			align-items: center;

			.operation_btn {
				display: flex;
				flex-direction: column;
				align-items: center;
				margin-right: 40rpx;
				padding: 16rpx 0;

				.btn_text {
					font-size: 22rpx;
					color: #666;
					margin-top: 8rpx;

					&.collected {
						color: #FCB857;
					}
				}
			}

			.primary_btn {
				width: 60vw;
				height: 80rpx;
				line-height: 80rpx;
				text-align: center;
				background: linear-gradient(135deg, $uni-topic-color, darken($uni-topic-color, 10%));
				color: #fff;
				font-size: 32rpx;
				font-weight: 600;
				border-radius: 40rpx;
				box-shadow: 0 8rpx 24rpx rgba($uni-topic-color, 0.3);
			}

			&.activityDetail_btn--review {
				padding: 0 40rpx;
				height: 140rpx;
				background: #fff;
				box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.1);

				.review_action {
					flex: 1;
					height: 80rpx;
					display: flex;
					align-items: center;
					justify-content: center;
					border-radius: 40rpx;
					font-size: 0;

					uni-icons {
						margin-right: 12rpx;
					}

					.action_text {
						font-size: 28rpx;
						font-weight: 600;
					}

					&--reject {
						background: linear-gradient(135deg, #FF6B6B, #FF4757);
						color: #fff;
						box-shadow: 0 6rpx 16rpx rgba(255, 107, 107, 0.3);

						&:active {
							background: linear-gradient(135deg, #FF4757, #FF3838);
							transform: translateY(2rpx);
						}
					}

					&--approve {
						background: linear-gradient(135deg, #4CAF50, #2E7D32);
						color: #fff;
						box-shadow: 0 6rpx 16rpx rgba(76, 175, 80, 0.3);

						&:active {
							background: linear-gradient(135deg, #43A047, #1B5E20);
							transform: translateY(2rpx);
						}
					}
				}

				.review_divider {
					width: 40rpx;
				}
			}
		}
	}
</style>