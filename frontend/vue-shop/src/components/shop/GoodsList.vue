<template>
  <div class="container">
    <el-collapse v-model="activeNames">
      <el-collapse-item
        v-for="cate in brief"
        :title="cate.name"
        :name="cate.id"
        :key="cate.id"
      >
        <div class="innerContainer">
          <el-collapse v-model="secActiveNames">
            <el-collapse-item
              v-for="secCate in cate.children"
              :title="secCate.name"
              :name="secCate.id"
              :key="secCate.id"
            >
              <el-row :gutter="15">
                <el-col :span="6" v-for="(item, index) in secCate.itemList" :key="index">
                  <el-card :body-style="bodyStyle" shadow="hover" class="itemCard">
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
                        <div style="color:gray;">库存:{{item.reserve}}</div>
                      </div>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </el-collapse-item>
          </el-collapse>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bodyStyle: {
        padding: "0px",
        height: "250px",
      },
      brief: [],
      activeNames: [],
      secActiveNames: [],
    };
  },
  created() {
    this.getAllGood();
  },
  methods: {
    async getAllGood() {
      const { data: res } = await this.$http.get("getAllGood/");
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.brief = res.data;
      // console.log(res);
    },
    goDetailPage(id){
        this.$router.push(`/buy/detail?id=${id}`)
    }
  },
};
</script>

<style lang="less" scoped>

.container {
  position: absolute;
  width: 60%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #fff;
  padding: 24px;
  border-radius: 20px;
  border: 1px#d3dce6 solid;
  min-width: 1000px;
}

.innerContainer {
  padding: 24px;
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
.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.clearfix:after {
  clear: both;
}
</style>
