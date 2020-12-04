<template>
    <div>
        <!-- 面包屑导航区域 -->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>用户管理</el-breadcrumb-item>
            <el-breadcrumb-item>用户列表</el-breadcrumb-item>

        </el-breadcrumb>
        <!-- 卡片视图区域 -->
        <el-card>
            <!-- 搜索栏 -->

            <el-row :gutter="20">
                <el-col :span="7">
                    <el-input placeholder="请输入内容" class="" :query='queryInfo.query'>
                        <el-button slot="append" icon="el-icon-search" @click='getUserList'></el-button>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary">添加用户</el-button>
                </el-col>
            </el-row>

            <!-- 用户列表区 -->
            <el-table :data='userlist' border stripe>
                <!-- <el-table-column type="index" label="#"></el-table-column> -->
                <el-table-column label="ID" prop='id' width='85px'></el-table-column>
                <el-table-column label="用户名" prop='username' width='105px'></el-table-column>
                <el-table-column label="密码" prop='password'></el-table-column>
                <el-table-column label="角色" prop='role_name'></el-table-column>
                <el-table-column label="状态">
                    <template slot-scope="scope">
                        <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"
                            @change="userStateChanged(scope.row)">
                        </el-switch>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <!-- 修改按钮 -->
                        <el-tooltip class="item" effect="dark" content="修改信息" placement="top" :enterable="false">
                            <el-button type="primary" icon="el-icon-edit"></el-button>
                        </el-tooltip>

                        <!-- 删除按钮 -->
                        <el-tooltip class="item" effect="dark" content="删除用户" placement="top" :enterable="false">
                            <el-button type="danger" icon="el-icon-delete"></el-button>
                        </el-tooltip>

                        <!-- 分配角色按钮 -->
                        <el-tooltip class="item" effect="dark" content="分配角色" placement="top" :enterable="false">
                            <el-button type="warning" icon="el-icon-setting"></el-button>
                        </el-tooltip>

                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页区域 -->
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                :current-page="queryInfo.pagenum" :page-sizes="[2, 5, 10, 50]" :page-size="queryInfo.pagesize"
                layout="total, sizes, prev, pager, next, jumper" :total="total">
            </el-pagination>

        </el-card>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                // 获取用户列表的参数对象
                queryInfo: {
                    query: '',
                    pagenum: 1,
                    pagesize: 5
                },
                // 用户列表
                userlist: [],
                total: 0
            }
        },
        created() {
            this.getUserList()
        },
        methods: {
            async getUserList() {
                const { data: res } = await this.$http.get('users', {
                    params: this.queryInfo
                })
                if (res.meta.code !== 200) return this.$message.error('获取用户列表失败！')
                this.userlist = res.data.userlist
                this.total = res.data.total
                
            },
            //监听pagesize改变的事件
            handleSizeChange(newSize) {
                this.queryInfo.pagesize = newSize
                this.getUserList()
            },
            //监听页码值改变的事件
            handleCurrentChange(newPage) {
                this.queryInfo.pagenum = newPage
                this.getUserList()
            },
            //监听用户状态改变
            async userStateChanged(userinfo) {
                
                var state_temp = 0
                if (userinfo.state === true){
                    state_temp = 1
                }
                
                const {data:res}  = await this.$http.put(`users/${userinfo.id}/state/${state_temp}`)
                
                if (res.meta.code !== 200) {
                    userInfo.state = !userinfo.state
                    return this.$message.error('更新状态失败')
                }
                this.$message.success('更新状态成功')

            }
        }

    }
</script>

<style lang="less" scoped>

</style>