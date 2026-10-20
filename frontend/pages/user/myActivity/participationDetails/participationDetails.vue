<template>
	<view class="participation container">
		<view class="participation_step">
			<uni-steps :options="list" :active="active" :active-color="list[2].title==='已拒绝'?activeColor:'#2979FF	'" />
		</view>

		<view class="participation_list">
			<uni-list>
				<uni-list-item title="报名时间" :rightText="formatTime(registrationTime,'YYYY.MM.DD')"></uni-list-item>
			</uni-list>
		</view>
	</view>
</template>

<script setup>
	import {
		onMounted,
		ref
	} from 'vue'
	import {
		apiGetActiviyStatus
	} from '@/api/activity/index.js'
	import formatTime from '@/utils/dateUtil'

	const props = defineProps(['activeId'])
	const userId = uni.getStorageSync('userInfo').id
	const registrationTime=ref('')
	const active = ref(1)
	const activeColor='#FB4A3E'
	const list = ref([{
		title: '已报名'
	}, {
		title: '待录取'
	}, {
		title: '已录取'
	},{
		title:'未签到'
	}])

	async function getActiviyStatus() {
		let res = await apiGetActiviyStatus({
			activityId: props.activeId,
			userId: userId
		})
		
		if (res.code == 200) {
			let status = res.data.registration.status
			registrationTime.value=res.data.registration.registrationTime
			
			console.log(res);

			if (status === '已通过') {
				active.value = 3
			} else if (status === '已拒绝') {
				active.value = 2
				list.value[2].title ='已拒绝'
			}else if(status==='签到成功'){
				active.value = 3
				list.value[3].title ='签到成功'
			}

		}
	}

	onMounted(() => {
		getActiviyStatus()
	})
</script>

<style lang="scss" scoped>
	.participation {
		display: flex;
		flex-direction: column;

		.participation_step {
			margin-top: 20vh;
		}

		.participation_list {
			margin-top: 270rpx;
		}
	}
</style>