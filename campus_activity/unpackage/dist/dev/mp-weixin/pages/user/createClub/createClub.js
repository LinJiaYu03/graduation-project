"use strict";
const common_vendor = require("../../../common/vendor.js");
const utils_convertCloudPath = require("../../../utils/convertCloudPath.js");
const api_club_index = require("../../../api/club/index.js");
if (!Array) {
  const _easycom_uni_file_picker2 = common_vendor.resolveComponent("uni-file-picker");
  const _easycom_uni_forms_item2 = common_vendor.resolveComponent("uni-forms-item");
  const _easycom_uni_tag2 = common_vendor.resolveComponent("uni-tag");
  const _easycom_uni_forms2 = common_vendor.resolveComponent("uni-forms");
  (_easycom_uni_file_picker2 + _easycom_uni_forms_item2 + _easycom_uni_tag2 + _easycom_uni_forms2)();
}
const _easycom_uni_file_picker = () => "../../../uni_modules/uni-file-picker/components/uni-file-picker/uni-file-picker.js";
const _easycom_uni_forms_item = () => "../../../uni_modules/uni-forms/components/uni-forms-item/uni-forms-item.js";
const _easycom_uni_tag = () => "../../../uni_modules/uni-tag/components/uni-tag/uni-tag.js";
const _easycom_uni_forms = () => "../../../uni_modules/uni-forms/components/uni-forms/uni-forms.js";
if (!Math) {
  (_easycom_uni_file_picker + _easycom_uni_forms_item + _easycom_uni_tag + _easycom_uni_forms)();
}
const _sfc_main = {
  __name: "createClub",
  setup(__props) {
    const levelTags = ["班级", "院级", "校级"];
    const availableTags = ["团支部", "音乐", "文艺", "传媒", "社团与协会", "公益志愿"];
    const formRef = common_vendor.ref(null);
    const form = common_vendor.reactive({
      iconUrl: [],
      name: "",
      description: "",
      levelTag: "",
      tags: []
    });
    const coverImageUrl = common_vendor.ref("");
    const filesName = common_vendor.ref("");
    const filePath = common_vendor.ref("");
    function isTagSelected(tagValue) {
      return form.tags.includes(tagValue);
    }
    function toggleTag(tagValue) {
      const index = form.tags.indexOf(tagValue);
      if (index > -1) {
        form.tags.splice(index, 1);
      } else {
        form.tags.push(tagValue);
      }
    }
    function toggleLevelTag(value) {
      form.levelTag = value;
    }
    const rules = {
      iconUrl: {
        required: true,
        errorMessage: "请上传封面图片",
        validator: (rule, value, callback) => {
          if (!Array.isArray(value) || value.length < 1) {
            callback("请至少上传1张封面图片");
            return;
          }
          callback();
        }
      },
      name: {
        required: true,
        errorMessage: "请输入活动名称"
      },
      description: {
        required: true,
        errorMessage: "请输入活动简介",
        validator: (rule, value, callback) => {
          if (!value || value.trim().length === 0) {
            callback("请输入活动简介");
            return;
          }
          if (value.length < 10) {
            callback("活动简介至少需要10个字符");
            return;
          }
          callback();
        }
      },
      tags: {
        required: true,
        errorMessage: "请至少选择1个标签",
        validator: (rule, value, callback) => {
          if (!Array.isArray(value) || value.length < 1) {
            callback("请至少选择1个标签");
            return;
          }
          callback();
        }
      }
    };
    function select(e) {
      coverImageUrl.value = e.tempFilePaths[0];
      filesName.value = e.tempFiles[0].name;
    }
    async function handleSubmit() {
      formRef.value.validate().then(async () => {
        common_vendor.index.showLoading({
          title: "提交中..."
        });
        try {
          if (coverImageUrl.value) {
            await new Promise((resolve, reject) => {
              common_vendor.tr.uploadFile({
                filePath: coverImageUrl.value,
                cloudPath: `club/${(/* @__PURE__ */ new Date()).getTime()}_${filesName.value}`,
                fileType: "image",
                success: (e) => {
                  filePath.value = utils_convertCloudPath.convertCloudPath(e.fileID);
                  resolve();
                }
              });
            });
          }
          const userInfo = common_vendor.index.getStorageSync("userInfo");
          const formData = {
            name: form.name,
            description: form.description || void 0,
            levelTag: form.levelTag,
            tags: form.tags.length > 0 ? form.tags.join(",") : void 0,
            userId: userInfo == null ? void 0 : userInfo.id
          };
          if (filePath.value) {
            formData.iconUrl = filePath.value;
          }
          const res = await api_club_index.apiCreateClub(formData);
          common_vendor.index.hideLoading();
          if (res.code === 200) {
            common_vendor.index.showToast({
              title: "创建成功",
              icon: "success"
            });
            setTimeout(() => {
              common_vendor.index.reLaunch({
                url: "/pages/user/user"
              });
            }, 1500);
          } else {
            common_vendor.index.showToast({
              title: res.message || "创建失败",
              icon: "none"
            });
          }
        } catch (e) {
          common_vendor.index.hideLoading();
          common_vendor.index.showToast({
            title: "创建失败",
            icon: "none"
          });
          common_vendor.index.__f__("error", "at pages/user/createClub/createClub.vue:217", "创建社团失败", e);
        }
      }).catch((err) => {
        common_vendor.index.__f__("warn", "at pages/user/createClub/createClub.vue:221", "表单校验未通过", err);
      });
    }
    return (_ctx, _cache) => {
      return {
        a: common_vendor.o(select),
        b: common_vendor.o(($event) => form.iconUrl = $event),
        c: common_vendor.p({
          fileMediatype: "image",
          limit: "1",
          ["auto-upload"]: false,
          mode: "grid",
          title: "上传图标",
          modelValue: form.iconUrl
        }),
        d: common_vendor.p({
          label: "社团图标",
          name: "iconUrl",
          required: true
        }),
        e: form.name,
        f: common_vendor.o(($event) => form.name = $event.detail.value),
        g: common_vendor.p({
          label: "社团名称",
          name: "name",
          required: true
        }),
        h: form.description,
        i: common_vendor.o(($event) => form.description = $event.detail.value),
        j: common_vendor.t(form.description.length),
        k: common_vendor.p({
          label: "社团简介",
          name: "description",
          required: true
        }),
        l: common_vendor.f(levelTags, (tag, index, i0) => {
          return {
            a: index,
            b: common_vendor.o(($event) => toggleLevelTag(tag), index),
            c: "dbf6d87f-6-" + i0 + ",dbf6d87f-5",
            d: common_vendor.p({
              text: tag,
              type: tag === form.levelTag ? "primary" : "default",
              inverted: !(tag === form.levelTag)
            })
          };
        }),
        m: common_vendor.p({
          label: "社团级别",
          name: "tags",
          required: true
        }),
        n: common_vendor.f(availableTags, (tag, index, i0) => {
          return {
            a: index,
            b: common_vendor.o(($event) => toggleTag(tag), index),
            c: "dbf6d87f-8-" + i0 + ",dbf6d87f-7",
            d: common_vendor.p({
              text: tag,
              type: isTagSelected(tag) ? "primary" : "default",
              inverted: !isTagSelected(tag)
            })
          };
        }),
        o: common_vendor.p({
          label: "社团标签",
          name: "tags",
          required: true
        }),
        p: common_vendor.sr(formRef, "dbf6d87f-0", {
          "k": "formRef"
        }),
        q: common_vendor.p({
          modelValue: form,
          rules,
          ["label-position"]: "top",
          ["label-width"]: "120",
          ["validate-trigger"]: "bind"
        }),
        r: common_vendor.o(handleSubmit)
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-dbf6d87f"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../../.sourcemap/mp-weixin/pages/user/createClub/createClub.js.map
