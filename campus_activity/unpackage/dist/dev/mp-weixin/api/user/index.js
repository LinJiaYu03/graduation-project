"use strict";
const utils_request = require("../../utils/request.js");
const apiUserLogin = (data) => utils_request.request({
  url: "/users/login",
  data,
  method: "POST"
});
const apiUserWxLogin = (data) => utils_request.request({
  url: "/users/wx-login",
  data,
  method: "POST"
});
const apiUserRegistration = (data) => utils_request.request({
  url: "/users/register",
  data,
  method: "POST"
});
const apiImproveUserInfo = (id, data) => utils_request.request({
  url: `/users/${id}/profile`,
  data,
  method: "PUT"
});
exports.apiImproveUserInfo = apiImproveUserInfo;
exports.apiUserLogin = apiUserLogin;
exports.apiUserRegistration = apiUserRegistration;
exports.apiUserWxLogin = apiUserWxLogin;
//# sourceMappingURL=../../../.sourcemap/mp-weixin/api/user/index.js.map
