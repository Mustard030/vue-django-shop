<template>
  <div>
    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>商品条目管理</el-breadcrumb-item>
      <el-breadcrumb-item>修改商品</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区域 -->
    <el-card>
      <!-- 修改商品提示信息 -->
      <el-alert
        title="修改商品"
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
      <el-tabs :tab-position="'left'" v-model="activeName">
        <el-tab-pane label="基本信息" name="0">
          <!-- 表单区域 -->
          <el-form
            :model="editItemForm"
            :rules="editItemRules"
            ref="editItemFormRef"
            label-width="100px"
            label-position="top"
          >
            <el-form-item label="商品名称" prop="itemName">
              <el-input v-model="editItemForm.itemName" width="300px"></el-input>
            </el-form-item>
            <el-form-item label="商品价格" prop="price">
              <el-input v-model="editItemForm.price" type="number"></el-input>
            </el-form-item>
            <el-form-item label="库存量" prop="reserve">
              <el-input v-model="editItemForm.reserve"></el-input>
            </el-form-item>
            <el-form-item label="商品分类" prop="itemClass">
              <el-cascader
                v-model="editItemForm.itemClass"
                :options="categoryList"
                :props="cateProps"
                clearable
                filterable
              ></el-cascader>
            </el-form-item>
            <el-form-item label="单位 如:斤,个,份" prop="unit">
              <el-input v-model="editItemForm.unit"></el-input>
            </el-form-item>
            <el-form-item label="所属商家" prop="merchant">
              <el-select
                v-model="editItemForm.merchant"
                filterable
                clearable
                placeholder="请选择"
                :disabled="this.$store.state.userInfo.is_superuser ? false : true"
              >
                <el-option
                  v-for="m in merchantList"
                  :key="m.id"
                  :label="m.name"
                  :value="m.admin"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 上传图片Tabs -->
        <el-tab-pane label="上传图片" name="1">
          <el-upload
            :action="uploadUrl"
            :on-preview="handlePreview"
            :before-remove="handleRemove"
            :on-success="handleSuccess"
            list-type="picture-card"
            :headers="headersObj"
            :file-list="editItemForm.pics"
          >
            <i class="el-icon-plus"></i>
          </el-upload>
        </el-tab-pane>

        <el-tab-pane label="商品内容" name="2">
          <!-- 富文本编辑器组件 -->
          <quill-editor
            v-model="editItemForm.introduce"
            :options="editorOption"
          ></quill-editor>
          <el-button type="primary" class="addBtn" @click="submitForm"
            >确认修改</el-button
          >
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
      editorOption: {
        placeholder: "开始编辑吧",
        modules: {
          toolbar: [
            ["bold", "italic", "underline", "strike"], // toggled buttons
            ["blockquote", "code-block"],

            [{ header: 1 }, { header: 2 }], // custom button values
            [{ list: "ordered" }, { list: "bullet" }],
            [{ script: "sub" }, { script: "super" }], // superscript/subscript
            [{ indent: "-1" }, { indent: "+1" }], // outdent/indent
            [{ direction: "rtl" }], // text direction

            [{ size: ["small", false, "large", "huge"] }], // custom dropdown
            [{ header: [1, 2, 3, 4, 5, 6, false] }],

            [{ color: [] }, { background: [] }], // dropdown with defaults from theme
            [{ font: [] }],
            [{ align: [] }],

            ["clean"], // remove formatting button
            ["image"]
          ],
          // 调整图片大小
          imageResize: {
            displayStyles: {
              backgroundColor: "black",
              border: "none",
              color: "white",
            },
            modules: ["Resize", "DisplaySize", "Toolbar"],
          },
        },
      },
      // 查询对象
      queryInfo:{
        query:"",
        pagenum: 1,
        pagesize: 1000000,
      },
      // 标签页激活Name
      activeName: "0",
      // 级联选择器选中项
      category: [],
      // 级联选择框配置对象
      cateProps: {
        value: "cat_id",
        label: "cat_name",
        children: "children",
        expandTrigger: "hover",
      },
      // 商品分类列表
      categoryList: [],
      // 添加商品的表单数据对象
      editItemForm: {
        id: window.sessionStorage.getItem("editItem"),
        itemName: "",
        price: 0,
        reserve: 0,
        itemClass: [],
        unit: "",
        merchant: 0,
        introduce: "",
        pics: [],
      },
      // 新增的商品的返回商品id
      //   newItemID: null,
      // 图片上传地址
      uploadUrl: "http://localhost:80/api/private/itemPics/",
      // 添加商品的表单验证项
      editItemRules: {
        itemName: [{ required: true, message: "请输入商品名称", trigger: "blur" }],
        price: [
          { required: true, message: "请输入商品价格", trigger: "blur" },
          //   { min: 0, max: 9999.99, message: "请输入0~9999.99以内的价格", trigger: "blur" },
        ],
        reserve: [
          { required: true, message: "请输入商品库存量:", trigger: "blur" },
          //   { min: 0, max: 3, message: "请输入0~999以内的数字", trigger: "blur" },
        ],
        itemClass: [{ required: true, message: "请选择商品分类", trigger: "blur" }],
        unit: [{ required: true, message: "请填写商品单位", trigger: "blur" }],
        merchant:[{required: true, message:"请选择所属商家",trigger:"blur"}]
      },
      // 文件上传的请求头
      headersObj: {
        Authorization: window.sessionStorage.getItem("token"),
      },
      // 预览图片地址
      previewUrl: "",
      // 图片预览对话框显示
      previewVisible: false,
      //商家列表
      merchantList: [],
    };
  },
  created() {
    this.getCateList();
    this.getMerchantList();
    this.getItemData(window.sessionStorage.getItem("editItem"));
  },
  methods: {
    // 获取商品分类
    async getCateList() {
      const { data: res } = await this.$http.get("categories/", { params: { type: 2 } });
      if (res.meta.code !== 200) return this.$message.error(res.meta.message);

      this.categoryList = res.data;
    },
    // 获取商家列表
    async getMerchantList() {
      const { data: res } = await this.$http.get("merchant/",{ params: this.queryInfo });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.merchantList = res.data.merchant;
    },
    // 获取此条目商品信息
    async getItemData(id) {
      const { data: res } = await this.$http.get("goods/", { params: { id: id } });
      if(res.meta.code!==200){
        this.$message.error(res.meta.message);
        this.$router.push("/goods");
        return;
        }
      this.editItemForm.itemName = res.data.name;
      this.editItemForm.price = res.data.price;
      this.editItemForm.reserve = res.data.reserve;
      this.editItemForm.itemClass = res.data.itemClass;
      this.editItemForm.unit = res.data.unit;
      this.editItemForm.introduce = res.data.introduce;
      this.editItemForm.merchant = res.data.merchant;
      this.editItemForm.pics = res.data.pics;
    },
    // 处理图片预览效果
    handlePreview(file) {
      this.previewUrl = file.url;
      this.previewVisible = true;
    },
    // 处理图片删除
    async handleRemove(file, fileList) {
      var removePicID = file.id;
      const { data: res } = await this.$http.delete("itemPics/", {
        data: { id: removePicID },
      });
      if (res.meta.code !== 200) {
        this.$message.error(res.meta.message);
        reject(false);
      } else {
        const i = this.editItemForm.pics.findIndex((x) => x.id === removePicID);
        this.editItemForm.pics.splice(i, 1);
      }
    },
    // 监听图片上传成功
    handleSuccess(response) {
      const newPicID = response.data.id;
      this.editItemForm.pics.push({
        id: newPicID,
        url: response.data.url,
        name: response.data.name,
      });
    },
    // 提交商品表单
    async submitForm() {
      this.$refs.editItemFormRef.validate((valid) => {
        if (!valid) {
          return this.$message.error("请填写必要的表单项");
        }
      });
      // 执行修改
      const { data: res } = await this.$http.put("goods/", this.editItemForm);
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.$message.success(res.meta.message);
      this.$router.push("/goods");
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
.addBtn {
  margin-top: 20px;
}
</style>
