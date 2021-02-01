<template>
  <el-container>
    <div class="aside">
      <el-aside>
        <el-menu :default-active="activePath" router>
          <div class="avatar-wrapper">
            
              <el-image
                :src="this.$store.state.BACKEND_URL + this.$store.state.userInfo.avatar"
                fit="fill"
              ></el-image>
            
            <p class="username">{{ this.$store.state.userInfo.username }}</p>
          </div>

          <el-menu-item index="/user/portal" @click="saveNavState('/user/portal')"
            >个人信息</el-menu-item
          >
          <el-menu-item index="/user/cookbook" @click="saveNavState('/user/cookbook')"
            >我的菜谱</el-menu-item
          >
          <el-menu-item index="/user/address" @click="saveNavState('/user/address')"
            >收货地址</el-menu-item
          >
          <el-menu-item index="/user/order" @click="saveNavState('/user/order')"
            >我的订单</el-menu-item
          >
        </el-menu>
      </el-aside>
    </div>
    <div class="main-container">
      <el-main>
        <router-view></router-view>
      </el-main>
    </div>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      activePath: "",
    };
  },
  created() {
    this.activePath = window.sessionStorage.getItem("activePath");
  },
  methods: {
    // 保存链接的激活状态
    saveNavState(activePath) {
      window.sessionStorage.setItem("activePath", activePath);
      this.activePath = activePath;
    },
  },
};
</script>

<style lang="less" scoped>
.aside {
  border-radius: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  overflow: hidden;
  position: fixed;
  left: 15%;
  top: 10%;
  // width: 200px;
}
.el-menu-item {
  text-align: center;
  font-size: 16px;
  border-top: 1px #d4d4d4 solid;
}
.el-menu-item:focus,
.el-menu-item:hover,
.el-menu-item.is-active {
  background-color: #98afee;
  color: white;
}

.main-container {
  position: absolute;
  left: 31%;
  width: 1000px;
  margin-left: 20px;
  // border: 1px solid red;
}
.avatar-wrapper {
  width: 100%;
  height: 300px;
  // box-sizing: border-box;
}

.el-image {
  // float: bottom;
  width: 210px;
  height:210px;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -58%);
  border-radius: 50%;
  border: 1px solid #eee;
  box-shadow: 0 0 10px #ddd;
}
.username {
  text-align: center;
  position: relative;
  margin-top: 30px;
  font-size: 18px;
  line-height: 48px;
  font-weight: 700;
  color: #666;
}

</style>
