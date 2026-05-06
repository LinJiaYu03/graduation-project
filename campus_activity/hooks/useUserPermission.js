export default function useUserPermission(){
	const userInfo = uni.getStorageSync('userInfo') || {}
	console.log('userInfo:', userInfo)
	const isBoss = userInfo.isBoss
	const isManager = userInfo.isManager
	console.log('isBoss:', isBoss, 'isManager:', isManager)

	return {
		isBoss,
		isManager
	}
}