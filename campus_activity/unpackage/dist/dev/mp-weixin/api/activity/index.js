"use strict";
const common_vendor = require("../../common/vendor.js");
const utils_request = require("../../utils/request.js");
const apiCreateActivity = (data) => utils_request.request({
  url: "/activities",
  method: "POST",
  data
});
const apiGetActivityList = (data) => utils_request.request({
  url: "/activities/search",
  method: "POST",
  data
});
const apiQueryActivity = (id) => utils_request.request({
  url: `/activities/${id}`
});
const apiJoinActivity = (id, data) => utils_request.request({
  url: `/activities/${id}/register`,
  method: "POST",
  data
});
const apiGetHotActivity = () => utils_request.request({
  url: "/activities/hot"
});
const apiGetClubActivity = (id) => utils_request.request({
  url: `/activities/club/${id}`
});
const apiGetJoinOrManangeActivity = (data) => utils_request.request({
  url: `/activities/user/${data.id}?type=${data.type}&keyword=${data.keyword}`
});
const apiGetActiviyStatus = (data) => utils_request.request({
  url: `/activities/${data.activityId}/registrations/check?userId=${data.userId}`
});
const apiActivityRate = (data) => utils_request.request({
  url: "/activities/comment",
  method: "POST",
  data
});
const apiGetMemberReviewList = (data) => utils_request.request({
  url: `/activities/${data.activityId}/registrations/status?managerUserId=${data.userId}`
});
const apiMemberReview = (data) => utils_request.request({
  url: "/activities/registrations/review",
  method: "POST",
  data
});
const apiActivityReviewList = () => utils_request.request({
  url: "/activities/pending?bossUserId=8"
});
const apiActivityReview = (data) => utils_request.request({
  url: "/activities/review",
  method: "POST",
  data
});
const apiGetRegistrationStatistics = (data) => utils_request.request({
  url: `/activities/${data.activityId}/statistics?managerUserId=${data.managerUserId}`
});
const apiGetCheckinStatistics = (data) => utils_request.request({
  url: `/activities/${data.activityId}/checkin-statistics?managerUserId=${data.managerUserId}`
});
const apiGetScoreStatistics = (data) => utils_request.request({
  url: `/activities/${data.activityId}/score-statistics?managerUserId=${data.managerUserId}`
});
const apiCheckinActivity = (data) => utils_request.request({
  url: "/activities/checkin",
  method: "POST",
  data
});
const apiUpdateActivity = (data) => utils_request.request({
  url: "/activities/update",
  method: "PUT",
  data
});
const apiUpdateActivityStatus = (id, data) => utils_request.request({
  url: `/activities/${id}/publish-status`,
  method: "PUT",
  data
});
const getBaseUrl = () => {
  return "http://localhost:8080/api";
};
const isMiniProgram = () => {
  return typeof common_vendor.index.getFileSystemManager === "function";
};
const exportFile = (url, fileName, callback) => {
  common_vendor.index.showLoading({ title: "正在导出..." });
  if (isMiniProgram()) {
    common_vendor.index.request({
      url,
      responseType: "arraybuffer",
      success: (res) => {
        common_vendor.index.hideLoading();
        if (res.statusCode === 200) {
          const fs = common_vendor.index.getFileSystemManager();
          const filePath = common_vendor.wx$1.env.USER_DATA_PATH + "/" + fileName;
          fs.writeFile({
            filePath,
            data: res.data,
            encoding: "binary",
            success: () => {
              common_vendor.index.openDocument({
                filePath,
                fileType: "xlsx",
                success: () => common_vendor.index.showToast({ title: "导出成功", icon: "success" }),
                fail: (err) => {
                  common_vendor.index.__f__("error", "at api/activity/index.js:156", "打开文件失败", err);
                  common_vendor.index.showToast({ title: "文件已保存到: " + filePath, icon: "none" });
                }
              });
            },
            fail: (err) => {
              common_vendor.index.__f__("error", "at api/activity/index.js:162", "写入文件失败", err);
              common_vendor.index.showToast({ title: "导出失败", icon: "none" });
            }
          });
        } else {
          common_vendor.index.showToast({ title: "导出失败: " + res.statusCode, icon: "none" });
        }
      },
      fail: (err) => {
        common_vendor.index.hideLoading();
        common_vendor.index.__f__("error", "at api/activity/index.js:172", "请求失败", err);
        common_vendor.index.showToast({ title: "导出失败", icon: "none" });
      }
    });
  } else {
    common_vendor.index.hideLoading();
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    link.click();
    common_vendor.index.showToast({ title: "导出成功", icon: "success" });
  }
};
const apiExportRegistration = (activityId, managerUserId) => {
  const url = `${getBaseUrl()}/activities/${activityId}/export/registration?managerUserId=${managerUserId}`;
  exportFile(url, "报名情况表.xlsx");
};
const apiExportCheckin = (activityId, managerUserId) => {
  const url = `${getBaseUrl()}/activities/${activityId}/export/checkin?managerUserId=${managerUserId}`;
  exportFile(url, "签到情况表.xlsx");
};
const apiExportScore = (activityId, managerUserId) => {
  const url = `${getBaseUrl()}/activities/${activityId}/export/score?managerUserId=${managerUserId}`;
  exportFile(url, "评分情况表.xlsx");
};
exports.apiActivityRate = apiActivityRate;
exports.apiActivityReview = apiActivityReview;
exports.apiActivityReviewList = apiActivityReviewList;
exports.apiCheckinActivity = apiCheckinActivity;
exports.apiCreateActivity = apiCreateActivity;
exports.apiExportCheckin = apiExportCheckin;
exports.apiExportRegistration = apiExportRegistration;
exports.apiExportScore = apiExportScore;
exports.apiGetActivityList = apiGetActivityList;
exports.apiGetActiviyStatus = apiGetActiviyStatus;
exports.apiGetCheckinStatistics = apiGetCheckinStatistics;
exports.apiGetClubActivity = apiGetClubActivity;
exports.apiGetHotActivity = apiGetHotActivity;
exports.apiGetJoinOrManangeActivity = apiGetJoinOrManangeActivity;
exports.apiGetMemberReviewList = apiGetMemberReviewList;
exports.apiGetRegistrationStatistics = apiGetRegistrationStatistics;
exports.apiGetScoreStatistics = apiGetScoreStatistics;
exports.apiJoinActivity = apiJoinActivity;
exports.apiMemberReview = apiMemberReview;
exports.apiQueryActivity = apiQueryActivity;
exports.apiUpdateActivity = apiUpdateActivity;
exports.apiUpdateActivityStatus = apiUpdateActivityStatus;
//# sourceMappingURL=../../../.sourcemap/mp-weixin/api/activity/index.js.map
