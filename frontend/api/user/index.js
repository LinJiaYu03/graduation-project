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

// 完善个人信息（当前登录用户，后端从令牌识别）
export const apiImproveUserInfo=(data)=>request({
	url:'/users/profile',
	data,
	method:'PUT'
})

// 当前登录用户角色与权限
export const apiGetMyPermissions=()=>request({
	url:'/rbac/me'
})

// 当前登录用户信息
export const apiGetCurrentUser=()=>request({
	url:'/users/profile'
})