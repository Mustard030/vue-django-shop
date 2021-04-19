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
            <i
              class="el-icon-circle-check"
              style="font-size: 90px; color: green"
              v-if="trueOrder === true"
            ></i>

            <span style="font-size: 19px; margin-left: 10px" v-if="trueOrder === true && paid === false"
              >订单提交成功！去付款咯～</span
            >
            <span style="font-size: 19px; margin-left: 10px" v-if="paid === true"
              >订单已经支付过了~</span
            >
            <br />
            <span
              style="font-size: 13px; margin-left: 10px; color: #939799"
              v-if="trueOrder === true"
              >订单编号:{{ orderId }}</span
            >
            <i
              class="el-icon-circle-close"
              style="font-size: 90px; color: red"
              v-if="trueOrder !== true"
            ></i>
            <span style="font-size: 19px; margin-left: 10px" v-if="trueOrder !== true"
              >订单不存在</span
            >
          </div>
        </div>
        <el-divider></el-divider>
        <div v-if="trueOrder === true && paid === false">
          <p>选择您的支付方式:</p>
          <div>
            <el-radio v-model="paymentway" label="wechat" border>微信支付</el-radio>
            <el-radio v-model="paymentway" label="alipay" border>支付宝</el-radio>
            <el-radio v-model="paymentway" label="bc" border>中国银行</el-radio>
            <el-radio v-model="paymentway" label="icbc" border>中国工商银行</el-radio>
          </div>
          <br /><el-button type="success" round @click="pay" :disabled="paymentway===null">点击即可模拟付款</el-button>
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
      // 真实订单
      trueOrder: false,
      // 支付方式
      paymentway:null,
      paid:false,
    };
  },
  created() {
    this.orderId = this.$route.query.orderId;
    this.checkOrder(this.orderId);
  },
  methods: {
    // 3秒后进入跳转页面
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
            // 跳转的页面写在此处
            this.$router.push({
              path: "/user/order",
            });
          }
        }, 1000);
      }
    },

    async pay() {
      const { data: res } = await this.$http.post("payment/", { orderId: this.orderId });
      // console.log(res.meta.code)
      if (res.meta.code === 200) {
        this.$notify({
          title: "成功",
          message: "付款成功,3秒后跳转至订单页面",
          type: "success",
        });
        this.threeGo();
      } else if (res.meta.code === 201) {
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

    async checkOrder(orderID) {
      const { data: res } = await this.$http.put("userOrder/", { orderId: orderID });
      if (res.meta.code === 400) {
        this.$message.error(res.meta.message);
        this.trueOrder = false;
        return;
      }
      if (res.meta.code === 201) {
        this.paid = true;
      }
      this.trueOrder = true;
      return;
    },
  },
};
</script>

<style lang="less" scoped>
.main-wrapper {
  width: 1330px;
  position: relative;
  left: 50%;
  background:none;
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
