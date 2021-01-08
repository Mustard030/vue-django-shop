<template>
  <div>
    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>订单管理</el-breadcrumb-item>
      <el-breadcrumb-item>订单列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区域 -->
    <el-card>
      <el-row>
        <el-col>
          <el-date-picker
            v-model="dateRange"
            type="datetimerange"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :default-time="['00:00:00', '23:59:59']"
            @change="changeData"
          >
          </el-date-picker>
        </el-col>
      </el-row>

      <!-- 订单列表 -->
      <el-table :data="orderList" border stripe>
        <el-table-column type="expand" label="详情">
          <template slot-scope="props">
            <el-form label-position="left" inline>
              <el-form-item label="商品名称">
                <span>{{ props.row.name }}</span>
              </el-form-item>
              <el-form-item label="所属店铺">
                <span>{{ props.row.shop }}</span>
              </el-form-item>
              <el-form-item label="商品 ID">
                <span>{{ props.row.id }}</span>
              </el-form-item>
              <el-form-item label="店铺 ID">
                <span>{{ props.row.shopId }}</span>
              </el-form-item>
              <el-form-item label="商品分类">
                <span>{{ props.row.category }}</span>
              </el-form-item>
              <el-form-item label="店铺地址">
                <span>{{ props.row.address }}</span>
              </el-form-item>
              <el-form-item label="商品描述">
                <span>{{ props.row.desc }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="订单编号" prop="order_number"></el-table-column>
        <el-table-column label="订单价格" prop="order_price"></el-table-column>
        <el-table-column label="付款状态" prop="pay_status">
          <template slot-scope="scope">
            <el-tag type="danger" v-if="scope.row.pay_status === false">未付款</el-tag>
            <el-tag type="success" v-else>已付款</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="发货状态" prop="send_status">
          <template slot-scope="scope">
            <el-tag type="danger" v-if="scope.row.send_status === false">未发货</el-tag>
            <el-tag type="success" v-else>已发货</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="收货状态" prop="delivery_status">
          <template slot-scope="scope">
            <el-tag type="danger" v-if="scope.row.delivery_status === false"
              >未收货</el-tag
            >
            <el-tag type="success" v-else>已收货</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="下单时间" prop="create_date">
          <template slot-scope="scope">
            {{ scope.row.create_time }}
          </template>
        </el-table-column>
        <el-table-column label="查看物流信息">
          <template slot-scope="scope">
            <el-button
              type="success"
              icon="el-icon-location"
              size="mini"
              @click="showProgressBox(scope.row.order_number)"
            ></el-button>
          </template>
        </el-table-column>
      </el-table>

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

      <!-- 分页区域 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-sizes="[10, 20, 50]"
        :page-size="queryInfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 查询参数对象
      queryInfo: {
        query: "",
        pagenum: 1,
        pageSize: 10,
      },
      // 查询条目总数
      total: 0,
      // 订单列表
      orderList: [],
      // 选择日期范围
      dateRange: [],
      // 物流进度对话框显示
      progressDialogVisible: false,
      // 物流信息数组
      progressInfo: [],
      // 时间线反向
      reverse: true,
    };
  },
  created() {
    this.getOrderList();
  },
  methods: {
    // 获取订单列表
    async getOrderList() {
      const { data: res } = await this.$http.get("orders/", { params: this.queryInfo });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.orderList = res.data.orderList;
      this.total = res.data.total;
    },
    // 监听pagesize改变的事件
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize;
      this.getOrderList();
    },
    // 监听页码值改变的事件
    handleCurrentChange(newPage) {
      this.queryInfo.pagenum = newPage;
      this.getOrderList();
    },
    // 监听时间区间选择器
    changeData() {
      // console.log(this.dateRange)
      if (this.dateRange !== null) {
        var start = this.dateRange[0];
        var end = this.dateRange[1];
        // UTC时间格式转换——2019-10-14 12:20:12
        let delayTime = new Date(start).toJSON();
        this.dateRange[0] = new Date(+new Date(delayTime) + 8 * 3600 * 1000)
          .toISOString()
          .replace(/T/g, " ")
          .replace(/\.[\d]{3}Z/, "");
        delayTime = new Date(end).toJSON();
        this.dateRange[1] = new Date(+new Date(delayTime) + 8 * 3600 * 1000)
          .toISOString()
          .replace(/T/g, " ")
          .replace(/\.[\d]{3}Z/, "");
        this.queryInfo.query = this.dateRange[0] + "," + this.dateRange[1];
      }else {
        this.queryInfo.query="";
      }
      this.getOrderList();
    },
    // 显示物流进度
    async showProgressBox(id) {
      const { data: res } = await this.$http.get("kuaidi/", { params: { id: id } });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.progressInfo = res.data;

      this.progressDialogVisible = true;
    },
  },
};
</script>

<style lang="less" scoped></style>
