"use strict";
const common_vendor = require("../common/vendor.js");
function useUserPermission() {
  const userInfo = common_vendor.index.getStorageSync("userInfo") || {};
  common_vendor.index.__f__("log", "at hooks/useUserPermission.js:3", "userInfo:", userInfo);
  const isBoss = userInfo.isBoss;
  const isManager = userInfo.isManager;
  common_vendor.index.__f__("log", "at hooks/useUserPermission.js:6", "isBoss:", isBoss, "isManager:", isManager);
  return {
    isBoss,
    isManager
  };
}
exports.useUserPermission = useUserPermission;
//# sourceMappingURL=../../.sourcemap/mp-weixin/hooks/useUserPermission.js.map
