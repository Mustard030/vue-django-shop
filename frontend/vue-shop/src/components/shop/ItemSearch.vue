<template>
  <div>
    <div class="recommend">
      <el-card class="box-card">
        <!-- <div slot="header" class="clearfix">
          <span>销量排行榜</span>
        </div> -->
        <p v-if="this.$store.state.searchResult.length < 1" style="text-align:center;font-size:14px;color:#909399;">没找到你想要的商品~</p>
        <el-row :gutter="15">
          <el-col
            :span="6"
            v-for="(item, index) in this.$store.state.searchResult"
            :key="index"
          >
            <el-card :body-style="bodyStyle" shadow="hover" class="itemCard">
              <el-image
                :src="item.pic"
                fit="fill"
                style="width: 100%; height: 100%"
                @click="goDetailPage(item.id)"
              ></el-image>
              <div style="padding: 14px">
                <span class="content">{{ item.name }}</span>
                <div class="bottom clearfix">
                  <div class="price">¥{{ item.price }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-card>
      <!-- {{ this.$store.state.searchResult }} -->
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bodyStyle: {
        padding: '0px',
        height: '250px'
      },
      // 搜索结果集
      results: []
    }
  },
  created() {
    // this.getSearchData(this.$route.query.keyword)
  },
  methods: {
    // 获取搜索数据
    async getSearchData(keyword) {
      const { data: res } = await this.$http.get('searchItem/', {
        params: { keyword: keyword }
      })
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message)
      }
      this.results = res.data
    },
    goDetailPage(id) {
      this.$router.push(`/buy/detail?id=${id}`)
    }
  }
}
</script>

<style lang="less" scoped>
.recommend {
  width: 1000px;
  position: absolute;
  left: 50%;
//   top: 50%;
  transform: translateX(-50%);
  margin-top: 20px;
}
.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}
.price {
    float: right;
    color: rgb(255,103,0);
    margin-bottom: 5px;
}
.itemCard{
    margin-bottom: 15px;
    // font-color:rgb(66,66,66);
}
.content {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
