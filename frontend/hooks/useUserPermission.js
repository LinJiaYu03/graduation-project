export default function useUserPermission() {
	const userInfo = uni.getStorageSync('userInfo') || {}
	const roles = userInfo.roles || []
	const permissions = userInfo.permissions || []

	const isBoss = roles.some(role => role.code === 'ADMIN')
	const isManager = roles.some(role => role.code === 'CLUB_MANAGER')

	return {
		isBoss,
		isManager,
		roles,
		permissions
	}
}
