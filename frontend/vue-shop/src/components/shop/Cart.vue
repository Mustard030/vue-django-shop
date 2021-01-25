<template>
  <div>
    <div class="cart-wrapper">
      <el-card>
        <div slot="header">
          <span>购物车清单</span>
        </div>
        <el-table
          ref="multipleTable"
          :data="tableData"
          tooltip-effect="dark"
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column label="商品ID" prop="id" v-if="false"></el-table-column>

          <el-table-column label="" width="120">
            <template slot-scope="scope">
              <el-image :src="scope.row.pic"></el-image>
            </template>
          </el-table-column>
          <el-table-column
            prop="name"
            label="商品名称"
            show-overflow-tooltip
          ></el-table-column>
          <el-table-column label="单价">
            <template slot-scope="scope">¥{{ scope.row.price | priceFilter }}</template>
          </el-table-column>
          <el-table-column label="数量">
            <template slot-scope="scope">
              <el-input-number
                v-model="scope.row.num"
                :min="1"
                :max="10"
                size="small"
              ></el-input-number>
            </template>
          </el-table-column>
          <el-table-column label="小计">
            <template slot-scope="scope"
              >¥{{ (scope.row.price * scope.row.num) | priceFilter }}</template
            >
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                icon="el-icon-close"
                circle
                @click="deleteItem(scope.row.id)"
                class="delbtn"
              ></el-button>
            </template>
          </el-table-column>
        </el-table>
        <div style="margin-top: 20px">
          <el-button @click="toggleSelection()">取消选择</el-button>
          <el-button @click="goCount" class="count" type="danger" :disabled="this.multipleSelection.length===0">立即结算</el-button>
          <span class="price-count">合计: {{ this.getPriceCount | priceFilter }}元</span>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
      multipleSelection: [],
    };
  },
  created() {
    this.getCart();
  },
  filters: {
    priceFilter: function (price) {
      if (!price) {
        return 0;
      }
      let newVal = parseFloat(price).toFixed(2);
      return newVal;
    },
  },
  methods: {
    async getCart() {
      const { data: res } = await this.$http.get(
        `cart/?id=${this.$store.state.userInfo.userId}`
      );
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.tableData = res.data.tableData;
      // console.log(this.tableData);
    },
    toggleSelection(rows) {
      if (rows) {
        rows.forEach((row) => {
          this.$refs.multipleTable.toggleRowSelection(row);
        });
      } else {
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
      console.log(this.multipleSelection);
    },
    // 去结算
    goCount() {
      console.log(this.multipleSelection)
    },
  },
  computed: {
    getPriceCount: function () {
      let sum = 0;
      this.multipleSelection.forEach((x) => {
        sum += +x.price * x.num;
      });
      return sum;
    },
  },
};
</script>

<style lang="less" scoped>
.cart-wrapper {
  width: 1330px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}
.delbtn {
  border: 0 !important;
}
.count {
  float: right;
  display: inline;
  // background: #ff6700;
  // border-color: #ff6700;
  // color: #fff;
}
.price-count {
  color: #ff6700;
  float: right;
  margin-top: 0px;
  line-height:40px;
  size:39px;
  margin-right: 10px;
}
</style>
