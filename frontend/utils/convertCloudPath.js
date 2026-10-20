export default function convertCloudPath(cloudPath) {
	// 提取环境ID和文件路径
	const match = cloudPath.match(/cloud:\/\/([^\/]+)\/(.+)/);

	if (!match) {
		return cloudPath; // 如果不是cloud://格式，返回原路径
	}

	const envId = match[1]; // env-00jxuc2o76k9
	const filePath = match[2]; // avatar/1765554670933_xin.jpg

	// 构建新的URL
	return `https://${envId}.normal.cloudstatic.cn/${filePath}`;
}