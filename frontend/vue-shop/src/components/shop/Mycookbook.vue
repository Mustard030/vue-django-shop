<template>
  <div>
    <el-card>
      <div slot="header">
        <span style="font-size: 20px">我的菜谱</span>
        <el-button type="primary" class="newBook" @click="newBook"
          >发布菜谱<i class="el-icon-upload el-icon--right"></i
        ></el-button>
      </div>
      <div>
        <el-row v-for="(item, index) in MyBookList" :key="index">
          <el-col :span="24">
            <el-card class="onebook">
              <h2 @click="goCookbookDetail(item.id)">{{ item.title }}</h2>
              <span class="operator">
                <i class="el-icon-edit" @click="editBook(item.id)"></i>
                <i class="el-icon-delete" @click="deleteItem(item.id)"></i>
              </span>
              <p style="font-size: 14px; color: #909399">
                <span>{{ item.author }}</span>
                <el-divider direction="vertical"></el-divider>
                <span>最后编辑于: {{ item.modify_time }}</span>
              </p>
              <p v-html="item.content" class="content"></p>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 我发布的菜谱列表
      MyBookList: [],
    };
  },
  created() {
    this.getMyBook();
  },
  methods: {
    // 获得我发布的菜谱
    async getMyBook() {
      var id = this.$store.state.userInfo.userId;
      const { data: res } = await this.$http.get("myBook/", { params: { id: id } });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.MyBookList = res.data;
      // console.log(this.MyBookList);
    },
    goCookbookDetail(id) {
      this.$router.push(`/cookbook/detail?bookid=${id}`);
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
      this.getMyBook();
    },
    // 新建菜谱
    newBook(){
      this.$router.push('/cookbook/Add')
    },
    // 编辑菜谱
    editBook(id){
      this.$router.push(`/cookbook/Edit?bookid=${id}`)
    },
  },
};
</script>

<style lang="less" scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.onebook{
  h2{
    cursor: pointer;
  }
}
.content {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.newBook {
  position: relative;
  float: right;
}
.operator{
  position: relative;
  float:right;
  i{
    font-size:21px;
    margin-left:20px;
    cursor: pointer;
    opacity: 0;
  }
}
.onebook:hover{
  i{
    opacity: 1;
  }
  }
</style>
