import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { apiGetCurrentUser } from '@/api/user/index.js'

// 小程序没有 localStorage，用 uni storage 作为持久化载体
const uniStorage = {
	getItem: (key) => uni.getStorageSync(key),
	setItem: (key, value) => uni.setStorageSync(key, value)
}

export const useUserStore = defineStore('user', () => {
	const user = ref(null)

	const id = computed(() => user.value?.id)
	const roles = computed(() => user.value?.roles || [])
	const isBoss = computed(() => roles.value.some(role => role.code === 'ADMIN'))
	const isManager = computed(() => roles.value.some(role => role.code === 'CLUB_MANAGER'))
	const avatarUrl = computed(() => user.value?.avatarUrl || '')
	const realName = computed(() => user.value?.realName || '')
	const studentNo = computed(() => user.value?.studentNo || '')

	async function fetchMe() {
		const res = await apiGetCurrentUser()
		if (res.code === 200 && res.data) {
			user.value = res.data
		}
		return user.value
	}

	function clear() {
		user.value = null
	}

	return {
		user,
		id,
		roles,
		isBoss,
		isManager,
		avatarUrl,
		realName,
		studentNo,
		fetchMe,
		clear
	}
}, {
	persist: {
		key: 'userInfo',
		storage: uniStorage,
		paths: ['user']
	}
})
