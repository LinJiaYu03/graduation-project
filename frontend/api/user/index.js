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

// 完善个人信息
export const apiImproveUserInfo=(id,data)=>request({
	url:`/users/${id}/profile`,
	data,
	method:'PUT'
})