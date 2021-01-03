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
          <el-input
            placeholder="请输入内容"
            v-model="queryInfo.query"
            clearable
            @change="getUserList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getUserList"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="addDialogVisible = true">添加用户</el-button>
        </el-col>
      </el-row>

      <!-- 添加用户的对话框 -->
      <el-dialog
        title="添加用户"
        :visible.sync="addDialogVisible"
        width="30%"
        @close="addDialogClosed"
      >
        <!-- 内容主体 -->
        <el-form
          ref="addFormRef"
          :model="addForm"
          :rules="addFormRules"
          label-width="70px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="addForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="addForm.password"></el-input>
          </el-form-item>
          <!-- <el-form-item label="确认密码" prop="checkPass">
                        <el-input v-model="addForm.checkPass"></el-input>
                    </el-form-item> -->
          <el-form-item label="角色">
            <el-radio-group v-model="addForm.mg_state" size="medium">
              <el-radio-button border :label="1">普通用户</el-radio-button>
              <el-radio-button border :label="2">商家</el-radio-button>
              <el-radio-button border :label="3">管理员</el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>

        <!-- 底部区域 -->
        <span slot="footer" class="dialog-footer">
          <el-button @click="addDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="addUser">确 定</el-button>
        </span>
      </el-dialog>

      <!-- 修改用户的对话框 -->
      <el-dialog title="修改密码" :visible.sync="editDialogVisible" width="30%">
        <el-form
          ref="editFormRef"
          :model="editForm"
          :rules="editFormRules"
          label-width="70px"
        >
          <el-form-item label="用户名">
            <el-input v-model="editForm.username" disabled></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="editForm.password"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="editDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="updateUser">确 定</el-button>
        </span>
      </el-dialog>

      <!-- 修改用户身份的对话框 -->
      <el-dialog title="修改身份" :visible.sync="editRoleDialogVisible" width="30%" >
        <el-form
          ref="editRoleFormRef"
          :model="editRoleForm"
          :rules="editRoleFormRules"
          label-width="70px"
        >
          <el-form-item label="角色" prop="role">
            <el-radio-group v-model="editRoleForm.role" size="medium">
              <el-radio-button border :label="1">普通用户</el-radio-button>
              <el-radio-button border :label="2">商家</el-radio-button>
              <el-radio-button border :label="3">管理员</el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="editRoleDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="updateUserRole">确 定</el-button>
        </span>
      </el-dialog>

      <!-- 用户列表区 -->
      <el-table :data="userlist" border stripe>
        <!-- <el-table-column type="index" label="#"></el-table-column> -->
        <el-table-column label="ID" prop="id" width="85px"></el-table-column>
        <el-table-column label="用户名" prop="username" width="105px"></el-table-column>
        <el-table-column label="手机号" prop="phone"></el-table-column>
        <el-table-column label="邮箱" prop="email"></el-table-column>
        <el-table-column label="角色" prop="role_name"></el-table-column>
        <el-table-column label="可用状态">
          <template slot-scope="scope">
            <el-switch
              v-model="scope.row.state"
              active-color="#13ce66"
              inactive-color="#ff4949"
              @change="userStateChanged(scope.row)"
            >
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <!-- 修改按钮 -->
            <el-tooltip
              class="item"
              effect="dark"
              content="修改密码"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                @click="showEditDialog(scope.row.id)"
              >
              </el-button>
            </el-tooltip>

            <!-- 删除按钮 -->
            <el-tooltip
              class="item"
              effect="dark"
              content="删除用户"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                @click="deleteUser(scope.row.id)"
              ></el-button>
            </el-tooltip>

            <!-- 分配角色按钮 -->
            <el-tooltip
              class="item"
              effect="dark"
              content="分配角色"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="warning"
                icon="el-icon-setting"
                @click="showEditRoleDialog(scope.row.id)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-sizes="[10, 20, 50]"
        :page-size="queryInfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    var checkUsername = (rule, value, callback) => {
      var data = this.$http.get(`checkUsable/${value}`).then((res) => {
        console.log(res.data);
        if (res.data.meta.code !== 200) {
          callback(new Error("用户名已被使用！"));
        } else {
          callback();
        }
      });
    };

    return {
      // 获取用户列表的参数对象
      queryInfo: {
        query: "",
        pagenum: 1,
        pagesize: 10,
      },
      // 用户列表
      userlist: [],
      total: 0,
      // 添加用户对话框显示
      addDialogVisible: false,
      // 修改用户对话框显示
      editDialogVisible: false,
      //修改用户角色对话框
      editRoleDialogVisible: false,
      // 添加用户表单数据
      addForm: {
        username: "",
        password: "",
        mg_state: 1,
      },
      // 修改信息表单数据
      editForm: {
        id: "",
        username: "",
        password: "",
      },
      //修改用户角色表单数据
      editRoleForm: {
        id: "",
        role: "",
      },
      // 添加用户表单验证规则对象
      addFormRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          {
            min: 3,
            max: 10,
            message: "长度在 3 到 10 个字符之间",
            trigger: "blur",
          },
          {
            min: 3,
            max: 10,
            message: "长度在 3 到 10 个字符之间",
            trigger: "change",
          },
          {
            validator: checkUsername,
            message: "用户名已被使用！",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 16,
            message: "长度在 6 到 16 个字符之间",
            trigger: "blur",
          },
          {
            min: 6,
            max: 16,
            message: "长度在 6 到 16 个字符之间",
            trigger: "change",
          },
        ],
      },
      // 修改用户表单规则
      editFormRules: {
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 16,
            message: "长度在 6 到 16 个字符之间",
            trigger: "blur",
          },
          {
            min: 6,
            max: 16,
            message: "长度在 6 到 16 个字符之间",
            trigger: "change",
          },
        ],
      },
      //更改用户角色表单规则
      editRoleFormRules: {
        role: [{ required: true, message: "请选择用户角色", trigger: "blur" }]
      },
    };
  },
  created() {
    this.getUserList();
  },
  methods: {
    async getUserList() {
      const { data: res } = await this.$http.get("users", {
        params: this.queryInfo,
      });
      if (res.meta.code !== 200) return this.$message.error("获取用户列表失败！");
      this.userlist = res.data.userlist;
      this.total = res.data.total;
    },
    // 监听pagesize改变的事件
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize;
      this.getUserList();
    },
    // 监听页码值改变的事件
    handleCurrentChange(newPage) {
      this.queryInfo.pagenum = newPage;
      this.getUserList();
    },
    // 监听用户状态改变
    async userStateChanged(userinfo) {
      var stateTemp = 0;
      if (userinfo.state === true) {
        stateTemp = 1;
      }

      const { data: res } = await this.$http.put(
        `users/${userinfo.id}/state/${stateTemp}`
      );
      console.log(res);
      if (res.meta.code !== 200) {
        userinfo.state = !userinfo.state;
        return this.$message.error("更新状态失败");
      }
      this.$message.success("更新状态成功");
    },
    // 监听添加用户对话框的关闭事件
    addDialogClosed() {
      this.$refs.addFormRef.resetFields();
      this.addForm.mg_state = 1;
    },
    // 添加用户
    addUser() {
      this.$refs.addFormRef.validate(async (valid) => {
        if (!valid) return;
        const { data: res } = await this.$http.post("users/", this.addForm);
        // console.log(res)
        if (res.meta.code !== 201) {
          return this.$message.error(res.meta.message);
        }
        this.$message.success(res.meta.message);
        // 隐藏添加提示框
        this.addDialogVisible = false;
        // 重新获取用户数据
        this.getUserList();
      });
    },
    // 修改用户密码
    updateUser() {
      this.$refs.editFormRef.validate(async (valid) => {
        if (!valid) return;
        const { data: res } = await this.$http.put("users/", this.editForm);
        // console.log(res)
        if (res.meta.code !== 201) {
          return this.$message.error(res.meta.message);
        }
        this.$message.success(res.meta.message);
        // 隐藏添加提示框
        this.editDialogVisible = false;
        // 重新获取用户数据
        this.getUserList();
      });
    },
    // 监听修改用户对话框的关闭事件
    editDialogClosed() {
      this.$refs.editFormRef.resetFields();
    },
    // 显示编辑用户的对话框
    async showEditDialog(id) {
      const { data: res } = await this.$http.get("users/" + id);
      if (res.meta.code !== 200) return this.$message.error("获取信息失败");
      this.editForm = res.data;
      this.editDialogVisible = true;
      // console.log(id)
    },
    // 显示更改用户角色的对话框
    async showEditRoleDialog(id) {
      this.editRoleForm.id = id;
      this.editRoleDialogVisible = true;
    },
    //更新用户角色
    async updateUserRole() {
      // console.log(this.editRoleForm)
      const { data:res} = await this.$http.patch("users/",this.editRoleForm)
      if(res.meta.code!==200){
        return this.$message.error(res.meta.message);
      }
      this.$message.success(res.meta.message);
      this.getUserList();
      this.$refs.editRoleFormRef.resetFields();
      this.editRoleDialogVisible = false;
      return;
    },
    // 删除用户确认弹框
    async deleteUser(id) {
      // console.log(id)
      const confirmResult = await this.$confirm(
        "此操作将永久删除该用户, 是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      ).catch((res) => res);

      if (confirmResult !== "confirm") {
        return this.$message.info("已取消删除");
      }
      const { data: res } = await this.$http.delete("users/", { data: { id: id } });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.$message.success(res.meta.message);
      this.getUserList();
      // console.log(res);
    },
  },
};
</script>

<style lang="less" scoped></style>
