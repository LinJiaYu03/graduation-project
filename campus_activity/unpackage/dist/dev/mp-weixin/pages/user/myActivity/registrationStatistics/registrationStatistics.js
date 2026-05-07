"use strict";
const common_vendor = require("../../../../common/vendor.js");
const api_activity_index = require("../../../../api/activity/index.js");
if (!Array) {
  const _easycom_l_echart2 = common_vendor.resolveComponent("l-echart");
  _easycom_l_echart2();
}
const _easycom_l_echart = () => "../../../../uni_modules/lime-echart/components/l-echart/l-echart.js";
if (!Math) {
  _easycom_l_echart();
}
const _sfc_main = {
  __name: "registrationStatistics",
  props: ["id"],
  setup(__props) {
    const props = __props;
    const managerUserId = common_vendor.index.getStorageSync("userInfo").id;
    const registrationChartRef = common_vendor.ref(null);
    const checkinChartRef = common_vendor.ref(null);
    const scoreChartRef = common_vendor.ref(null);
    const activityInfo = common_vendor.ref({});
    const registrationData = common_vendor.ref({
      pending: 0,
      approved: 0,
      rejected: 0,
      total: 0,
      maxParticipants: 0,
      currentParticipants: 0
    });
    const checkinData = common_vendor.ref({
      checkedIn: 0,
      notCheckedIn: 0,
      totalApproved: 0,
      checkinRate: 0
    });
    const scoreData = common_vendor.ref({
      scoreDistribution: {
        "0.5-1.0": 0,
        "1.5-2.0": 0,
        "2.5-3.0": 0,
        "3.5-4.0": 0,
        "4.5-5.0": 0
      },
      averageScore: 0,
      scoredCount: 0,
      notScoredCount: 0,
      totalApproved: 0,
      scoreRate: 0
    });
    const echarts = require("../../../../static/echarts.min.js");
    const getActivityStatistics = async () => {
      const registrationResponse = await api_activity_index.apiGetRegistrationStatistics({
        activityId: props.id,
        managerUserId
      });
      if (registrationResponse.code === 200) {
        const statistics = registrationResponse.data.statistics;
        activityInfo.value = statistics.activityInfo;
        registrationData.value = {
          pending: statistics.statusStats.pending,
          approved: statistics.statusStats.approved,
          rejected: statistics.statusStats.rejected,
          total: statistics.statusStats.total,
          maxParticipants: statistics.maxParticipants,
          currentParticipants: statistics.currentParticipants
        };
        await initRegistrationChart();
      }
      const checkinResponse = await api_activity_index.apiGetCheckinStatistics({
        activityId: props.id,
        managerUserId
      });
      if (checkinResponse.code === 200) {
        const statistics = checkinResponse.data.statistics;
        checkinData.value = {
          checkedIn: statistics.checkedIn,
          notCheckedIn: statistics.notCheckedIn,
          totalApproved: statistics.totalApproved,
          checkinRate: statistics.checkinRate
        };
        await initCheckinChart();
      }
      const scoreResponse = await api_activity_index.apiGetScoreStatistics({
        activityId: props.id,
        managerUserId
      });
      if (scoreResponse.code === 200) {
        const statistics = scoreResponse.data.statistics;
        scoreData.value = {
          scoreDistribution: statistics.scoreDistribution,
          averageScore: statistics.averageScore,
          scoredCount: statistics.scoredCount,
          notScoredCount: statistics.notScoredCount,
          totalApproved: statistics.totalApproved,
          scoreRate: statistics.scoreRate
        };
        await initScoreChart();
      }
    };
    const createRegistrationPieChartOption = () => {
      return {
        title: {
          left: "center",
          textStyle: {
            fontSize: 16
          }
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} {b}: {c} ({d}%)"
        },
        legend: {
          orient: "horizontal",
          bottom: "5%",
          data: ["待审核", "已通过", "已拒绝"]
        },
        series: [{
          name: "报名状态",
          type: "pie",
          radius: ["40%", "70%"],
          data: [
            {
              value: registrationData.value.pending,
              name: "待审核"
            },
            {
              value: registrationData.value.approved,
              name: "已通过"
            },
            {
              value: registrationData.value.rejected,
              name: "已拒绝"
            }
          ],
          color: ["#FFA500", "#52C41A", "#FF4D4F"],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)"
            }
          }
        }]
      };
    };
    const createCheckinPieChartOption = () => {
      return {
        title: {
          left: "center",
          textStyle: {
            fontSize: 16
          }
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} {b}: {c} ({d}%)"
        },
        legend: {
          orient: "horizontal",
          bottom: "5%",
          data: ["已签到", "未签到"]
        },
        series: [{
          name: "签到状态",
          type: "pie",
          radius: ["40%", "70%"],
          data: [
            {
              value: checkinData.value.checkedIn,
              name: "已签到"
            },
            {
              value: checkinData.value.notCheckedIn,
              name: "未签到"
            }
          ],
          color: ["#52C41A", "#FFA500"],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)"
            }
          }
        }]
      };
    };
    const createScoreBarChartOption = () => {
      return {
        title: {
          left: "center",
          textStyle: {
            fontSize: 16
          }
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow"
          }
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        xAxis: {
          type: "category",
          data: ["0.5-1.0", "1.5-2.0", "2.5-3.0", "3.5-4.0", "4.5-5.0"]
        },
        yAxis: {
          type: "value",
          name: "人数"
        },
        series: [{
          name: "评分分布",
          type: "bar",
          data: [
            scoreData.value.scoreDistribution["0.5-1.0"],
            scoreData.value.scoreDistribution["1.5-2.0"],
            scoreData.value.scoreDistribution["2.5-3.0"],
            scoreData.value.scoreDistribution["3.5-4.0"],
            scoreData.value.scoreDistribution["4.5-5.0"]
          ],
          itemStyle: {
            color: function(params) {
              const colors = ["#FF4D4F", "#FF7A45", "#FFA500", "#52C41A", "#1890FF"];
              return colors[params.dataIndex];
            }
          },
          label: {
            show: true,
            position: "top"
          }
        }]
      };
    };
    const initRegistrationChart = async () => {
      if (!registrationChartRef.value)
        return;
      try {
        const chart = await registrationChartRef.value.init(echarts);
        const option = createRegistrationPieChartOption();
        chart.setOption(option);
      } catch (error) {
        common_vendor.index.__f__("error", "at pages/user/myActivity/registrationStatistics/registrationStatistics.vue:333", "报名图表初始化失败:", error);
      }
    };
    const initCheckinChart = async () => {
      if (!checkinChartRef.value)
        return;
      try {
        const chart = await checkinChartRef.value.init(echarts);
        const option = createCheckinPieChartOption();
        chart.setOption(option);
      } catch (error) {
        common_vendor.index.__f__("error", "at pages/user/myActivity/registrationStatistics/registrationStatistics.vue:346", "签到图表初始化失败:", error);
      }
    };
    const initScoreChart = async () => {
      if (!scoreChartRef.value)
        return;
      try {
        const chart = await scoreChartRef.value.init(echarts);
        const option = createScoreBarChartOption();
        chart.setOption(option);
      } catch (error) {
        common_vendor.index.__f__("error", "at pages/user/myActivity/registrationStatistics/registrationStatistics.vue:359", "评分图表初始化失败:", error);
      }
    };
    const handleExportRegistration = () => {
      api_activity_index.apiExportRegistration(props.id, managerUserId);
    };
    const handleExportCheckin = () => {
      api_activity_index.apiExportCheckin(props.id, managerUserId);
    };
    const handleExportScore = () => {
      api_activity_index.apiExportScore(props.id, managerUserId);
    };
    common_vendor.onMounted(() => {
      getActivityStatistics();
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.o(handleExportRegistration),
        b: common_vendor.o(handleExportCheckin),
        c: common_vendor.o(handleExportScore),
        d: common_vendor.sr(registrationChartRef, "cee11be1-0", {
          "k": "registrationChartRef"
        }),
        e: common_vendor.o(initRegistrationChart),
        f: common_vendor.t(registrationData.value.total || 0),
        g: common_vendor.t(registrationData.value.currentParticipants || 0),
        h: common_vendor.t(registrationData.value.maxParticipants || 0),
        i: common_vendor.sr(checkinChartRef, "cee11be1-1", {
          "k": "checkinChartRef"
        }),
        j: common_vendor.o(initCheckinChart),
        k: common_vendor.t(checkinData.value.checkedIn || 0),
        l: common_vendor.t(checkinData.value.notCheckedIn || 0),
        m: common_vendor.t(checkinData.value.checkinRate || 0),
        n: common_vendor.sr(scoreChartRef, "cee11be1-2", {
          "k": "scoreChartRef"
        }),
        o: common_vendor.o(initScoreChart),
        p: common_vendor.t(scoreData.value.averageScore || 0),
        q: common_vendor.t(scoreData.value.scoredCount || 0),
        r: common_vendor.t(scoreData.value.notScoredCount || 0),
        s: common_vendor.t(scoreData.value.scoreRate || 0)
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-cee11be1"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../../../.sourcemap/mp-weixin/pages/user/myActivity/registrationStatistics/registrationStatistics.js.map
