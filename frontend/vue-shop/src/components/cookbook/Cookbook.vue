<template>
  <div>
    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>菜谱管理</el-breadcrumb-item>
      <el-breadcrumb-item>菜谱列表</el-breadcrumb-item>
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
            @change="getCookbookList"
            @clear="getCookbookList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getCookbookList"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="goAddPage">添加菜谱</el-button>
        </el-col>
      </el-row>

      <!-- 订单列表 -->
      <el-table :data="cookbookList" border stripe>
        <el-table-column type="expand" label="详情">
          <template slot-scope="props">
            <p v-html="props.row.content"></p>
          </template>
        </el-table-column>
        <el-table-column label="文章编号" prop="id"></el-table-column>
        <el-table-column label="标题" prop="title"></el-table-column>
        <el-table-column label="作者" prop="author"></el-table-column>
        <el-table-column label="作者ID" prop="authorID" v-if="false"></el-table-column>
        <el-table-column label="创建时间" prop="create_time"></el-table-column>
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
        pagesize: 10,
      },
      // 菜谱列表
      cookbookList: [],
      // 菜谱列表返回结果数
      total: 0,
    };
  },
  created() {
    this.getCookbookList();
  },
  methods: {
    // 获取菜谱列表
    async getCookbookList() {
      const { data: res } = await this.$http.get("cookbooks/", {
        params: this.queryInfo,
      });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.cookbookList = res.data.cookbookList;
      this.total = res.data.total;
    },
    // 删除文章
    async deleteItem(id) {
      const confirmResult = await this.$confirm(
        "此操作将永久删除该菜谱, 是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      ).catch((res) => res);

      if (confirmResult !== "confirm") {
        return this.$message.info("已取消删除");
      }
      const { data: res } = await this.$http.delete("cookbooks/", { data: { id: id } });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.$message.success(res.meta.message);
      this.getCookbookList();
    },
    // 跳转到新增页面
    goAddPage(){
      this.$router.push("/cookbook/add");
    },
    // 跳转至修改页面
    goEditPage(id){
      window.sessionStorage.setItem("essayID", id);
      this.$router.push("/cookbook/edit");
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
  },
};
</script>

<style lang="less" scoped></style>
