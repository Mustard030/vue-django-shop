<template>
  <div>
    <div class="main-wrapper">
      <el-card>
        <!-- 标题 -->
        <div slot="header">
          <span>支付订单</span>
        </div>

        <div class="contain-wrapper">
          <div>
            <i class="el-icon-circle-check" style="font-size: 90px; color: green"></i>

            <span style="font-size: 19px; margin-left: 10px"
              >订单提交成功！去付款咯～</span
            ><br />
            <span style="font-size: 13px; margin-left: 10px; color: #939799"
              >订单编号:{{ orderId }}</span
            >
          </div>
        </div>
        <el-divider></el-divider>
        <div>
          <el-button type="success" round @click="pay">点击即可模拟付款</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 订单ID
      orderId: "",
    };
  },
  created() {
    this.orderId = this.$route.query.orderId;
  },
  methods: {
    //3秒后进入跳转页面
    threeGo() {
      const TIME_COUNT = 3;
      if (!this.timer) {
        this.count = TIME_COUNT;
        this.show = false;
        this.timer = setInterval(() => {
          if (this.count > 0 && this.count <= TIME_COUNT) {
            this.count--;
          } else {
            this.show = true;
            clearInterval(this.timer);
            this.timer = null;
            //跳转的页面写在此处
            this.$router.push({
              path: "/user/order",
            });
          }
        }, 1000);
      }
    },

    async pay() {
      const { data: res } = await this.$http.post("payment/", { orderId: this.orderId });
      console.log(res.meta.code)
      if (res.meta.code === 200) {
        this.$notify({
          title: "成功",
          message: "付款成功,3秒后跳转至订单页面",
          type: "success",
        });
        this.threeGo();
      }
      else if (res.meta.code === 201) {
        this.$notify({
          title: "警告",
          message: res.meta.message,
          type: "warning",
        });
        this.threeGo();
      } else {
        this.$notify.error({
          title: "错误",
          message: "付款失败",
        });
      }
    },
  },
};
</script>

<style lang="less" scoped>
.main-wrapper {
  width: 1330px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}
.contain-wrapper {
  width: 500px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}
i {
  vertical-align: middle;
}
</style>
