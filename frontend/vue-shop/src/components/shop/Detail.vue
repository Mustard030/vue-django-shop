<template>
  <div>
    <div class="main-wrapper">
      <div class="info-wrapper">
        <div class="info-pics">
          <el-carousel :interval="5000" :height="dataHeight">
            <el-carousel-item v-for="(pic, index) in itemDetail.pics" :key="index">
              <el-image
                :src="pic"
                fit="fill"
                style="width: 100%; height: 100%"
              ></el-image>
            </el-carousel-item>
          </el-carousel>
        </div>
        <div class="info">
          <div>
            <h2 class="itemName">{{ itemDetail.itemName }}</h2>
          </div>
          <div>
            <p class="price">
              ¥{{ itemDetail.price | priceFilter
              }}<span style="color: #997979; font-size: 14px"
                >/{{ itemDetail.unit }}</span
              >
              <span style="margin-left: 30px" v-if="itemDetail.reserve === 0">售罄</span>
            </p>
          </div>
          <el-divider></el-divider>
          <div>
            <el-input-number
              v-model="num"
              :min="1"
              :max="itemDetail.reserve > 10 ? 10 : itemDetail.reserve"
              :disabled="itemDetail.reserve === 0"
            ></el-input-number
            >&nbsp;<span style="color: #997979; font-size: 15px">{{
              itemDetail.unit
            }}</span>
          </div>
          <div>
            <span style="color: #997979; font-size: 14px"
              >剩余{{ itemDetail.reserve }}{{ itemDetail.unit }}</span
            >
          </div>
          <br />
          <div>
            <el-button
              type="primary"
              round
              @click="addToCart(itemDetail.id)"
              :disabled="itemDetail.reserve === 0"
              >添加到购物车</el-button
            >
          </div>
        </div>
      </div>
      <el-divider>商品介绍</el-divider>
      <div class="item-introduce">
        <p v-html="itemDetail.introduce"></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dataHeight: {
      type: String,
      default: "360px",
    },
  },
  data() {
    return {
      itemDetail: {},
      // 购买数量
      num: "",
    };
  },
  created() {
    this.getItemDetail(this.$route.query.id);
  },
  filters: {
    priceFilter: function (price) {
      if (!price) {
        return 0;
      }
      const newVal = parseFloat(price).toFixed(2);
      return newVal;
    },
  },
  methods: {
    async getItemDetail(id) {
      const { data: res } = await this.$http.get("good/", { params: { id: id } });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.itemDetail = res.data;

      console.log(this.itemDetail);
    },
    async addToCart(id) {
      const { data: res } = await this.$http.post("cart/", { id: id, number: this.num });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      return this.$message.success(res.meta.message);
    },
  },
};
</script>

<style lang="less" >
.main-wrapper {
  width: 100%;
  background: #fff;
  padding-top: 50px;
  // border: 1px solid red;
  // display: flex;
  // flex-wrap: wrap;
}
.info-wrapper {
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  width: 1270px;
  margin-bottom: 90px;
  // height: 360px;
  // border: 1px solid green;
  display: flex;
  .info-pics {
    width: 560px;
    // height:100px;
    // border-block: 1px solid red;
  }
  .price {
    font-size: 24px;
    color: #d44d44;
  }
  .info {
    width: 715px;
    padding-left: 90px;
    padding-right: 50px;
    .itemName {
      // font-size:24px;
      font-weight: 400;
    }
  }
}
.item-introduce {
  width: 1270px;
  // height: 100px;
  // box-sizing: border-box;
  left: 50%;
  transform: translateX(23.9%);
  margin-top: 50px;
  padding-bottom: 100px;
  // border: 1px solid blue;
  p {
    p {
      img {
        width: 1270px;
      }
    }
  }
}
</style>
