<template>
  <div>
    <div class="main-wrapper">
      <el-card>
        <div slot="header">
          <span>确认订单</span>
        </div>
        <div class="address">
          
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cartList: [],
      addressList: [],
    };
  },
  created() {
    this.cartList = this.$store.state.cartList;
    this.getAddressList();
  },
  methods: {
    // 获取用户收货列表
    async getAddressList(){
      const {data:res} = await this.$http.get('userAddress/')
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
</style>
