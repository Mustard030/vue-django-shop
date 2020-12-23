<template>
  <div>
    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>添加商品</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区域 -->
    <el-card>
      <!-- 添加商品提示信息 -->
      <el-alert
        title="添加商品"
        type="info"
        :closable="false"
        center
        show-icon
      ></el-alert>
      <!-- 步骤条 -->
      <el-steps :active="activeName - 0" finish-status="success" align-center>
        <el-step title="基本信息"></el-step>
        <el-step title="上传图片"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>

      <!-- 表单区域 -->
      <el-form
        :model="addItemForm"
        :rules="addItemRules"
        ref="addItemFormRef"
        label-width="100px"
        label-position="top"
      >
        <!-- 侧边标签页 -->
        <el-tabs :tab-position="'left'" v-model="activeName">
          <el-tab-pane label="基本信息" name="0">
            <el-form-item label="商品名称" prop="itemName">
              <el-input v-model="addItemForm.itemName" width="300px"></el-input>
            </el-form-item>
            <el-form-item label="商品价格" prop="price">
              <el-input v-model="addItemForm.price" type="number"></el-input>
            </el-form-item>
            <el-form-item label="库存量" prop="reserver">
              <el-input v-model="addItemForm.reserver" type="number"></el-input>
            </el-form-item>
            <el-form-item label="商品分类" prop="itemClass">
              <el-cascader
                v-model="category"
                :options="categoryList"
                :props="cateProps"
                @change="handleCateChange"
                clearable
                filterable
              ></el-cascader>
            </el-form-item>
            <el-form-item label="单位" prop="unit">
              <el-input v-model="addItemForm.unit"></el-input>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="上传图片" name="1">上传图片</el-tab-pane>
        </el-tabs>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      //标签页激活Name
      activeName: "0",
      //级联选择器选中项
      category: [],
      //级联选择框配置对象
      cateProps: {
        value: "cat_id",
        label: "cat_name",
        children: "children",
        expandTrigger: "hover",
      },
      //商品分类列表
      categoryList: [],
      // 添加商品的表单数据对象
      addItemForm: {
        itemName: "",
        price: 0,
        reserver: 0,
        itemClass: 0,
        unit: "",
      },
      //添加商品的表单验证项
      addItemRules: {
        itemName: [{ required: true, message: "请输入商品名称:", trigger: "blur" }],
        price: [
          { required: true, message: "请输入商品价格", trigger: "blur" },
          //   { min: 0, max: 9999.99, message: "请输入0~9999.99以内的价格", trigger: "blur" },
        ],
        reserver: [
          { required: true, message: "请输入商品库存量:", trigger: "blur" },
          { min: 0, max: 3, message: "请输入0~999以内的数字", trigger: "blur" },
        ],
        itemClass: [{ required: true, message: "请选择商品分类", trigger: "blur" }],
      },
    };
  },
  created() {
    this.getCateList();
  },
  methods: {
    //获取商品分类
    async getCateList() {
      const { data: res } = await this.$http.get("categories/", { params: { type: 2 } });
      if (res.meta.code !== 200) return this.$message.error(res.meta.message);

      this.categoryList = res.data;
    },
    // 监听分类选择改变事件
    handleCateChange() {
      this.addItemForm.itemClass = this.category[this.category.length - 1];
      console.log(this.addItemForm)
    },
  },
};
</script>

<style lang="less" scoped>
.el-steps {
  margin-top: 20px;
}
</style>
