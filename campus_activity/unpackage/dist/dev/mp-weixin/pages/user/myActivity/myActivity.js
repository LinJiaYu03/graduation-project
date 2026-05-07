"use strict";
const common_vendor = require("../../../common/vendor.js");
const api_activity_index = require("../../../api/activity/index.js");
if (!Math) {
  (comSearch + comActivityItem + comActivityItemManaged)();
}
const comSearch = () => "../../../components/com-search/com-search.js";
const comActivityItem = () => "./components/com-activity-item/com-activity-item.js";
const comActivityItemManaged = () => "./components/com-activity-item-managed/com-activity-item-managed2.js";
const _sfc_main = {
  __name: "myActivity",
  setup(__props) {
    const searchValue = common_vendor.ref("");
    const activeTab = common_vendor.ref("participated");
    const userInfo = common_vendor.index.getStorageSync("userInfo");
    const userId = userInfo.id;
    const isManager = userInfo.isBoss || userInfo.isManager;
    const activity_participated = common_vendor.ref([]);
    const activity_managed = common_vendor.ref([]);
    const tabs = common_vendor.computed(() => {
      if (isManager) {
        return [
          { label: "参与", value: "participated" },
          { label: "管理", value: "managed" }
        ];
      }
      return [{ label: "参与", value: "participated" }];
    });
    function onSearch() {
      getJoinOrManangeActivityList();
    }
    function OnChangeActiveTab(tab) {
      if (!isManager && tab === "managed")
        return;
      activeTab.value = tab;
      getJoinOrManangeActivityList();
    }
    async function getJoinOrManangeActivityList() {
      let res = await api_activity_index.apiGetJoinOrManangeActivity({
        id: userId,
        type: activeTab.value,
        keyword: searchValue.value
      });
      if (res.code == 200) {
        let {
          activities
        } = res.data;
        activeTab.value === "participated" ? activity_participated.value = activities : activity_managed.value = activities;
      }
    }
    common_vendor.onShow(() => {
      getJoinOrManangeActivityList();
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.o(onSearch),
        b: common_vendor.o(($event) => searchValue.value = $event),
        c: common_vendor.p({
          value: searchValue.value
        }),
        d: common_vendor.f(tabs.value, (tab, k0, i0) => {
          return {
            a: common_vendor.t(tab.label),
            b: tab.value,
            c: activeTab.value === tab.value ? 1 : "",
            d: common_vendor.o(($event) => OnChangeActiveTab(tab.value), tab.value)
          };
        }),
        e: activeTab.value === "participated"
      }, activeTab.value === "participated" ? {
        f: common_vendor.f(activity_participated.value, (item, k0, i0) => {
          return {
            a: item.id,
            b: "73e68555-1-" + i0,
            c: common_vendor.p({
              activeInfo: item
            })
          };
        })
      } : {
        g: common_vendor.f(activity_managed.value, (item, k0, i0) => {
          return {
            a: item.id,
            b: common_vendor.o(getJoinOrManangeActivityList, item.id),
            c: "73e68555-2-" + i0,
            d: common_vendor.p({
              activeInfo: item
            })
          };
        })
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-73e68555"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../../.sourcemap/mp-weixin/pages/user/myActivity/myActivity.js.map
