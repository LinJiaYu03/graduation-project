import requset from '@/utils/request.js'

export const apiGetSchoolInfoTree = () => requset({
	url: '/campus/tree'
})

// 创建学校/学院/班级
export const apiCreateCampus = (data) => requset({
	url: '/campus',
	method: 'POST',
	data
})