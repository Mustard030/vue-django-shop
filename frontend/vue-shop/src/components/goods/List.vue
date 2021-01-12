<template>
  <div>
    <!-- 商品列表页面 -->

    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>商品条目管理</el-breadcrumb-item>
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
            @change="getGoodsList"
            @clear="getGoodsList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getGoodsList"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-cascader
            v-model="category"
            :options="options"
            :props="cateProps"
            @change="handleCateChange"
            clearable
            filterable
          ></el-cascader>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="goAddPage">添加商品</el-button>
        </el-col>
      </el-row>

      <!-- 商品列表区 -->
      <el-table :data="goodsList" border stripe>
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="商品介绍">
                <div>
                  <p v-html="props.row.introduce"></p>
                </div> 
              </el-form-item>
              
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="商品ID" prop="id" width="85px"></el-table-column>
        <el-table-column label="商品名" prop="itemName"></el-table-column>
        <el-table-column
          label="所属分类"
          prop="itemClass"
          width="100px"
        ></el-table-column>
        <el-table-column label="店家" prop="merchantName"></el-table-column>
        <el-table-column label="销量" prop="sales" width="100px"></el-table-column>
        <el-table-column label="余量" prop="reserve" width="100px"></el-table-column>
        <el-table-column label="价格(元)" prop="price" width="100px"></el-table-column>
        <el-table-column label="单位" prop="unit" width="100px"></el-table-column>
        <el-table-column label="操作" width="150px">
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
        categoryId: 0,
        pagenum: 1,
        pagesize: 10,
      },
      // 商品信息列表
      goodsList: [],
      // 级联选择器选中项的数组
      category: [],
      // 筛选用级联选择器获取商品分类
      options: [],
      // 查询结果返回总数
      total: 0,
      // 级联选择框配置对象
      cateProps: {
        value: "cat_id",
        label: "cat_name",
        children: "children",
        expandTrigger: "hover",
      },
    };
  },
  created() {
    this.getGoodsList();
    this.getCateList();
  },
  methods: {
    // 根据分页获取对应的商品列表
    async getGoodsList() {
      const { data: res } = await this.$http.get("goods/", {
        params: this.queryInfo,
      });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }

      this.goodsList = res.data.goodslist;
      this.total = res.data.total;
    },
    // 获取用于限定搜索范围的商品分类列表
    async getCateList() {
      const { data: res } = await this.$http.get("categories/", { params: { type: 2 } });
      if (res.meta.code !== 200) return this.$message.error(res.meta.message);

      // 数据列表
      this.options = res.data;
    },
    // 监听pagesize改变的事件
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize;
      this.getGoodsList();
    },
    // 监听页码值改变的事件
    handleCurrentChange(newPage) {
      this.queryInfo.pagenum = newPage;
      this.getGoodsList();
    },
    // 监听分类选择改变事件
    handleCateChange() {
      this.queryInfo.categoryId = this.category[this.category.length - 1];
      this.getGoodsList();
    },
    // 跳转至更新商品信息页面
    goEditPage(id) {
      window.sessionStorage.setItem("editItem", id);
      this.$router.push("/goods/edit");
    },
    // 删除商品
    async deleteItem(id) {
      const confirmResult = await this.$confirm(
        "此操作将永久删除该商品, 是否继续?",
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
      const { data: res } = await this.$http.delete("goods/", { data: { id: id } });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.$message.success(res.meta.message);
      this.getGoodsList();
    },
    // 跳转至添加商品页面
    goAddPage() {
      this.$router.push("/goods/add");
    },
  },
};
</script>
<style lang="less" scoped>
.demo-table-expand {
  font-size: 0;
}
.el-form-item label{
  
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>
