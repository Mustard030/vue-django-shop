<template>
  <div class="body">
    <div class="carousel">
      <el-carousel :interval="5000" :height="dataHeight">
        <el-carousel-item v-for="pic in carouselPics" :key="pic.id">
          <el-image
            :src="pic.url"
            fit="fill"
            style="width: 100%; height: 100%"
          ></el-image>
        </el-carousel-item>
      </el-carousel>
    </div>

    <div class="recommend">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>销量排行榜</span>
          <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
        </div>
        <el-row :gutter="15">
          <el-col :span="6" v-for="(item, index) in recommendList" :key="index">
            <el-card :body-style="bodyStyle" shadow="hover" class="itemCard" >
              <el-image
                :src="item.pic"
                fit="fill"
                style="width: 100%; height: 100%"
                @click="goDetailPage(item.id)"
              ></el-image>
              <div style="padding: 14px">
                <span>{{ item.name }}</span>
                <div class="bottom clearfix">
                  <div class="price">¥{{ item.price }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dataHeight: {
      type: String,
      default: "400px",
    },
  },
  data() {
    return {
      bodyStyle: {
        padding: "0px",
        height: "250px",
      },
      carouselPics: [],
      recommendList: [],
    };
  },
  created() {
    this.getCarouselPics();
    this.getRecommendList();
  },
  methods: {
    async getCarouselPics() {
      const { data: res } = await this.$http.get("carouselPics/");
      this.carouselPics = res.data;
    },
    async getRecommendList() {
      const { data: res } = await this.$http.get("recommendList/");
      this.recommendList = res.data;
    },
    goDetailPage(id){
        this.$router.push(`/buy/detail?id=${id}`)
    }
  },
};
</script>

<style lang="less" scoped>
.body {
  width: 100%;
  height: 100%;
}
.carousel {
  width: 1000px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}
.recommend {
  width: 1000px;
  position: absolute;
  left: 50%;
  top: 50%;
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
</style>
