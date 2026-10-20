export default function formatTime(timestamp, format = 'YYYY-MM-DD hh:mm:ss') {
	if (!timestamp) return ''

	// 如果已经是标准格式的时间字符串，直接返回
	const datetimeRegex = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/
	if (typeof timestamp === 'string' && datetimeRegex.test(timestamp)) {
		return timestamp
	}

	// 如果是字符串时间戳，转换为数字
	timestamp = Number(timestamp)

	// 如果是秒级时间戳，转换为毫秒
	if (timestamp.toString().length === 10) {
		timestamp *= 1000
	}

	const date = new Date(timestamp)

	const pad = (n) => n.toString().padStart(2, '0')

	const map = {
		'YYYY': date.getFullYear(),
		'MM': pad(date.getMonth() + 1),
		'DD': pad(date.getDate()),
		'hh': pad(date.getHours()),
		'mm': pad(date.getMinutes()),
		'ss': pad(date.getSeconds()),
		'M': date.getMonth() + 1,
		'D': date.getDate(),
		'h': date.getHours(),
		'm': date.getMinutes(),
		's': date.getSeconds()
	}

	return format.replace(/YYYY|MM|DD|hh|mm|ss|M|D|h|m|s/g, matched => map[matched])
}