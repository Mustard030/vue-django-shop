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
                    <el-tag type="warning" v-else-if="scope.row.cat_level === 1">二级</el-tag>
                </template>
                <template v-slot:opt="scope">
                    <el-button type="primary" icon="el-icon-edit" size="mini" @click="showRenameDialog(scope.row)">编辑</el-button>
                    <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteCate(scope.row.cat_id)">删除</el-button>
                </template>
            </tree-table>

            <!-- 分页区域 -->
        </el-card>

        <!-- 添加信息的对话框 -->
        <el-dialog title="添加分类" :visible.sync="addDialogVisible"
                    width="45%" @closed="closeAddCateDialog">
            <el-form :model="addCateForm" :rules="addCateFormRules" ref="addCateFormRef" label-width="100px">
                <el-form-item label="分类名称：" prop="cat_name" >
                    <el-input v-model="addCateForm.cat_name"></el-input>
                </el-form-item>
                <el-form-item label="父级分类：" prop="parentCateId">
                    <el-select v-model="addCateForm.parentCateId" placeholder="不选择则自身为父级分类" @change="parentCateChanged" clearable>
                        <el-option
                        v-for="item in parentCateList"
                        :key="item.cat_id"
                        :label="item.cat_name"
                        :value="item.cat_id"
                        >
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible=false">取 消</el-button>
                <el-button type="primary" @click="addCate">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 修改信息的对话框 -->
        <el-dialog title="重命名分类" :visible.sync="renameDialogVisible"
                    width="45%" 
                    >
            <el-form :model="renameCateForm" :rules="renameCateFormRules" ref="renameCateFormRef" label-width="100px">
                <el-form-item label="分类名称：" prop="cat_name" >
                    <el-input v-model="renameCateForm.cat_name"></el-input>
                </el-form-item>
                
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="renameDialogVisible=false">取 消</el-button>
                <el-button type="primary" @click="renameCate">确 定</el-button>
            </span>
        </el-dialog>

        
    </div>
</template>

<script>
    export default{
        data(){
            var checkCatename = (rule, value, callback) => {
                var data = this.$http.get(`checkCateNameUseable/${value}`).then(res => {
                    // console.log(res.data)
                    if (res.data.meta.code !== 200) {
                        callback(new Error('分类名已被使用！'))
                    } else {
                    callback()
                    }
                })
            }
            return {
                // queryInfo:{
                //     type:3
                // },
                
                // 商品分类的数据列表
                catelist:[],
                total:0,
                // 表单列
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
                renameDialogVisible:false,
                addDialogVisible: false,
                //添加分类的表单数据项
                addCateForm:{
                    cat_name:'',
                    parentCateId:'',
                },
                //添加分类表单的验证规则
                addCateFormRules:{
                    cat_name: [
                        {
                            required:true,
                            message: '请输入分类名称',
                            trigger: 'blur'
                        },
                        {
                            min: 1,
                            max: 10,
                            message: '长度在 1 到 10 个字符之间',
                            trigger: 'blur'
                        },
                        {
                            min: 1,
                            max: 10,
                            message: '长度在 1 到 10 个字符之间',
                            trigger: 'change'
                        }
                    ]
                },
                //重命名分类表单的验证规则
                renameCateFormRules:{
                    cat_name: [
                        {
                            required:true,
                            message: '请输入分类名称',
                            trigger: 'blur'
                        },
                        {
                            validator: checkCatename,
                            message: '分类名已被使用！',
                            trigger: 'blur'
                        },
                        {
                            min: 1,
                            max: 10,
                            message: '长度在 1 到 10 个字符之间',
                            trigger: 'blur'
                        },
                        {
                            min: 1,
                            max: 10,
                            message: '长度在 1 到 10 个字符之间',
                            trigger: 'change'
                        }

                    ]
                },
                //重命名分类的表单数据项
                renameCateForm:{
                    cat_name:'',
                    cat_id:'',
                },
                
                //父级分类数据
                parentCateList:[],

            };
        },
        created() {
            this.getCateList()
        },
        methods: {
            // 获取商品分类数据
            async getCateList(){
                const {data:res} = await this.$http.get('categories/'
                ,{params: { type:2 }}
                )
                if (res.meta.code !== 200) return this.$message.error(res.meta.message)

                //数据列表
                this.catelist = res.data
            },
            //添加分类对话框
            showAddDialog(){
                //获取父级分类数据
                this.getParentCateList()
                //显示添加对话框
                this.addDialogVisible=true;
            },
            //重命名分类对话框
            showRenameDialog(row){
                this.renameCateForm.cat_id=row.cat_id
                this.renameCateForm.cat_name=row.cat_name
                // console.log(this.renameCateForm)
                //显示重命名对话框
                this.renameDialogVisible=true;
            },
            //删除分类对话框
            showDeleteCateDialog(){
                
                //显示删除对话框
                this.deleteDialogVisible=true;
            },
            //获取父级分类的数据
            async getParentCateList(){
                const {data:res} = await this.$http.get('categories/'
                ,{params: { type:1 }}
                )
                if (res.meta.code !== 200) return this.$message.error(res.meta.message)
                this.parentCateList = res.data
                // console.log(res.data)
            },
            //父级分类选择项改变则触发
            parentCateChanged(){
                // console.log(this.parentCateId)
            },
            //提交分类
            async addCate(){
                this.$refs.addCateFormRef.validate(async valid => {
                    if (!valid) return
                    const {data:res} = await this.$http.put('categories/',this.addCateForm )
                    if(res.meta.code !== 200) {return this.$message.error(res.meta.message)}
                    
                    this.$message.success(res.meta.message)
                    // 隐藏添加提示框
                    this.addDialogVisible = false
                    // 重新获取分类数据
                    this.getCateList()
                })
            },
            //关闭添加分类窗口
            closeAddCateDialog(){
                // console.log('clear')
                this.$refs.addCateFormRef.resetFields()
                this.addDialogVisible = false
            },
            // 重命名分类
            async renameCate(){
                this.$refs.renameCateFormRef.validate(async valid => {
                    if (!valid) return
                    const {data:res} = await this.$http.post('categories/',this.renameCateForm)
                    // console.log(res)
                    if (res.meta.code !== 200) { return this.$message.error(res.meta.message) }
                    this.$message.success(res.meta.message)
                    // 隐藏添加提示框
                    this.renameDialogVisible = false
                    // 重新获取用户数据
                    this.getCateList()
                })
            },
            // 删除分类
            async deleteCate(id) {
                // console.log(id)
                const confirmResult = await this.$confirm('此操作将永久删除该分类及其子分类, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).catch(res => res)
                // .then(() => {
                //     this.$message({
                //         type: 'success',
                //         message: '删除成功!'
                //     });
                // })

                if (confirmResult !== 'confirm') {
                    return this.$message.info('已取消删除')
                }
                const { data: res } = await this.$http.delete('categories/', { data: { id: id } })
                if (res.meta.code !== 200) {
                    return this.$message.error(res.meta.message)
                }
                this.$message.success(res.meta.message)
                this.getCateList()
                // console.log(res)
            }
        }
    }
</script>

<style lang="less" scoped>
.tree-table {
    margin-top: 10px;
}
.el-select {
    width: 100%;
}
</style>