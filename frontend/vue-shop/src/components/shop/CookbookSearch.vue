<template>
  <div>
    <div class="main-wrapper">
      <el-card>
        <p v-if="this.$store.state.searchResult.length < 1" style="text-align:center;font-size:14px;color:#909399;">没找到你想要的菜谱~</p>
        <el-row v-for="(item, index) in this.$store.state.searchResult" :key="index">
          <el-col :span="24">
            <el-card class="onebook" @click.native="goCookbookDetail(item.id)">
              <h2>{{ item.title }}</h2>
              <p style="font-size: 14px; color: #909399">
                <span>{{ item.author }}</span>
                <el-divider direction="vertical"></el-divider>
                <span>最后编辑于: {{ item.modify_time }}</span>
              </p>
              <p v-html="item.content" class="content"></p>
            </el-card>
          </el-col>
        </el-row>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {}
  },
  created() {
    //   console.log(this.$store.state.asd)
  },
  methods: {
    goCookbookDetail(id) {
      this.$router.push(`/cookbook/detail?bookid=${id}`)
    }
  }
}
</script>

<style lang="less" scoped>
.main-wrapper{
  background:none;
  padding-top:0;
}
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.content {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
