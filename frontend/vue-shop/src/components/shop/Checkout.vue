<template>
  <div>
    <!-- 最外层框架 -->
    <div class="main-wrapper">
      <!-- 卡片视图区域 -->
      <el-card>
        <!-- 标题 -->
        <div slot="header">
          <span>确认订单</span>
        </div>
        <!-- 地址标签区 -->
        <div class="address">
          <p class="title">收货地址</p>
          <el-row :gutter="15">
            <el-col :span="6" v-for="(item, index) in addressList" :key="index">
              <div
                class="addObj"
                @click="getAdd(item, index)"
                :class="{ active: index == isSelect }"
              >
                <p class="recipient">{{ item.recipient }}</p>
                <p class="info">{{ item.phone }}</p>
                <p class="info">{{ item.province }}</p>
                <p class="info">{{ item.address }}</p>
                <el-link
                  icon="el-icon-edit"
                  :underline="false"
                  @click="showEditDialog(item)"
                  >编辑</el-link
                >
              </div>
            </el-col>
            <el-col :span="6">
              <div class="addObj" @click="addDialogVisible = true">
                <i class="el-icon-circle-plus" id="addAddressIocn"></i>
                <p id="addText">添加新地址</p>
              </div>
            </el-col>
          </el-row>
          <el-divider></el-divider>
          <p class="title">商品</p>
          <el-table
            ref="multipleTable"
            :data="orderForm.cartList"
            tooltip-effect="dark"
            style="width: 100%"
            :show-header="false"
          >
            <el-table-column width="120">
              <template slot-scope="scope">
                <el-image :src="scope.row.pic"></el-image>
              </template>
            </el-table-column>
            <el-table-column prop="name" show-overflow-tooltip></el-table-column>
            <el-table-column>
              <template slot-scope="scope"
                >¥{{ scope.row.price | priceFilter }}&nbsp;x&nbsp;{{
                  scope.row.num
                }}</template
              >
            </el-table-column>
            <el-table-column>
              <template slot-scope="scope"
                >¥{{ (scope.row.price * scope.row.num) | priceFilter }}</template
              >
            </el-table-column>
          </el-table>
        </div>

        <p class="price-count">
          合计:<span style="font-size: 35px"> {{ this.getPriceCount | priceFilter }}</span
          >元
        </p>

        <el-divider></el-divider>
        <div class="btn">
          <el-button @click="payOrder" class="count" type="danger">立即支付</el-button>
        </div>
      </el-card>
    </div>
    <!-- 修改地址的对话框 -->
    <el-dialog
      title="修改地址信息"
      :visible.sync="editDialogVisible"
      width="30%"
      @close="editDialogClosed"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editFormRules"
        label-width="80px"
        label-position="left"
      >
        <el-form-item label="收货人" prop="recipient">
          <el-input v-model="editForm.recipient"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="editForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="省/市" prop="province">
          <el-cascader
            :options="cityOptions"
            v-model="editForm.province"
            :props="cityProps"
            clearable
            filterable
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="详细地址" prop="address">
          <el-input v-model="editForm.address"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateDelivery">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 添加收货地址的对话框 -->
    <el-dialog
      title="添加地址"
      :visible.sync="addDialogVisible"
      width="30%"
      @close="addDialogClosed"
    >
      <!-- 内容主体 -->
      <el-form
        ref="addFormRef"
        :model="addForm"
        :rules="editFormRules"
        label-width="80px"
        label-position="left"
      >
        <el-form-item label="收货人" prop="recipient">
          <el-input v-model="addForm.recipient"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="addForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="省/市" prop="province">
          <el-cascader
            :options="cityOptions"
            v-model="addForm.province"
            :props="cityProps"
            clearable
            filterable
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="详细地址" prop="address">
          <el-input v-model="addForm.address"></el-input>
        </el-form-item>
      </el-form>

      <!-- 底部区域 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addDelivery">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import cityOptions from '../../assets/js/citydata'
import Vue from 'vue'
export default {
  data() {
    return {
      cityOptions,
      cityProps: {
        expandTrigger: 'hover'
      },
      // 修改表单
      editForm: {
        id: 0,
        recipient: '',
        phone: '',
        province: [],
        address: ''
      },
      // 添加表单
      addForm: {
        recipient: '',
        phone: '',
        province: [],
        address: ''
      },
      // 地址列表
      addressList: [],
      orderForm: {
        delivery: 0,
        uuid: '',
        cartList: []
      },
      // 地址选中index
      isSelect: null,
      // 修改对话框可视
      editDialogVisible: false,
      // 添加对话框可视
      addDialogVisible: false,
      // 修改表单规则
      editFormRules: {
        recipient: [{ required: true, message: '请输入收件人姓名', trigger: 'blur' }],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { min: 11, max: 11, message: '请输入正确格式的手机号码', trigger: 'blur' },
          { min: 11, max: 11, message: '请输入正确格式的手机号码', trigger: 'change' }
        ],
        province: [
          { required: true, message: '请选择省/市', trigger: 'blur' },
          { required: true, message: '请选择省/市', trigger: 'change' }
        ],
        address: [{ required: true, message: '请输入详细地址', trigger: 'blur' }]
      }
    }
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
  created() {
    this.orderForm.cartList = this.$store.state.itemInCart
    this.getDeliveryList()
    this.getUUID()
  },
  computed: {
    getPriceCount: function () {
      let sum = 0
      this.orderForm.cartList.forEach((x) => {
        sum += +x.price * x.num
      })
      return sum
    }
  },
  methods: {
    // 获取用户收货列表
    async getDeliveryList() {
      const { data: res } = await this.$http.get('userDelivery/')
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message)
      }
      this.addressList = res.data.addressList
      // console.log(this.addressList);
    },
    // 获取订单编号UUID
    async getUUID() {
      const { data: res } = await this.$http.get('uuid/')
      // if (res.meta.code !== 200){return this.$message.error(res.meta.message)}
      this.orderForm.uuid = res.uuid
    },
    // 显示修改对话框
    showEditDialog(item) {
      this.editForm.id = item.id
      this.editForm.recipient = item.recipient
      this.editForm.phone = item.phone
      this.editForm.address = item.address
      var temp = item.province.split('/')
      this.editForm.province = temp
      this.editDialogVisible = true
    },
    // 发送收货地址更改请求
    async updateDelivery() {
      // console.log(this.editForm);
      this.$refs.editFormRef.validate(async (valid) => {
        if (!valid) return
        const { data: res } = await this.$http.put('userDelivery/', this.editForm)
        // console.log(res)
        if (res.meta.code !== 200) {
          return this.$message.error(res.meta.message)
        }
        // this.$message.success(res.meta.message);
        // 隐藏添加提示框
        this.editDialogVisible = false
        // 重新获取地址数据
        this.getDeliveryList()
      })
    },
    // 修改地址对话框关闭事件
    editDialogClosed() {
      this.$refs.editFormRef.resetFields()
    },
    // 添加地址
    async addDelivery() {
      this.$refs.addFormRef.validate(async (valid) => {
        if (!valid) return
        const { data: res } = await this.$http.post('userDelivery/', this.addForm)
        // console.log(res)
        if (res.meta.code !== 200) {
          return this.$message.error(res.meta.message)
        }
        // this.$message.success(res.meta.message);
        // 隐藏添加提示框
        this.addDialogVisible = false
        // 重新获取地址数据
        this.getDeliveryList()
      })
    },
    // 添加地址对话框关闭事件
    addDialogClosed() {
      this.$refs.addFormRef.resetFields()
    },
    // 获取选择的收货地址
    getAdd(item, index) {
      this.orderForm.delivery = item.id
      this.isSelect = index
    },
    // 付款
    async payOrder() {
      if (this.orderForm.delivery === 0) {
        return this.$message.error('请先选择送货地址')
      }
      const { data: res } = await this.$http.post('orders/', this.orderForm)
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message)
      }
      this.$router.push(`/order/payment?orderId=${this.orderForm.uuid}`)
    }
  }
}
</script>

<style lang="less" scoped>
.main-wrapper {
  width: 1330px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}
.addObj {
  padding: 10px 20px 25px 20px;
  height: 160px;
  border: 1.5px dashed rgb(176, 176, 176);
  border-radius: 10px;
  margin-bottom: 13px;
  cursor: pointer;
}
.addObj:hover {
  .el-link {
    opacity: 1;
  }
}
.addObj.active {
  // border-color: rgb(255, 103, 0);
  border: 1.5px solid rgb(255, 103, 0);
}
.recipient {
  line-height: 20px;
  font-size: 19px;
  font-weight: bold;
  // color: red;
}
.info {
  font-size: 14px;
  color: rgb(112, 112, 112);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.title {
  font-size: 20px;
}
.el-link {
  float: right;
  bottom: 5px;
  opacity: 0;
}
#addAddressIocn {
  position: relative;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 40px;
}
#addText {
  position: relative;
  top: 40%;
  left: 50%;
  text-align: center;
  font-size: 17px;
  transform: translate(-50%, -50%);
}
.itemcount {
  color: red;
}
.price-count {
  font-size: 20px;
  color: #f56c6c;
  text-align: right;
}
.btn {
  float: right;
  // right: 10px;
  margin-right: 10px;
  margin-bottom: 20px;
}
</style>
