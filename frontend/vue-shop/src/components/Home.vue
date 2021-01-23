<template>
    <el-container class="home-container">
        <!-- 头部区域 -->
        <el-header>
            <div>
                <img src="..\assets\logo.png" alt="" height="50px">
                <span>电商后台管理系统</span>
            </div>
            <div>
                <el-avatar :src='this.userava' id="ava"></el-avatar>
                <div id="username">您好！{{this.userInfo.username}}</div>
            <el-button type="danger" @click="logout"> <i class="el-icon-switch-button"></i>
                退出 </el-button>
            </div>
        </el-header>
        <!-- 页面主体 -->
        <el-container>
            <!-- 侧边栏 -->
            <el-aside width="200px">
                <!-- 侧边栏菜单区 -->
                <el-menu background-color="#333744" text-color="#fff"
                active-text-color="#ffd04b" unique-opened router
                :default-active="activePath"
                >
                    <!-- 一级菜单 -->
                    <el-submenu :index="item.id + ''" v-for="item in menulist" :key="item.id">
                        <!-- 一级菜单模板区 -->
                        <template slot="title">
                            <span>{{item.authname}}</span>
                        </template>
                        <!-- 二级菜单 -->
                        <el-menu-item :index="'/'+subItem.path" v-for="subItem in item.children"
                        :key="subItem.id" @click="saveNavState('/'+subItem.path)">
                            <template slot="title">
                                <!-- 图标 -->
                                <i class="el-icon-menu"></i>
                                <!-- 文本 -->
                                <span>{{subItem.authname}}</span>
                            </template>
                        </el-menu-item>
                    </el-submenu>

                </el-menu>

            </el-aside>
            <!-- 主视图 -->
            <el-main>
                <!-- 欢迎页占位符 -->
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>
<script>
export default {
  data() {
    return {
      menulist: [],
      // 激活的地址
      activePath: '',
      userInfo:{
          avatar: '',
          token: '',
          userId: '',
          userName: ''
      },
      userava:'',
    }
  },
  created() {
    this.getMenuList()
    this.activePath = window.sessionStorage.getItem('activePath')
    this.userInfo=this.$store.state.userInfo
    this.userava = this.$store.state.BACKEND_URL+this.userInfo.avatar
    
  },
  methods: {
    logout() {
      window.sessionStorage.clear()
      window.localStorage.clear()
      this.$router.push('/adminlogin')
    },
    // 获取侧边栏数据
    async getMenuList() {
      const { data: res } = await this.$http.get('menus/')

      if (res.meta.code !== 200) { return this.$message.error(res.meta.message) }
      this.menulist = res.data
    //   console.log(res)
    },
    // 保存链接的激活状态
    saveNavState(activePath) {
      window.sessionStorage.setItem('activePath', activePath)
      this.activePath = activePath
    }
  }
}
</script>
<style lang="less" scoped>
    .home-container {
        height: 100%;
    }

    .el-header {
        background-color: #373d41;
        display: flex;
        justify-content: space-between;
        font-size: 20px;
        color: #ffffff;
        align-items: center;

        >div {
            display: flex;
            align-items: center;

        }
    }

    .el-aside {
        background-color: #333744;
    }

    .el-main {
        background-color: #eaedf1;
    }

    .el-menu {
        border-right: none;
    }

    #username{
        margin-right: 20px;
        font-size: 15px;
    }

    #ava{
        margin-right: 15px;
    }
</style>
