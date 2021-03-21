<template>
  <div>
    <div class="main-wrapper">
      <el-card>
        <h1 class="title">{{ bookObj.title }}</h1>
        <p class="info">
            发布者:{{bookObj.author}}
            <el-divider direction="vertical"></el-divider>
            发布时间:{{bookObj.create_time}}
            <el-divider direction="vertical"></el-divider>
            修改时间:{{bookObj.modify_time}}
        </p>
        <el-divider></el-divider>
        <p v-html="bookObj.content"></p>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 菜谱对象
      bookObj: {
        essayID: '',
        title: '',
        author: '',
        content: '',
        create_time: '',
        modify_time: ''
      }
    }
  },
  created() {
    this.getThisEssay(this.$route.query.bookid)
  },
  methods: {
    // 获取该文章数据
    async getThisEssay(id) {
      // 如果文章id不存在
      if (!id) {
        this.$message.error('文章获取失败！')
        // this.$router.push("/cookbook");
      } else {
        const { data: res } = await this.$http.get('cookbooks/', { params: { id: id } })
        this.bookObj.essayID = res.data.cookbook.id
        this.bookObj.author = res.data.cookbook.author
        this.bookObj.title = res.data.cookbook.title
        this.bookObj.content = res.data.cookbook.content
        this.bookObj.create_time = res.data.cookbook.create_time
        this.bookObj.modify_time = res.data.cookbook.modify_time
        // console.log(this.bookObj)
      }
    }
  }
}
</script>

<style lang="less" scoped>
.title {
  font-size: 28px;
  word-wrap: break-word;
  color: #222226;
  font-weight: 600;
}
.info {
    font-size:14px;
    color:#909399;
}
</style>
