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
        <el-step title="商品内容"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>

      <!-- 侧边标签页 -->
      <el-tabs :tab-position="'left'" v-model="activeName" 
      :before-leave="beforeTabLeave1231415123"
      >
        <el-tab-pane label="基本信息" name="0" disabled>
          <!-- 表单区域 -->
          <el-form
            :model="addItemForm"
            :rules="addItemRules"
            ref="addItemFormRef"
            label-width="100px"
            label-position="top"
          >
            <el-form-item label="商品名称" prop="itemName">
              <el-input v-model="addItemForm.itemName" width="300px"></el-input>
            </el-form-item>
            <el-form-item label="商品价格" prop="price">
              <el-input v-model="addItemForm.price" type="number"></el-input>
            </el-form-item>
            <el-form-item label="库存量" prop="reserve">
              <el-input v-model="addItemForm.reserve" type="number"></el-input>
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
            <el-form-item label="单位 如:斤,个,份" prop="unit">
              <el-input v-model="addItemForm.unit"></el-input>
            </el-form-item>
            <!-- <el-button type="primary" @on-click="submitForm">提交</el-button> -->
          </el-form>
        </el-tab-pane>

        <!-- 上传图片Tabs -->
        <el-tab-pane label="上传图片" name="1">
          <el-upload
            :action="uploadUrl + this.newItemID"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :on-success="handleSuccess"
            list-type="picture"
            :headers="headersObj"
            drag
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </el-upload>
        </el-tab-pane>

        <el-tab-pane label="商品内容" name="2">
          <!-- 富文本编辑器组件 -->
          <quill-editor v-model="addItemForm.introduce">

          </quill-editor>
        </el-tab-pane>

        <!-- 图片预览 -->
        <el-dialog title="图片预览" :visible.sync="previewVisible" width="50%">
          <img :src="previewUrl" class="previewImg" />
        </el-dialog>
      </el-tabs>
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
        price: null,
        reserve: null,
        itemClass: 0,
        unit: "",
        introduce:"",
      },
      //新增的商品的返回商品id
      newItemID: null,
      // 图片上传地址
      uploadUrl: "http://localhost:80/api/private/itemPics/",
      //添加商品的表单验证项
      addItemRules: {
        itemName: [{ required: true, message: "请输入商品名称", trigger: "blur" }],
        price: [
          { required: true, message: "请输入商品价格", trigger: "blur" },
          //   { min: 0, max: 9999.99, message: "请输入0~9999.99以内的价格", trigger: "blur" },
        ],
        reserve: [
          { required: true, message: "请输入商品库存量:", trigger: "blur" },
          { min: 0, max: 3, message: "请输入0~999以内的数字", trigger: "blur" },
        ],
        itemClass: [{ required: true, message: "请选择商品分类", trigger: "blur" }],
        unit: [{ required: true, message: "请填写商品单位", trigger: "blur" }],
      },
      //文件上传的请求头
      headersObj: {
        Authorization: window.sessionStorage.getItem("token"),
      },
      //预览图片地址
      previewUrl: "",
      //图片预览对话框显示
      previewVisible: false,
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
      //   console.log(this.addItemForm);
    },
    //离开标签页前的钩子函数
    beforeTabLeave(activeName, oldActiveName) {
      if (oldActiveName === "0" && this.addItemForm.itemName === "") {
        this.$message.error("请先填写商品名称");
        return false;
      } else if (oldActiveName === "0" && this.addItemForm.price === null) {
        this.$message.error("请先填写商品价格");
        return false;
      } else if (oldActiveName === "0" && this.addItemForm.reserve === null) {
        this.$message.error("请先填写商品库存");
        return false;
      } else if (oldActiveName === "0" && this.category.length !== 2) {
        this.$message.error("请先选择商品分类");
        return false;
      } else if (oldActiveName === "0" && this.addItemForm.unit === "") {
        this.$message.error("请先填写商品单位");
        return false;
      } else if (oldActiveName === "0" && activeName === "1") {
        this.submitForm();
      }
    },
    // 处理图片预览效果
    handlePreview(file) {
      this.previewUrl = "http://localhost:80" + file.response.data.url;
      //   console.log(this.previewUrl);
      this.previewVisible = true;
    },
    // 处理图片删除
    async handleRemove(file) {
      const deleteID = file.response.data.id;
      const { data: res } = await this.$http.delete("itemPics/" + deleteID);
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      console.log(res);
      return this.$message.success(res.meta.message);
    },
    //监听图片上传成功
    handleSuccess(response) {
      console.log(response);
    },
    //提交商品表单
    async submitForm() {
      const { data: res } = await this.$http.post("goods/", this.addItemForm);
      if (res.meta.code !== 200) {
        this.activeName = "0";
        return this.$message.error(res.meta.message);
      }
      this.newItemID = res.data.newItemID;
      //   console.log(this.newItemID)
    },
  },
  computed: {},
};
</script>

<style lang="less" scoped>
.el-steps {
  margin-top: 20px;
}
.el-upload {
  margin-top: 20px !important;
  margin-left: 20px !important;
}
.previewImg {
  width: 100%;
}
</style>
