<template>
  <div>
    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>用户收货地址</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区域 -->
    <el-card>
      <!-- 搜索栏 -->
      <el-row :gutter="20">
        <el-col :span="7">
          <el-input
            placeholder="请输入内容"
            v-model="queryInfo.query"
            clearable
            @change="getDeliveryList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getDeliveryList"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="addDialogVisible = true">添加地址</el-button>
        </el-col>
        <el-col :span="2">
          <el-button icon="el-icon-refresh" circle @click="getDeliveryList"></el-button>
        </el-col>
      </el-row>
    </el-card>

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
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 获取收货地址列表对象
      queryInfo: {
        query: "",
        province: [],
        pagenum: 1,
        pagesize: 10,
      },
      //收货地址信息列表
      deliveryList:[],
      //收货地址信息列表返回总数
      total: 0,
    };
  },
  created() {
      this.getDeliveryList();
  },
  methods: {
      //获取收货地址列表
    async getDeliveryList() {
      const { data: res } = await this.$http.get("delivery/", { params: this.queryInfo });
      if(res.meta.code !== 200){return this.$message.error(res.meta.message)}
      this.deliveryList = res.data.deliveryList
      this.total = res.data.total
    },
    //每页数量变化
    handleSizeChange(){
        this.queryInfo.pagesize = newSize
        this.getDeliveryList()
    },
    //页码变化
    handleCurrentChange(){
        this.queryInfo.pagenum = newPage
        this.getDeliveryList()
    },
  },
};
</script>

<style lang="less" scoped></style>
