<template>
  <div>
    <!-- 商家列表 -->

    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商铺管理</el-breadcrumb-item>
      <el-breadcrumb-item>商铺列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区域 -->
    <el-card>
      <!-- 顶部搜索栏区域 -->
      <el-row :gutter="20">
        <el-col :span="7">
          <el-input
            placeholder="请输入内容"
            v-model="queryInfo.query"
            clearable
            @change="getMerchantList"
            @clear="getMerchantList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getMerchantList"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="openAddDialog">添加商铺</el-button>
        </el-col>
      </el-row>

      <!-- 列表区域 -->
      <el-table :data="merchantList" border stripe>
        <el-table-column label="商铺ID" prop="id"></el-table-column>
        <el-table-column label="商铺名称" prop="name"></el-table-column>
        <el-table-column label="商铺管理员" prop="admin_name"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <!-- 修改按钮 -->
            <el-tooltip
              class="item"
              effect="dark"
              content="编辑"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="small"
                @click="goEditPage(scope.row.id)"
              >
              </el-button>
            </el-tooltip>

            <!-- 删除按钮 -->
            <el-tooltip
              class="item"
              effect="dark"
              content="删除"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="small"
                @click="deleteItem(scope.row.id)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      //查询对象
      queryInfo: {
        query: "",
        pagenum: 1,
        pagesize: 10,
      },
      // 返回商铺数据集
      merchantList: [],
      // 商铺数据集数量
      total: 0,
    };
  },
  created() {
    this.getMerchantList();
  },
  methods: {
    async getMerchantList() {
      const { data: res } = await this.$http.get("merchant/", { params: this.queryInfo });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.merchantList = res.data.merchant;
      this.total = res.data.total;
    },
  },
};
</script>

<style lang="less" scoped></style>
