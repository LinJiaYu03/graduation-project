"use strict";
const common_vendor = require("./common/vendor.js");
const api_activity_index = require("./api/activity/index.js");
const utils_dateUtil = require("./utils/dateUtil.js");
const utils_request = require("./utils/request.js");
if (!Array) {
  const _easycom_uni_icons2 = common_vendor.resolveComponent("uni-icons");
  const _easycom_uni_popup2 = common_vendor.resolveComponent("uni-popup");
  (_easycom_uni_icons2 + _easycom_uni_popup2)();
}
const _easycom_uni_icons = () => "./uni_modules/uni-icons/components/uni-icons/uni-icons.js";
const _easycom_uni_popup = () => "./uni_modules/uni-popup/components/uni-popup/uni-popup.js";
if (!Math) {
  (_easycom_uni_icons + _easycom_uni_popup)();
}
const _sfc_main = {
  __name: "com-activity-item-managed",
  props: ["activeInfo"],
  emits: ["updataActivityList"],
  setup(__props, { emit: __emit }) {
    const props = __props;
    const emits = __emit;
    const userId = common_vendor.index.getStorageSync("userInfo").id;
    common_vendor.ref();
    common_vendor.ref(0);
    const qrcodePopup = common_vendor.ref(null);
    const qrcodeData = common_vendor.ref(null);
    const loading = common_vendor.ref(false);
    function activityDetail() {
      common_vendor.index.navigateTo({
        url: `/pages/activity/activityDetail/activityDetail?id=${props.activeInfo.id}`
      });
    }
    function memberReview() {
      common_vendor.index.navigateTo({
        url: `/pages/user/memberReview/memberReview?id=${props.activeInfo.id}`
      });
    }
    function editActivity() {
      common_vendor.index.navigateTo({
        url: `/pages/user/publishActivity/publishActivity?id=${props.activeInfo.id}`
      });
    }
    function onChangeActivityStatus(value) {
      common_vendor.index.showModal({
        content: value ? "确认下架该活动？" : "确认上架该活动？",
        async success(e) {
          if (e.confirm) {
            let res = await api_activity_index.apiUpdateActivityStatus(props.activeInfo.id, {
              managerUserId: userId,
              isPublished: !value
            });
            if (res.code == 200) {
              emits("updataActivityList");
              common_vendor.index.showToast({
                title: res.message,
                icon: "success"
              });
            }
          }
        }
      });
    }
    function deleteActivity() {
      common_vendor.index.showModal({
        content: "确认删除该活动？删除后不可恢复！",
        async success(e) {
          if (e.confirm) {
            let res = await api_activity_index.apiDeleteActivity(props.activeInfo.id, userId);
            if (res.code === 200) {
              common_vendor.index.showToast({
                title: "删除成功",
                icon: "success"
              });
              emits("updataActivityList");
            } else {
              common_vendor.index.showToast({
                title: res.message || "删除失败",
                icon: "none"
              });
            }
          }
        }
      });
    }
    async function showQrcode() {
      var _a, _b;
      (_a = qrcodePopup.value) == null ? void 0 : _a.open();
      loading.value = true;
      qrcodeData.value = null;
      try {
        const res = await utils_request.request({
          url: `/activities/${props.activeInfo.id}/qrcode`,
          method: "GET"
        });
        if (res.code === 200 && ((_b = res.data) == null ? void 0 : _b.qrcode)) {
          qrcodeData.value = res.data.qrcode;
        } else {
          common_vendor.index.showToast({
            title: res.message || "获取二维码失败",
            icon: "none"
          });
        }
      } catch (error) {
        common_vendor.index.__f__("error", "at pages/user/myActivity/components/com-activity-item-managed/com-activity-item-managed.vue:198", "获取二维码失败:", error);
        common_vendor.index.showToast({
          title: "获取二维码失败",
          icon: "none"
        });
      } finally {
        loading.value = false;
      }
    }
    function closeQrcode() {
      var _a;
      (_a = qrcodePopup.value) == null ? void 0 : _a.close();
    }
    async function saveQrcode() {
      var _a;
      if (!((_a = qrcodeData.value) == null ? void 0 : _a.qrCode)) {
        common_vendor.index.showToast({
          title: "二维码数据不存在",
          icon: "none"
        });
        return;
      }
      const base64 = qrcodeData.value.qrCode;
      common_vendor.index.showLoading({
        title: "保存中..."
      });
      try {
        const filePath = await base64ToPath(base64);
        await new Promise((resolve, reject) => {
          common_vendor.index.saveImageToPhotosAlbum({
            filePath,
            success: () => {
              common_vendor.index.hideLoading();
              common_vendor.index.showToast({
                title: "保存成功",
                icon: "success"
              });
              resolve();
            },
            fail: (err) => {
              common_vendor.index.hideLoading();
              if (err.errMsg.includes("auth deny")) {
                common_vendor.index.showModal({
                  title: "需要相册权限",
                  content: "请在设置中开启相册权限以保存图片",
                  confirmText: "去设置",
                  success: (res) => {
                    if (res.confirm) {
                      common_vendor.index.openSetting();
                    }
                  }
                });
              } else {
                common_vendor.index.showToast({
                  title: "保存失败",
                  icon: "none"
                });
              }
              reject(err);
            }
          });
        });
      } catch (error) {
        common_vendor.index.__f__("error", "at pages/user/myActivity/components/com-activity-item-managed/com-activity-item-managed.vue:270", "保存二维码失败:", error);
        common_vendor.index.hideLoading();
        common_vendor.index.showToast({
          title: "保存失败",
          icon: "none"
        });
      }
    }
    function base64ToPath(base64) {
      return new Promise((resolve, reject) => {
        const [, format, bodyData] = /data:image\/(\w+);base64,(.*)/.exec(base64) || [];
        if (!format) {
          reject(new Error("ERROR_BASE64SRC_PARSE"));
          return;
        }
        const filePath = `${common_vendor.wx$1.env.USER_DATA_PATH}/${Date.now()}.${format}`;
        const fs = common_vendor.wx$1.getFileSystemManager();
        fs.writeFile({
          filePath,
          data: bodyData,
          encoding: "base64",
          success: () => resolve(filePath),
          fail: reject
        });
      });
    }
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: __props.activeInfo.imageUrls[0],
        b: common_vendor.t(__props.activeInfo.name),
        c: common_vendor.t(__props.activeInfo.isPublished ? "上线状态" : "下线状态"),
        d: common_vendor.n(__props.activeInfo.isPublished ? "online" : "offline"),
        e: common_vendor.t(__props.activeInfo.activityType),
        f: common_vendor.t(common_vendor.unref(utils_dateUtil.formatTime)(__props.activeInfo.startTime, "YYYY.MM.DD hh:mm")),
        g: common_vendor.t(common_vendor.unref(utils_dateUtil.formatTime)(__props.activeInfo.endTime, "YYYY.MM.DD hh:mm")),
        h: common_vendor.o(activityDetail),
        i: common_vendor.o(memberReview),
        j: common_vendor.o(() => {
          common_vendor.index.navigateTo({
            url: `/pages/user/myActivity/registrationStatistics/registrationStatistics?id=${props.activeInfo.id}`
          });
        }),
        k: common_vendor.o(editActivity),
        l: common_vendor.o(showQrcode),
        m: common_vendor.t(__props.activeInfo.isPublished ? "活动下架" : "活动上架"),
        n: common_vendor.o(($event) => onChangeActivityStatus(__props.activeInfo.isPublished)),
        o: common_vendor.t(__props.activeInfo.status),
        p: common_vendor.p({
          type: "trash",
          size: "18",
          color: "#fff"
        }),
        q: common_vendor.o(deleteActivity),
        r: common_vendor.p({
          type: "closeempty",
          size: "24",
          color: "#666"
        }),
        s: common_vendor.o(closeQrcode),
        t: loading.value
      }, loading.value ? {
        v: common_vendor.p({
          type: "spinner-cycle",
          size: "40",
          color: "#FCB857"
        })
      } : qrcodeData.value ? {
        x: qrcodeData.value.qrCode,
        y: common_vendor.t(qrcodeData.value.activityName),
        z: common_vendor.t(qrcodeData.value.activityId)
      } : {
        A: common_vendor.p({
          type: "info",
          size: "40",
          color: "#ff3b30"
        })
      }, {
        w: qrcodeData.value,
        B: qrcodeData.value
      }, qrcodeData.value ? {
        C: common_vendor.p({
          type: "download",
          size: "18",
          color: "#fff"
        }),
        D: common_vendor.o(saveQrcode)
      } : {}, {
        E: common_vendor.sr(qrcodePopup, "76fc133d-1", {
          "k": "qrcodePopup"
        }),
        F: common_vendor.p({
          type: "center",
          ["background-color"]: "rgba(0,0,0,0.5)"
        })
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-76fc133d"]]);
exports.MiniProgramPage = MiniProgramPage;
//# sourceMappingURL=../.sourcemap/mp-weixin/com-activity-item-managed.js.map
