import request from "@/utils/request";

// 用户登录
export const apiUserLogin=(data)=>request({
	url:'/users/login',
	data,
	method:'POST'
})

// 用户注册
export const apiUserRegistration=(data)=>request({
	url:'/users/register',
	data,
	method:'POST'
})

// 退出登录
export const apiUserLogout=(data)=>request({
	url:'/users/logout',
	data,
	method:'POST'
})

// 完善个人信息
export const apiImproveUserInfo=(id,data)=>request({
	url:`/users/${id}/profile`,
	data,
	method:'PUT'
})

// 当前用户角色与权限
export const apiGetMyPermissions=()=>request({
	url:'/rbac/me'
})

// 分配用户全局角色
export const apiAssignUserRoles=(id,data)=>request({
	url:`/users/${id}/roles`,
	data,
	method:'PUT'
})