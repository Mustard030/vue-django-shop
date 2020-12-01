<template>
    <el-container class="home-container">
        <!-- 头部区域 -->
        <el-header>
            <div>
                <img src="..\assets\logo.png" alt="" height="50px">
                <span>电商后台管理系统</span>
            </div>
            <el-button type="danger" @click="logout">退出 </el-button>
        </el-header>
        <!-- 页面主体 -->
        <el-container>
            <!-- 侧边栏 -->
            <el-aside width="200px">
                <!-- 侧边栏菜单区 -->
                <el-menu background-color="#333744" text-color="#fff" active-text-color="#ffd04b">
                    <!-- 一级菜单 -->
                    <el-submenu index="1">
                        <!-- 一级菜单模板区 -->
                        <template slot="title">
                            <!-- 图标 -->
                            <i class="el-icon-location"></i>
                            <!-- 文本 -->
                            <span>导航一</span>
                        </template>
                        <el-menu-item index="1-4-1">选项1</el-menu-item>
                        <el-submenu index="1-4">
                            <template slot="title">选项4</template>
                            <el-menu-item index="1-4-1">选项1</el-menu-item>
                        </el-submenu>
                    </el-submenu>
                    
                </el-menu>

            </el-aside>
            <!-- 主视图 -->
            <el-main>Main

            </el-main>
        </el-container>
    </el-container>
</template>
<script>
    export default {
        created(){
            this.getMenuList()
        },
        methods: {
            logout() {
                window.sessionStorage.clear()
                this.$router.push('/login')
            },
            //获取侧边栏数据
            async getMenuList(){
                const {data:res} = await this.$http.get('menus/')
                console.log('res')
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
    .el-menu{
        border-right: solid 0px #e6e6e6;
    }
</style>