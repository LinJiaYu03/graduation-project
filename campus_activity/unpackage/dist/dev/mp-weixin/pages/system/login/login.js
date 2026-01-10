"use strict";
const common_vendor = require("../../../common/vendor.js");
const api_user_index = require("../../../api/user/index.js");
if (!Array) {
  const _easycom_uni_forms_item2 = common_vendor.resolveComponent("uni-forms-item");
  const _easycom_uni_forms2 = common_vendor.resolveComponent("uni-forms");
  (_easycom_uni_forms_item2 + _easycom_uni_forms2)();
}
const _easycom_uni_forms_item = () => "../../../uni_modules/uni-forms/components/uni-forms-item/uni-forms-item.js";
const _easycom_uni_forms = () => "../../../uni_modules/uni-forms/components/uni-forms/uni-forms.js";
if (!Math) {
  (_easycom_uni_forms_item + _easycom_uni_forms)();
}
const _sfc_main = {
  __name: "login",
  setup(__props) {
    const form = common_vendor.ref(null);
    const formData = common_vendor.reactive({
      username: "",
      password: ""
    });
    const rules = {
      username: {
        rules: [{
          required: true,
          errorMessage: "请输入账号"
        }]
      },
      password: {
        rules: [
          {
            required: true,
            errorMessage: "请输入密码"
          },
          {
            minLength: 6,
            errorMessage: "密码至少6位"
          }
        ]
      }
    };
    const onInput = (name, e) => {
      const value = e.detail ? e.detail.value : e.target.value;
      formData[name] = value;
      if (form.value) {
        form.value.setValue(name, value);
      }
    };
    const handleLogin = async () => {
      await form.value.validate();
      let res = await api_user_index.apiUserLogin(formData);
      if (res.code === 200) {
        handleLoginSuccess(res.data.user);
      }
    };
    const handleWxLogin = () => {
      common_vendor.index.login({
        provider: "weixin",
        success: async (loginRes) => {
          if (loginRes.code) {
            try {
              let res = await api_user_index.apiUserWxLogin({
                code: loginRes.code
              });
              if (res.code === 200) {
                handleLoginSuccess(res.data.user);
              }
            } catch (e) {
              common_vendor.index.showToast({
                title: "微信登录失败",
                icon: "none"
              });
            }
          }
        }
      });
    };
    const handleLoginSuccess = (user) => {
      const token = user.token;
      if (user.isCompleted) {
        common_vendor.index.setStorageSync("token", token);
        common_vendor.index.setStorageSync("userInfo", user);
        common_vendor.index.showToast({
          title: "登录成功",
          icon: "success"
        });
        common_vendor.index.reLaunch({
          url: "/pages/index/index"
        });
      } else {
        common_vendor.index.setStorageSync("token", token);
        common_vendor.index.navigateTo({
          url: `/pages/system/userInfo/userInfo?id=${user.id}`,
          success() {
            common_vendor.index.showToast({
              title: "请先完善个人信息",
              icon: "none"
            });
          }
        });
      }
    };
    const goToRegister = () => {
      common_vendor.index.navigateTo({
        url: "/pages/system/registration/registration"
      });
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.o([($event) => formData.username = $event.detail.value, ($event) => onInput("username", $event)]),
        b: formData.username,
        c: common_vendor.p({
          label: "账号",
          name: "username",
          required: true
        }),
        d: common_vendor.o([($event) => formData.password = $event.detail.value, ($event) => onInput("password", $event)]),
        e: formData.password,
        f: common_vendor.p({
          label: "密码",
          name: "password",
          required: true
        }),
        g: common_vendor.sr(form, "858729ca-0", {
          "k": "form"
        }),
        h: common_vendor.p({
          rules,
          modelValue: formData,
          ["label-position"]: "top"
        }),
        i: common_vendor.o(handleLogin),
        j: common_vendor.o(goToRegister),
        k: common_vendor.o(handleWxLogin)
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-858729ca"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../../.sourcemap/mp-weixin/pages/system/login/login.js.map
