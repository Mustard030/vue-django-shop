<template>
  <el-container class="home-container">
    <!-- 头部区域 -->
    <el-header>
      <el-menu
        :default-active="activePath"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        router
      >
        <el-menu-item index="/" @click="saveNavState('/')">首页</el-menu-item>
        <el-menu-item index="/category/list" @click="saveNavState('/category/list')"
          >全部商品分类</el-menu-item
        >
        <el-menu-item>
          <el-link
            href="https://github.com/Mustard030/vue-django-shop"
            target="_blank"
            :underline="false"
            >Github</el-link
          >
        </el-menu-item>
        <div class="searchbar">
          <el-input
            placeholder="请输入内容"
            v-model="keyword"
            class="input-with-select"
            clearable=""
          >
            <el-select v-model="select" slot="prepend" placeholder="请选择">
              <el-option label="商品" value="item"></el-option>
              <el-option label="菜谱" value="cookbook"></el-option>
            </el-select>
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="searchWithSelect"
            ></el-button>
          </el-input>
        </div>
        <div class="userinfo">
          <el-row :gutter="20">
            <el-col :span="12">
              <div v-if="this.loginedUser.userId == null">
                <a @click="goLogin">
                  <el-avatar class="avatar" icon="el-icon-user-solid"></el-avatar
                ></a>
              </div>
              <div v-else>
                <el-dropdown>
                  <el-avatar
                    class="avatar"
                    icon="el-icon-user-solid"
                    :src="
                      this.$store.state.BACKEND_URL + this.$store.state.userInfo.avatar
                    "
                  ></el-avatar>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item
                      ><i class="el-icon-user"></i
                      ><a @click="goUserPage">个人中心</a></el-dropdown-item
                    >
                    <el-dropdown-item
                      ><i class="el-icon-notebook-2"></i
                      ><a @click="goMyCookbookPage">我的菜谱</a></el-dropdown-item
                    >
                    <el-dropdown-item
                      ><i class="el-icon-tickets"></i
                      ><a @click="goMyOrderPage">我的订单</a></el-dropdown-item
                    >
                    <el-dropdown-item divided
                      ><i class="el-icon-switch-button"></i
                      ><a @click="clearLocalStorage">退出登录</a></el-dropdown-item
                    >
                  </el-dropdown-menu>
                </el-dropdown>
              </div></el-col
            >
            <el-col :span="12" style="margin-top: 10px">
              
                <el-button
                  icon="el-icon-shopping-cart-2"
                  circle
                  @click="goCartPage"
                ></el-button
              >
            </el-col>
          </el-row>
        </div>
      </el-menu>
    </el-header>

    <!-- 页面主体 -->
    <!-- 主视图 -->
    <el-main background-color="#EAEDF1" style="min-width: 1200px">
      <!-- 欢迎页占位符 -->
      <router-view></router-view>
    </el-main>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      keyword: "",
      select: "item",
      activePath: "/",
    };
  },
  created() {
    this.activePath = window.sessionStorage.getItem("activePath");
  },
  methods: {
    handleSelect(key, keyPath) {
      // console.log(key, keyPath);
    },
    clearLocalStorage() {
      window.sessionStorage.clear();
      this.$store.commit("clearLocalStorage");
      this.$router.push("/");
    },
    goLogin() {
      this.$router.push("/login");
    },
    goUserPage() {
      this.$router.push("/user/portal");
    },
    goCartPage() {
      this.$router.push("/buy/cart");
    },
    goMyCookbookPage() {
      this.$router.push("/user/cookbook");
    },
    goMyOrderPage() {
      this.$router.push("/user/order");
    },
    // 保存链接的激活状态
    saveNavState(activePath) {
      window.sessionStorage.setItem("activePath", activePath);
      this.activePath = activePath;
    },
    // 切换搜索商品或菜谱的网址
    async searchWithSelect() {
      var href = "";
      if(this.select==='item'){
        href = "searchItem/"
      }else if(this.select === "cookbook"){
        href = "searchCookbook/"
      }
      const {data:res} = await this.$http.get(href,{params:{keyword:this.keyword}})
      if (res.meta.code!==200){return this.$message.error(res.meta.message)}
      this.$store.commit('updateSearchResult',res.data)
      this.$router.push(`/search/${this.select}?keyword=${this.keyword}`);
    },
  },
  computed: {
    loginedUser() {
      return this.$store.state.userInfo;
    },
    // cartValue() {
    //   var num = 0;
    //   this.$http.get(`cart/?id=${this.$store.state.userInfo.userId}`).then((res)=>{
    //     // console.log(res.data.data.tableData)
    //     for(var i=0;i<res.data.data.tableData.length;i++){
    //       num+=res.data.data.tableData[i].num
    //     }
    //   });
    //   return num;
    // },
  },
};
</script>
<style lang="less" scoped>
.home-container {
  height: 100%;
}
.el-header {
  padding: 0;
}
.el-menu {
  padding: 0 300px 0 300px;
  min-width: 1200px;
}
.userinfo {
  float: right;
  height: 100%;
}
.avatar {
  margin-top: 10px;
}
.searchbar {
  float: left;
  margin-top: 10px;
  margin-left: 130px;
  width: 30%;
}
.el-select {
  width: 80px;
}
.input-with-select .el-input-group__prepend {
  background-color: #fff;
}
</style>
