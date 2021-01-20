<template>
  <el-container class="home-container">
    <!-- 头部区域 -->
    <el-header>
      <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
      >
        <el-menu-item index="1">首页</el-menu-item>
        <el-menu-item index="2">全部商品类型</el-menu-item>
        <!-- <el-submenu index="2">
          <template slot="title">我的工作台</template>
          <el-menu-item index="2-1">选项1</el-menu-item>
          <el-menu-item index="2-2">选项2</el-menu-item>
          <el-menu-item index="2-3">选项3</el-menu-item>
          <el-submenu index="2-4">
            <template slot="title">选项4</template>
            <el-menu-item index="2-4-1">选项1</el-menu-item>
            <el-menu-item index="2-4-2">选项2</el-menu-item>
            <el-menu-item index="2-4-3">选项3</el-menu-item>
          </el-submenu>
        </el-submenu> -->
        <!-- <el-menu-item index="3">消息中心</el-menu-item> -->
        <el-menu-item index="4">
          <a href="https://github.com/Mustard030/vue-django-shop" target="_blank">Github</a>
        </el-menu-item>
      </el-menu>
    </el-header>

    <!-- 页面主体 -->
    <el-container>
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
      activeIndex: "1",
    };
  },
  created() {},
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
  },
};
</script>
<style lang="less" scoped>
.el-menu{
    padding-left: 100px;
    padding-right: 100px;
}
</style>
