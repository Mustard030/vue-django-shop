<template>
    <div>
        <!-- 面包屑导航区域 -->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>商品管理</el-breadcrumb-item>
            <el-breadcrumb-item>商品类别管理</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 卡片视图区域 -->
        <el-card>
            <!-- 添加按钮 -->
            <el-row>
                <el-col>
                    <el-button type="primary" @click="showAddDialog">添加分类</el-button>
                </el-col>
            </el-row>

            <!-- 表格区域 -->
            <tree-table :data="catelist" :columns = "columns" 
            :selection-type="false" :expand-type="false" show-index
            index-text='#' border>
                <template v-slot:isok="scope">
                    <i class="el-icon-success" style="color: green;" v-if="scope"></i>
                </template>
                <template v-slot:order="scope">
                    <el-tag type="success" v-if="scope.row.cat_level === 0">一级</el-tag>
                    <el-tag type="warning" v-else>二级</el-tag>
                </template>
                <template v-slot:opt="scope">
                    <el-button type="primary" icon="el-icon-edit" size="mini">编辑</el-button>
                    <el-button type="danger" icon="el-icon-delete" size="mini">删除</el-button>
                </template>
            </tree-table>

            <!-- 分页区域 -->
        </el-card>

        <!-- 添加信息的对话框 -->
        <el-dialog title="提示" :visible.sync="addDialogVisible"
                    width="45%" >
            <el-form :model="addCateForm" :rules="addCateFormRules" ref="addCateFormRef" label-width="100px">
                <el-form-item label="分类名称：" prop="cat_name" >
                    <el-input v-model="addCateForm.name"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addDialogVisible = false">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default{
        data(){
            return {
                // queryInfo:{
                //     type:3
                // },
                
                // 商品分类的数据列表
                catelist:[],
                total:0,
                columns:[
                    {
                        label: '分类名称',
                        prop:'cat_name'
                    },
                    {
                        label: '是否有效',
                        type:'template',
                        template: 'isok'
                    },
                    {
                        label: '排序',
                        type:'template',
                        template: 'order'
                    },
                    {
                        label: '操作',
                        type:'template',
                        template: 'opt'
                    }
                ],
                addDialogVisible: false,
                //添加分类的表单数据项
                addCateForm:{
                    cat_name:'',
                    cat_pid:0,
                    cat_level:0
                },
                //添加分类表单的验证规则
                addCateFormRules:{
                    cat_name: [
                        {
                            required:true,
                            message: '请输入分类名称',
                            trigger: 'blur'
                        }
                    ]
                }
            };
        },
        created() {
            this.getCateList()
        },
        methods: {
            // 获取商品分类数据
            async getCateList(){
                const {data:res} = await this.$http.get('categories'
                // ,{params: this.queryInfo}
                )
                if (res.meta.code !== 200) return this.$message.error(res.meta.message)

                //数据列表
                this.catelist = res.data
            },
            showAddDialog(){
                this.addDialogVisible=true;
            }
        }
    }
</script>

<style lang="less" scoped>
.tree-table {
    margin-top: 10px;
}
</style>