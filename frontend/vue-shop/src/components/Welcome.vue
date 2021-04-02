<template>
  <div class="main-container">
    <!-- 卡片视图区域 -->
    <el-card class="wrapper">
      <el-container>
        <el-main>
          <el-row type="flex" justify="space-around">
            <el-col :span="6"
              ><el-card shadow="hover" class="dataitem doneOrder">
                <div ref="doneOrderRef" class="cellbox">
                  <span class="labeltext">本月已完成订单</span>
                  <p class="theNumber">{{ doneOrderNumInThisMonth }}<span class="suffix"> 份</span></p>
                </div></el-card
              ></el-col
            >
            <el-col :span="6"
              ><el-card shadow="hover" class="dataitem totalSales">
                <div ref="totalSalesRef" class="cellbox">
                  <span class="labeltext">本月销售额</span>
                  <p class="theNumber">{{ totalSales }}<span class="suffix"> 元</span></p>
                </div></el-card
              ></el-col
            >
            <el-col :span="9">
              <el-card class="dataitem chartitem" shadow="hover">
                <div class="chartsContainer" ref="hotItemRef">本月热销商品种类饼状图</div>
              </el-card></el-col
            >
          </el-row>

          <el-row type="flex" justify="space-around">
            <el-col :span="6"
              ><el-card shadow="hover" class="dataitem unsendOrder">
                <div ref="unsendOrderRef" class="cellbox">
                  <span class="labeltext">本月未发货订单</span>
                  <p class="theNumber">{{ unsendOrderNumInThisMonth }}<span class="suffix"> 份</span></p>
                </div></el-card
              ></el-col
            >
            <el-col :span="6"
              ><el-card shadow="hover" class="dataitem unreceOrder">
                <div ref="unreceOrderRef" class="cellbox">
                  <span class="labeltext">本月未收货订单</span>
                  <p class="theNumber">{{ unreceOrderNumInThisMonth }}<span class="suffix"> 份</span></p>
                  
                </div></el-card
              ></el-col
            >
            <el-col :span="9">
              <el-card class="dataitem chartitem" shadow="hover">
                <div class="chartsContainer" ref="UserRef">近一年用户新增折线图</div>
              </el-card></el-col
            >
          </el-row>
        </el-main>
      </el-container>
      <el-container>
        <el-footer style="width: 100%; margin: 35px 0 20px 0">
          <el-card class="footerCard" shadow="hover">
            <div ref="orderRef" style="height: 260px">近一年订单折线图</div>
          </el-card>
        </el-footer>
      </el-container>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 图表对象
      hotItemChartInstance: null,
      userChartInstance: null,
      orderChartInstance: null,
      // 左上角4个数字数据
      // 本月完成订单数
      doneOrderNumInThisMonth: 0,
      // 本月销售额
      totalSales: 0,
      // 本月未发货订单数
      unsendOrderNumInThisMonth: 0,
      // 本月未收货订单数
      unreceOrderNumInThisMonth: 0,
      // 图表数据
      allData: null,
      // 近一年用户注册数
      // 本月销售商品种类比例
      //
    };
  },
  mounted() {
    this.getData();
    this.initChatrs();
    // window.addEventListener("resize", this.screenAdapter);
    // this.screenAdapter();
  },
  destroyed() {
    // window.removeEventListener("resize", this.screenAdapter);
  },
  methods: {
    // 初始化ECharts对象
    initChatrs() {
      this.hotItemChartInstance = this.$echarts.init(this.$refs.hotItemRef);
      this.userChartInstance = this.$echarts.init(this.$refs.UserRef);
      this.orderChartInstance = this.$echarts.init(this.$refs.orderRef);
      const hotItemChartOption = {
        title: {
          text: "本月热销商品分布图",
          left: "left",
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : <b>{c}</b> ({d}%)",
        },
        legend: [
          // {
          //   x: "center",
          //   y: "bottom",
          // },
        ],
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: true },
            restore: { show: false },
            saveAsImage: { show: true },
          },
        },
        series: [
          {
            type: "pie",
            radius: 50,
            center: ["25%", "50%"],
            // roseType: "radius",
            itemStyle: {
              // borderRadius: 5,
            },
            label: {
              show: true,
            },
            emphasis: {
              label: {
                show: true,
              },
            },
          },
          {
            type: "pie",
            radius: 50,
            center: ["75%", "50%"],
            // roseType: "radius",
            itemStyle: {
              // borderRadius: 5,
            },
          },
        ],
      };
      const userChartOption = {
        title: {
          text: "近一年新增用户趋势",
          left: "left",
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: true },
            restore: { show: false },
            saveAsImage: { show: true },
          },
        },
        tooltip: {
          trigger: 'axis',
          formatter: "{b} <br/> <b>{c}</b> 人",
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            type: "line",
            areaStyle: {},
          },
        ],
        grid: {
          top: 45,
          right: 45,
          bottom: 0,
          left: 30,
          containLabel: true,
        },
      };
      const orderChartOption = {
        tooltip: {
          trigger: "item",
          formatter: "{b} <br/> <b>{c}</b> 份订单",
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: true },
            restore: { show: false },
            saveAsImage: { show: true },
          },
        },
        title: {
          text: "近一年订单柱状图",
          left: "left",
        },
        xAxis: {
          type: "category",
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            type: "bar",
          },
        ],
        grid: {
          top: 45,
          right: 0,
          bottom: 0,
          left: 0,
          containLabel: true,
        },
      };
      this.hotItemChartInstance.setOption(hotItemChartOption);
      this.userChartInstance.setOption(userChartOption);
      this.orderChartInstance.setOption(orderChartOption);
    },
    // 获取服务器数据
    async getData() {
      const { data: res } = await this.$http.get("sold/");
      // 赋值左上方四个图的数据
      this.doneOrderNumInThisMonth = res.data.doneOrderNum;
      this.totalSales = res.data.totalSales;
      this.unsendOrderNumInThisMonth = res.data.unsendOrderNum;
      this.unreceOrderNumInThisMonth = res.data.unreceOrderNum;

      this.allData = res.data;
      // console.log(res.data);
      this.updateChart();
    },
    // 更新图表
    updateChart() {
      // 处理数据
      const orderDataxAx = this.allData.orderChart.map((item) => {
        return item.date;
      });
      const orderDatayAx = this.allData.orderChart.map((item) => {
        return item.count;
      });
      const userDataxAx = this.allData.userChart.map((item) => {
        return item.date;
      });
      const userDatayAx = this.allData.userChart.map((item) => {
        return item.count;
      });
      // 各图表数据对象
      const hotItemDataOption = {
        series: [
          { name: this.allData.soldChart[0].name, data: this.allData.soldChart[0].data },
          { name: this.allData.soldChart[1].name, data: this.allData.soldChart[1].data },
        ],
      };
      const userDataOption = {
        xAxis: {
          data: userDataxAx,
        },
        series: [
          {
            data: userDatayAx,
          },
        ],
      };
      const orderDataOption = {
        xAxis: {
          data: orderDataxAx,
        },
        series: [
          {
            data: orderDatayAx,
          },
        ],
      };
      // 设置数据对象
      this.hotItemChartInstance.setOption(hotItemDataOption);
      this.userChartInstance.setOption(userDataOption);
      this.orderChartInstance.setOption(orderDataOption);
    },
    // 配置适配器
    // screenAdapter() {
    //   const hotItemAdapterOption = {};
    //   const userDataAdapterOption = {};
    //   const orderDataAdapterOption = {};
    //   this.hotItemChartInstance.setOption(hotItemAdapterOption);
    //   this.userChartInstance.setOption(userDataAdapterOption);
    //   this.orderChartInstance.setOption(orderDataAdapterOption);
    //   this.hotItemChartInstance.resize();
    //   this.userChartInstance.resize();
    //   this.orderChartInstance.resize();
    // },
  },
};
</script>

<style lang="less" scoped>
.el-main {
  margin: 0;
  padding: 0;
  margin-left: 30px;
}
.el-row {
  margin-bottom: 30px;
  &:last-child {
    margin-bottom: 0;
  }
}
.main-container {
  width: 100%;
  height: 100%;
}
.wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}
.dataitem {
  height: 240px;
}
.smallChartItem {
  margin-bottom: 30px;
  &:last-child {
    margin-bottom: 0;
  }
}
.chartsContainer {
  width: 100%;
  height: 200px;
}
.footerCard {
  width: 100%;
  height: 300px;
}
.chartitem {
  padding-left: 0;
}
.doneOrder {
  background-color: rgba(44, 171, 144, 1);
}
.totalSales {
  background-color: antiquewhite;
}
.unsendOrder {
  background-color: #dd6060;
}
.unreceOrder {
  background-color: #409eff;
}
.cellbox{
  height:200px;
}
.theNumber {
  // border: 1px solid red;
  text-align:center;
  height:100px;
  line-height:90px;
  font-size: 50px;
}
.labeltext{
  font-size:20px;
  font-weight:bold;
}
.suffix {
  font-size:16px;
}
</style>
