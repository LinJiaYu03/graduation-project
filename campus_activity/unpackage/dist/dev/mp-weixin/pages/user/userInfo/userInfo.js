"use strict";
const common_vendor = require("../../../common/vendor.js");
const utils_convertCloudPath = require("../../../utils/convertCloudPath.js");
const api_user_index = require("../../../api/user/index.js");
const api_school_index = require("../../../api/school/index.js");
if (!Array) {
  const _easycom_uni_list_item2 = common_vendor.resolveComponent("uni-list-item");
  const _easycom_uni_list2 = common_vendor.resolveComponent("uni-list");
  (_easycom_uni_list_item2 + _easycom_uni_list2)();
}
const _easycom_uni_list_item = () => "../../../uni_modules/uni-list/components/uni-list-item/uni-list-item.js";
const _easycom_uni_list = () => "../../../uni_modules/uni-list/components/uni-list/uni-list.js";
if (!Math) {
  (_easycom_uni_list_item + _easycom_uni_list)();
}
const _sfc_main = {
  __name: "userInfo",
  setup(__props) {
    const userInfo = common_vendor.ref(common_vendor.index.getStorageSync("userInfo"));
    const userAvatar = common_vendor.ref(userInfo.value.avatarUrl);
    const filesName = common_vendor.ref();
    const schoolData = common_vendor.ref([]);
    const multiIndex = common_vendor.ref([0, 0, 0]);
    const multiArray = common_vendor.computed(() => {
      var _a, _b, _c, _d;
      if (!schoolData.value || schoolData.value.length === 0) {
        return [[], [], []];
      }
      const schools = schoolData.value.map((item) => item.name);
      const colleges = (((_a = schoolData.value[multiIndex.value[0]]) == null ? void 0 : _a.colleges) || []).map((item) => item.name);
      const classes = (((_d = (_c = (_b = schoolData.value[multiIndex.value[0]]) == null ? void 0 : _b.colleges) == null ? void 0 : _c[multiIndex.value[1]]) == null ? void 0 : _d.classes) || []).map((item) => item.name);
      return [schools, colleges, classes];
    });
    const initMultiIndex = () => {
      if (userInfo.value.schoolName && userInfo.value.collegeName && userInfo.value.className && schoolData.value.length > 0) {
        const schoolIndex = schoolData.value.findIndex((school) => school.name === userInfo.value.schoolName);
        if (schoolIndex !== -1) {
          const colleges = schoolData.value[schoolIndex].colleges || [];
          const collegeIndex = colleges.findIndex((college) => college.name === userInfo.value.collegeName);
          if (collegeIndex !== -1) {
            const classes = colleges[collegeIndex].classes || [];
            const classIndex = classes.findIndex((cls) => cls.name === userInfo.value.className);
            if (classIndex !== -1) {
              multiIndex.value = [schoolIndex, collegeIndex, classIndex];
              return;
            }
          }
        }
      }
      multiIndex.value = [0, 0, 0];
    };
    async function getSchoolInfoTree() {
      try {
        let res = await api_school_index.apiGetSchoolInfoTree();
        schoolData.value = res.data.items || [];
        initMultiIndex();
      } catch (e) {
        common_vendor.index.__f__("error", "at pages/user/userInfo/userInfo.vue:129", "获取学校信息失败", e);
      }
    }
    common_vendor.onMounted(() => {
      getSchoolInfoTree();
    });
    function upload() {
      common_vendor.index.chooseImage({
        count: 1,
        success(e) {
          userAvatar.value = e.tempFilePaths[0];
          filesName.value = e.tempFiles[0].name;
        }
      });
    }
    function editField(field, label, currentValue, isPassword = false) {
      common_vendor.index.showModal({
        title: `编辑${label}`,
        editable: true,
        placeholderText: `请输入${label}`,
        content: currentValue,
        success: (res) => {
          if (res.confirm && res.content !== void 0) {
            const newValue = res.content.trim();
            if (field === "phone" && newValue && !/^1[3-9]\d{9}$/.test(newValue)) {
              common_vendor.index.showToast({
                title: "手机号格式不正确",
                icon: "none"
              });
              return;
            }
            if (field === "email" && newValue && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newValue)) {
              common_vendor.index.showToast({
                title: "邮箱格式不正确",
                icon: "none"
              });
              return;
            }
            if (field === "realName" && !newValue) {
              common_vendor.index.showToast({
                title: "姓名不能为空",
                icon: "none"
              });
              return;
            }
            userInfo.value[field] = newValue;
            common_vendor.index.showToast({
              title: "修改成功",
              icon: "success"
            });
          }
        }
      });
    }
    function editGender() {
      common_vendor.index.showActionSheet({
        itemList: ["男", "女"],
        success: (res) => {
          userInfo.value.gender = res.tapIndex === 0 ? 1 : 0;
          common_vendor.index.showToast({
            title: "修改成功",
            icon: "success"
          });
        }
      });
    }
    function onPickerChange(e) {
      const values = e.detail.value;
      multiIndex.value = values;
      const schoolIndex = values[0];
      const collegeIndex = values[1];
      const classIndex = values[2];
      const school = schoolData.value[schoolIndex];
      if (school) {
        userInfo.value.schoolName = school.name;
        const college = (school.colleges || [])[collegeIndex];
        if (college) {
          userInfo.value.collegeName = college.name;
          const cls = (college.classes || [])[classIndex];
          if (cls) {
            userInfo.value.className = cls.name;
          } else {
            userInfo.value.className = "";
          }
        } else {
          userInfo.value.collegeName = "";
          userInfo.value.className = "";
        }
      }
      common_vendor.index.showToast({
        title: "修改成功",
        icon: "success"
      });
    }
    function onPickerColumnChange(e) {
      const column = e.detail.column;
      const value = e.detail.value;
      const newIndex = [...multiIndex.value];
      newIndex[column] = value;
      if (column === 0) {
        newIndex[1] = 0;
        newIndex[2] = 0;
      } else if (column === 1) {
        newIndex[2] = 0;
      }
      const schools = schoolData.value || [];
      if (!schools[newIndex[0]] || !(schools[newIndex[0]].colleges || []).length) {
        newIndex[1] = 0;
        newIndex[2] = 0;
      } else {
        const colleges = schools[newIndex[0]].colleges || [];
        if (!colleges[newIndex[1]] || !(colleges[newIndex[1]].classes || []).length) {
          newIndex[2] = 0;
        }
      }
      multiIndex.value = newIndex;
    }
    async function saveChanges() {
      if (!userInfo.value.realName) {
        common_vendor.index.showToast({
          title: "请输入姓名",
          icon: "none"
        });
        return;
      }
      common_vendor.index.showLoading({
        title: "保存中..."
      });
      try {
        await new Promise((resolve, reject) => {
          common_vendor.tr.uploadFile({
            filePath: userAvatar.value,
            cloudPath: `avatar/${(/* @__PURE__ */ new Date()).getTime()}_${filesName.value}`,
            fileType: "image",
            success: (e) => {
              let filePath = utils_convertCloudPath.convertCloudPath(e.fileID);
              userInfo.value.avatarUrl = filePath;
              resolve();
            },
            fail: (err) => reject(err)
          });
        });
        common_vendor.index.__f__("log", "at pages/user/userInfo/userInfo.vue:306", userInfo.value.avatarUrl);
        let res = await api_user_index.apiImproveUserInfo(userInfo.value.id, userInfo.value);
        common_vendor.index.hideLoading();
        if (res.code === 200) {
          common_vendor.index.setStorageSync("userInfo", res.data.user);
          common_vendor.index.showToast({
            title: "保存成功",
            icon: "success"
          });
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/pages/user/user"
            });
          }, 1500);
        } else {
          common_vendor.index.showToast({
            title: res.message || "保存失败",
            icon: "none"
          });
        }
      } catch (e) {
        common_vendor.index.hideLoading();
        const errorMsg = e.message || e.errMsg || "保存失败";
        common_vendor.index.showToast({
          title: errorMsg,
          icon: "none"
        });
        common_vendor.index.__f__("error", "at pages/user/userInfo/userInfo.vue:335", "保存失败", e);
      }
    }
    return (_ctx, _cache) => {
      return {
        a: userAvatar.value,
        b: common_vendor.o(upload),
        c: common_vendor.o(($event) => editField("realName", "姓名", userInfo.value.realName)),
        d: common_vendor.p({
          title: "姓名",
          clickable: true,
          ["right-text"]: userInfo.value.realName
        }),
        e: common_vendor.o(editGender),
        f: common_vendor.p({
          title: "性别",
          clickable: true,
          ["right-text"]: userInfo.value.gender === 1 ? "男" : "女"
        }),
        g: common_vendor.p({
          title: "学校",
          ["right-text"]: userInfo.value.schoolName
        }),
        h: multiArray.value,
        i: multiIndex.value,
        j: common_vendor.o(onPickerChange),
        k: common_vendor.o(onPickerColumnChange),
        l: common_vendor.p({
          title: "学院",
          ["right-text"]: userInfo.value.collegeName
        }),
        m: multiArray.value,
        n: multiIndex.value,
        o: common_vendor.o(onPickerChange),
        p: common_vendor.o(onPickerColumnChange),
        q: common_vendor.p({
          title: "班级",
          ["right-text"]: userInfo.value.className
        }),
        r: multiArray.value,
        s: multiIndex.value,
        t: common_vendor.o(onPickerChange),
        v: common_vendor.o(onPickerColumnChange),
        w: common_vendor.o(($event) => editField("password", "密码", "", true)),
        x: common_vendor.p({
          title: "密码",
          clickable: true,
          ["right-text"]: userInfo.value.password ? "******" : ""
        }),
        y: common_vendor.o(($event) => editField("phone", "手机号", userInfo.value.phone)),
        z: common_vendor.p({
          title: "手机号",
          clickable: true,
          ["right-text"]: userInfo.value.phone
        }),
        A: common_vendor.o(($event) => editField("email", "邮箱", userInfo.value.email)),
        B: common_vendor.p({
          title: "邮箱",
          clickable: true,
          ["right-text"]: userInfo.value.email
        }),
        C: common_vendor.o(saveChanges)
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-0b0fe2f0"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../../.sourcemap/mp-weixin/pages/user/userInfo/userInfo.js.map
