<template>
  <div>
    <el-card>
      <div slot="header">
        <span style="font-size: 20px">我的订单</span>
      </div>
      <div class="main-wrapper">
        <div>
          <el-link :underline="false" @click="setAct(1)">全部订单</el-link>
          <el-divider direction="vertical"></el-divider>
          <el-link :underline="false" @click="setAct(2)">待支付</el-link>
          <el-divider direction="vertical"></el-divider>
          <el-link :underline="false" @click="setAct(3)">待收货</el-link>
        </div>

        <div class="orderInfo">
          <div>
            <p v-if="orderList.length < 1" style="text-align:center;font-size:14px;color:#909399;">还没有订单信息哦~</p>
          </div>
          <ul>
            <li v-for="(order, index) in orderList" :key="index">
              <div class="oneOrder">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看物流"
                  placement="top"
                  :enterable="false"
                  v-if="order.delivery_status"
                >
                  <span class="status delivery" @click="showProgressBox(order.id)">
                    已收货
                  </span></el-tooltip
                >
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看物流"
                  placement="top"
                  :enterable="false"
                  v-else-if="order.send_status"
                >
                  <span class="status send" @click="showProgressBox(order.id)">
                    已发货
                  </span></el-tooltip
                >
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="还没有物流哦~"
                  placement="top"
                  :enterable="false"
                  v-else-if="order.pay_status"
                  ><span class="status pay">已付款</span></el-tooltip
                >
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="去支付"
                  placement="top"
                  :enterable="false"
                  v-else
                  ><span class="status unpay" @click="payOrder(order.id)"
                    >未付款</span
                  ></el-tooltip
                >
                <i
                  class="el-icon-delete"
                  @click="deleteOrder(order.id)"
                  v-if="order.delivery_status"
                ></i>
                <div class="orderInfo">
                  <div class="orderInfoDetail">
                    <span>{{ order.create_date }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span>{{ order.deliveryInfo.recipient }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span>订单号:{{ order.id }}</span>
                    <!-- <el-divider direction="vertical"></el-divider> -->
                  </div>
                  <div class="orderInfoTotalPrice">
                    <span style="color: #757575"
                      >实付金额:<span style="font-size: 22px; color: #333">{{
                        order.total_price | priceFilter
                      }}</span
                      >元</span
                    >
                  </div>
                </div>
                <el-divider></el-divider>
                <div class="item">
                  <el-table
                    ref="multipleTable"
                    :data="order.order_detail"
                    tooltip-effect="dark"
                    style="width: 100%"
                    :show-header="false"
                  >
                    <el-table-column width="120">
                      <template slot-scope="scope">
                        <el-image :src="scope.row.pic"></el-image>
                      </template>
                    </el-table-column>
                    <el-table-column
                      prop="itemName"
                      show-overflow-tooltip
                    ></el-table-column>
                    <el-table-column>
                      <template slot-scope="scope"
                        >¥{{ scope.row.price | priceFilter }}&nbsp;x&nbsp;{{
                          scope.row.number
                        }}</template
                      >
                    </el-table-column>
                    <el-table-column>
                      <template slot-scope="scope"
                        >¥{{
                          (scope.row.price * scope.row.number) | priceFilter
                        }}</template
                      >
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </el-card>
    <!-- 物流进度对话框 -->
    <el-dialog title="物流进度" :visible.sync="progressDialogVisible" width="30%">
      <el-timeline :reverse="reverse">
        <el-timeline-item
          v-for="(activity, index) in progressInfo"
          :key="index"
          :timestamp="activity.time"
        >
          {{ activity.message }}
        </el-timeline-item>
      </el-timeline>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 订单列表
      orderList: [],
      // 全部订单选项
      allOrder: [],
      // 未支付
      unpay: [],
      // 未收货
      undelivery: [],
      // 物流进度对话框显示
      progressDialogVisible: false,
      // 物流信息数组
      progressInfo: [],
      // 时间线反向
      reverse: true
    }
  },
  created() {
    this.getAllOrder()
  },
  filters: {
    priceFilter: function (price) {
      if (!price) {
        return 0
      }
      const newVal = parseFloat(price).toFixed(2)
      return newVal
    }
  },
  methods: {
    // 获取订单数据
    async getAllOrder() {
      const { data: res } = await this.$http.get('userOrder/')
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message)
      }
      this.allOrder = res.data
      this.orderList = this.allOrder
      this.unpay = this.allOrder.filter(function (item, index, array) {
        // 元素值，元素的索引，原数组。
        return !item.pay_status
      })
      this.undelivery = this.allOrder.filter(function (item, index, array) {
        // 元素值，元素的索引，原数组。
        return item.pay_status && !item.delivery_status
      })
    },
    // 删除订单
    async deleteOrder(id) {
      const confirmResult = await this.$confirm(
        '此操作将永久删除该订单, 是否继续?',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).catch((res) => res)

      if (confirmResult !== 'confirm') {
        return this.$message.info('已取消删除')
      }
      const { data: res } = await this.$http.delete('userOrder/', { data: { id: id } })
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message)
      }
      this.$message.success(res.meta.message)
      this.getAllOrder()
    },
    setAct(id) {
      if (id === 1) {
        this.orderList = this.allOrder
      } else if (id === 2) {
        this.orderList = this.unpay
      } else if (id === 3) {
        this.orderList = this.undelivery
      }
    },
    // 去支付
    payOrder(id) {
      this.$router.push(`/order/payment?orderId=${id}`)
    },
    // 显示物流进度
    async showProgressBox(id) {
      const { data: res } = await this.$http.get('kuaidi/', { params: { id: id } })
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message)
      }
      this.progressInfo = res.data

      this.progressDialogVisible = true
    }
  }
}
</script>

<style lang="less" scoped>
.el-link {
  font-size: 16px;
}
ul {
  list-style-type: none;
  padding: 0;
}

.oneOrder {
  // height: 50px;
  margin-bottom: 20px;
  padding-top: 10px;
  // padding: 10px;
  border: 1px rgb(176, 176, 176) solid;
  p {
    // display: inline;
    margin-left: 10px;
  }
  i {
    position: relative;
    top: -40px;
    right: -880px;
    font-size: 19px;
    opacity: 0;
  }
  .status {
    font-size: 18px;
    color: #b0b0b0;
    margin-left: 10px;
  }
  .send {
    color: #5cb87a;
    cursor: pointer;
  }
  .pay {
    color: #e6a23c;
    // cursor: pointer;
  }
  .unpay {
    color: #f56c6c;
    cursor: pointer;
  }
}
.oneOrder:hover {
  i {
    opacity: 1;
    cursor: pointer;
  }
}
.orderInfoDetail {
  // float: left;
  display: inline-block;
  text-align: left;
  padding: 10px;
  span {
    color: #757575;
    font-size: 13px;
  }
}
.orderInfoTotalPrice {
  float: right;
  // position: relative;
  // left:80px;
  padding: 10px;
  display: inline-block;
  text-align: right;
  margin-bottom: 2px;
}
.el-divider--horizontal {
  margin: 12px 0;
}
</style>
