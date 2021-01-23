<template>
  <div>
    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>首页头图管理</el-breadcrumb-item>
      <el-breadcrumb-item>首页头图</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区域 -->
    <el-card>
      <el-upload
        :action="uploadUrl"
        :on-preview="handlePreview"
        :before-remove="handleRemove"
        :on-success="handleSuccess"
        list-type="picture-card"
        :headers="headersObj"
        :file-list="pics"
      >
        <i class="el-icon-plus"></i>
      </el-upload>
    </el-card>
    <!-- 图片预览 -->
        <el-dialog title="图片预览" :visible.sync="previewVisible" width="50%">
          <img :src="previewUrl" class="previewImg" width="100%"/>
        </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 图片上传地址
      uploadUrl: "http://localhost:80/api/private/carouselPics/",
      // 文件上传的请求头
      headersObj: {
        Authorization: window.sessionStorage.getItem("token"),
      },
      // 预览图片地址
      previewUrl: "",
      // 图片预览对话框显示
      previewVisible: false,
      // 图片列表
      pics: [],
    };
  },
  created() {
      this.getCarouselPics();
  },
  methods: {
    // 获取图片信息
    async getCarouselPics(){
        const {data:res} = await this.$http.get('carouselPics/')
        this.pics = res.data
        // console.log(res)
    },
    // 处理图片预览效果
    handlePreview(file) {
      this.previewUrl = file.url;
      this.previewVisible = true;
    },
    // 处理图片删除
    async handleRemove(file, fileList) {
      var removePicID = file.id;
      const { data: res } = await this.$http.delete("carouselPics/", {
        data: { id: removePicID },
      });
      if (res.meta.code !== 200) {
        this.$message.error(res.meta.message);
        reject(false);
      } else {
        const i = this.pics.findIndex((x) => x.id === removePicID);
        this.pics.splice(i, 1);
      }
      this.getCarouselPics();
    },
    // 监听图片上传成功
    handleSuccess(response) {
      const newPicID = response.data.id;
      this.pics.push({
        id: newPicID,
        url: response.data.url,
        // name: response.data.name,
      });
    },
  },
};
</script>

<style lang="less" scoped></style>
