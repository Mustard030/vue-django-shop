<template>
    <div>
        <!-- 商品列表页面 -->

        <!-- 面包屑导航栏 -->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>商品管理</el-breadcrumb-item>
            <el-breadcrumb-item>商品条目管理</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 卡片视图区域 -->
        <el-card>
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-input placeholder="请输入内容" v-model="search" clearable>
                        <el-button slot="append" icon="el-icon-search"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary">添加商品</el-button>
                </el-col>
            </el-row>
        </el-card>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                //查询参数对象
                queryInfo:{
                //搜索框内容
                search:'',
                //页数
                page:0,
                //每页条目数
                size:20,
                }
                
            };
        },
        created() {
            this.getGoodsList()
        },
        methods: {
            // 根据分页获取对应的商品列表
            async getGoodsList(){
                const {data:res} = await this.$http.get('goodsList/',{params: this.queryInfo})
            }
        }

    }
</script>
<style lang="less" scoped>

</style>