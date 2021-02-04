<template>
  <div>
    <div class="main-wrapper">
      <el-card>
        <el-row v-for="(item, index) in this.$store.state.searchResult" :key="index">
          <el-col :span="24">
            <el-card class="onebook">
              <h2>{{ item.title }}</h2>
              <p style="font-size: 14px; color: #997979">
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
    return {};
  },
  created() {
    //   console.log(this.$store.state.asd)
  },
  methods: {},
};
</script>

<style lang="less" scoped>
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
