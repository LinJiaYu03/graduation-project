import request from '@/utils/request.js'

// 创建社团
export const apiCreateClub = (data) => request({
	url: '/clubs',
	method: 'POST',
	data
})

// 查询社团列表
export const apiGetClubList = (data) => request({
	url: '/clubs/search',
	method: 'POST',
	data
})

// 查询我加入的社团
export const apiQueryJoinClubList = (data) => request({
	url: '/clubs/joined',
	method: 'POST',
	data
})

// 加入社团
export const apiJoinClub = (data) => request({
	url: '/clubs/join',
	method: 'POST',
	data
})

// 查看加入社团的人员列表
export const apiGetJoinClubUserList=(id)=>request({
	url:`/clubs/${id}/members`
})

// 设置社团管理员
export const apiSettingClubManager=(data)=>request({
	url:`/clubs/${data.clubId}/members/${data.userId}/manager?isManager=${data.isManager}`,
	method: 'POST'
})

// 获取最新社团列表
export const apiGetClubNewList=()=>request({
	url:'/clubs/latest?limit=6',
})

// 获取用户管理的社团下拉列表
export const apiGetClubManageList=(id)=>request({
	url:`/clubs/managed?userId=${id}`
})

// 查看社团详情
export const apiGetClubDetail=(id)=>request({
	url:`/clubs/${id}`,
})
