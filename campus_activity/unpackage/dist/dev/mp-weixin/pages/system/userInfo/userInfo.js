"use strict";
const common_vendor = require("../../../common/vendor.js");
const api_school_index = require("../../../api/school/index.js");
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
  __name: "userInfo",
  setup(__props) {
    const form = common_vendor.ref(null);
    const formData = common_vendor.reactive({
      realName: "",
      studentNo: "",
      schoolName: "",
      collegeName: "",
      className: "",
      gender: "1",
      phone: "",
      email: ""
    });
    const userId = common_vendor.ref();
    const schoolData = common_vendor.ref([]);
    const initMultiIndex = () => {
      if (formData.schoolName && formData.collegeName && formData.className && schoolData.value.length > 0) {
        const schoolIndex = schoolData.value.findIndex((school) => school.name === formData.schoolName);
        if (schoolIndex !== -1) {
          const colleges = schoolData.value[schoolIndex].colleges || [];
          const collegeIndex = colleges.findIndex((college) => college.name === formData.collegeName);
          if (collegeIndex !== -1) {
            const classes = colleges[collegeIndex].classes || [];
            const classIndex = classes.findIndex((cls) => cls.name === formData.className);
            if (classIndex !== -1) {
              return [schoolIndex, collegeIndex, classIndex];
            }
          }
        }
      }
      return [0, 0, 0];
    };
    const multiIndex = common_vendor.ref(initMultiIndex());
    const multiArray = common_vendor.computed(() => {
      var _a, _b, _c, _d;
      if (!schoolData.value || schoolData.value.length === 0) {
        return [
          [],
          [],
          []
        ];
      }
      const schools = schoolData.value.map((item) => item.name);
      const colleges = (((_a = schoolData.value[multiIndex.value[0]]) == null ? void 0 : _a.colleges) || []).map((item) => item.name);
      const classes = (((_d = (_c = (_b = schoolData.value[multiIndex.value[0]]) == null ? void 0 : _b.colleges) == null ? void 0 : _c[multiIndex.value[1]]) == null ? void 0 : _d.classes) || []).map(
        (item) => item.name
      );
      return [schools, colleges, classes];
    });
    const pickerDisplayText = common_vendor.computed(() => {
      if (!formData.schoolName || !formData.collegeName || !formData.className) {
        return "";
      }
      return `${formData.schoolName} - ${formData.collegeName} - ${formData.className}`;
    });
    const rules = {
      realName: {
        rules: [{
          required: true,
          errorMessage: "请输入姓名"
        }]
      },
      studentNo: {
        rules: [
          {
            required: true,
            errorMessage: "请输入学号"
          },
          {
            pattern: /^\d+$/,
            errorMessage: "学号格式不正确，只能输入数字"
          }
        ]
      },
      gender: {
        rules: [{
          required: true,
          errorMessage: "请选择性别"
        }]
      },
      schoolInfo: {
        rules: [{
          validateFunction: (rule, value, data, callback) => {
            if (!formData.schoolName || !formData.collegeName || !formData.className) {
              callback("请选择学校、学院、班级");
            }
            return true;
          }
        }]
      },
      phone: {
        rules: [{
          validateFunction: (rule, value, data, callback) => {
            if (value && !/^1[3-9]\d{9}$/.test(value)) {
              callback("手机号格式不正确");
            }
            return true;
          }
        }]
      },
      email: {
        rules: [{
          validateFunction: (rule, value, data, callback) => {
            if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
              callback("邮箱格式不正确");
            }
            return true;
          }
        }]
      }
    };
    const onInput = (name, e) => {
      const value = e.detail ? e.detail.value : e.target.value;
      formData[name] = value;
      if (form.value) {
        form.value.setValue(name, value);
      }
    };
    const onGenderChange = (e) => {
      formData.gender = e.detail.value;
      if (form.value) {
        form.value.setValue("gender", e.detail.value);
      }
    };
    const onPickerChange = (e) => {
      const values = e.detail.value;
      multiIndex.value = values;
      const schoolIndex = values[0];
      const collegeIndex = values[1];
      const classIndex = values[2];
      const school = schoolData.value[schoolIndex];
      if (school) {
        formData.schoolName = school.name;
        const college = (school.colleges || [])[collegeIndex];
        if (college) {
          formData.collegeName = college.name;
          const cls = (college.classes || [])[classIndex];
          if (cls) {
            formData.className = cls.name;
          } else {
            formData.className = "";
          }
        } else {
          formData.collegeName = "";
          formData.className = "";
        }
      }
      if (form.value) {
        form.value.setValue("schoolInfo", pickerDisplayText.value);
      }
    };
    const onPickerColumnChange = (e) => {
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
    };
    const handleSubmit = async () => {
      try {
        await form.value.validate();
        let res = await api_user_index.apiImproveUserInfo(userId.value, formData);
        if (res.code === 200) {
          common_vendor.index.__f__("log", "at pages/system/userInfo/userInfo.vue:286", res.data);
          common_vendor.index.setStorageSync("userInfo", res.data.user);
          common_vendor.index.setStorageSync("token", res.data.user.token);
          common_vendor.index.showToast({
            title: "保存成功",
            icon: "success"
          });
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/pages/system/login/login"
            });
          }, 1500);
        }
      } catch (e) {
        common_vendor.index.__f__("log", "at pages/system/userInfo/userInfo.vue:302", "表单校验失败", e);
      }
    };
    async function getSchoolInfoTree() {
      let res = await api_school_index.apiGetSchoolInfoTree();
      schoolData.value = res.data.items || [];
      multiIndex.value = initMultiIndex();
    }
    common_vendor.onMounted(async () => {
      getSchoolInfoTree();
    });
    common_vendor.onLoad((e) => {
      userId.value = e.id;
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.o([($event) => formData.realName = $event.detail.value, ($event) => onInput("realName", $event)]),
        b: formData.realName,
        c: common_vendor.p({
          label: "姓名",
          name: "realName",
          required: true
        }),
        d: common_vendor.o([($event) => formData.studentNo = $event.detail.value, ($event) => onInput("studentNo", $event)]),
        e: formData.studentNo,
        f: common_vendor.p({
          label: "学号",
          name: "studentNo",
          required: true
        }),
        g: formData.gender === "1",
        h: formData.gender === "0",
        i: common_vendor.o(onGenderChange),
        j: common_vendor.p({
          label: "性别",
          name: "gender",
          required: true
        }),
        k: common_vendor.t(pickerDisplayText.value || "请选择学校、学院、班级"),
        l: common_vendor.n(pickerDisplayText.value ? "picker-text" : "picker-placeholder"),
        m: multiArray.value,
        n: multiIndex.value,
        o: common_vendor.o(onPickerChange),
        p: common_vendor.o(onPickerColumnChange),
        q: common_vendor.p({
          label: "学校/学院/班级",
          name: "schoolInfo",
          required: true
        }),
        r: common_vendor.o([($event) => formData.phone = $event.detail.value, ($event) => onInput("phone", $event)]),
        s: formData.phone,
        t: common_vendor.p({
          label: "手机号",
          name: "phone"
        }),
        v: common_vendor.o([($event) => formData.email = $event.detail.value, ($event) => onInput("email", $event)]),
        w: formData.email,
        x: common_vendor.p({
          label: "邮箱",
          name: "email"
        }),
        y: common_vendor.sr(form, "8f1c05e6-0", {
          "k": "form"
        }),
        z: common_vendor.p({
          rules,
          modelValue: formData,
          ["label-position"]: "top",
          ["label-width"]: "120"
        }),
        A: common_vendor.o(handleSubmit)
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-8f1c05e6"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../../.sourcemap/mp-weixin/pages/system/userInfo/userInfo.js.map
