<template>
  <div>
    <!-- 商家列表 -->

    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商铺管理</el-breadcrumb-item>
      <el-breadcrumb-item>商铺列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区域 -->
    <el-card>
      <!-- 顶部搜索栏区域 -->
      <el-row :gutter="20">
        <el-col :span="7">
          <el-input
            placeholder="请输入内容"
            v-model="queryInfo.query"
            clearable
            @change="getMerchantList"
            @clear="getMerchantList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getMerchantList"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button
            type="primary"
            @click="openAddDialog"
            :disabled="this.$store.state.userInfo.is_superuser ? false : true"
            >添加商铺</el-button
          >
        </el-col>
      </el-row>

      <!-- 列表区域 -->
      <el-table :data="merchantList" border stripe>
        <el-table-column label="商铺ID" prop="id"></el-table-column>
        <el-table-column label="商铺名称" prop="name"></el-table-column>
        <el-table-column label="商铺管理员" prop="admin_name"></el-table-column>
        <el-table-column label="商铺介绍" prop="introduce"></el-table-column>
        <el-table-column label="商铺管理员ID" prop="admin" v-if="false"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <!-- 修改按钮 -->
            <el-tooltip
              class="item"
              effect="dark"
              content="编辑"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="small"
                @click="showEditDialog(scope.row)"
              >
              </el-button>
            </el-tooltip>

            <!-- 删除按钮 -->
            <el-tooltip
              class="item"
              effect="dark"
              content="删除"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="small"
                @click="deleteMerchant(scope.row.id)"
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

    <!-- 修改商铺信息的对话框 -->
    <el-dialog title="修改店铺信息" :visible.sync="editDialogVisible" width="40%">
      <el-form ref="editFormRef" :model="editForm" :rules="FormRules" label-width="90px" label-position="left">
        <el-form-item label="店铺名称" prop="name">
          <el-input v-model="editForm.name"></el-input>
        </el-form-item>
        <el-form-item label="管理员" prop="admin">
          <el-select
            v-model="editForm.admin"
            filterable
            clearable
            placeholder="请选择"
            :disabled="this.$store.state.userInfo.is_superuser ? false : true"
          >
            <el-option
              v-for="admin in admin_select"
              :key="admin.admin"
              :label="admin.admin_name"
              :value="admin.admin"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="店铺简介" prop="introduce">
          <el-input
            type="textarea"
            :autosize="{ minRows: 1, maxRows: 4 }"
            placeholder="请输入内容"
            v-model="editForm.introduce"
          >
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateMerchant">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 添加商铺信息的对话框 -->
    <el-dialog title="添加店铺" :visible.sync="addDialogVisible" width="40%">
      <el-form ref="addFormRef" :model="addForm" :rules="FormRules" label-width="90px" label-position="left">
        <el-form-item label="店铺名称" prop="name">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>
        <el-form-item label="管理员" prop="admin">
          <el-select
            v-model="addForm.admin"
            filterable
            clearable
            placeholder="请选择"
            :disabled="this.$store.state.userInfo.is_superuser ? false : true"
          >
            <el-option
              v-for="admin in admin_select"
              :key="admin.admin"
              :label="admin.admin_name"
              :value="admin.admin"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="店铺简介" prop="introduce">
          <el-input
            type="textarea"
            :autosize="{ minRows: 1, maxRows: 4 }"
            placeholder="请输入内容"
            v-model="addForm.introduce"
          >
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addMerchant">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 查询对象
      queryInfo: {
        query: "",
        pagenum: 1,
        pagesize: 10,
      },
      // 编辑表单
      editForm: {
        id: 0,
        name: "",
        admin: 0,
        introduce: "",
      },
      // 新增表单
      addForm: {
        name: "",
        admin: null,
        introduce: "",
      },
      // 编辑表单规则
      FormRules: {
        name: [{ required: true, message: "请输入店铺名", trigger: "blur" }],
        admin: [{ required: true, message: "请选择管理员", trigger: "blur" }],
      },
      // 返回商铺数据集
      merchantList: [],
      // 商铺数据集数量
      total: 0,
      // 商店管理员选择器
      admin_select: [],
      // 修改对话框显示
      editDialogVisible: false,
      // 添加对话框显示
      addDialogVisible: false,
    };
  },
  created() {
    this.getMerchantList();
  },
  methods: {
    // 获取商家列表
    async getMerchantList() {
      const { data: res } = await this.$http.get("merchant/", { params: this.queryInfo });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.merchantList = res.data.merchant;
      this.total = res.data.total;
    },
    //显示修改对话框
    showEditDialog(row) {
      this.editForm.id = row.id;
      this.editForm.name = row.name;
      this.editForm.admin = row.admin;
      this.editForm.introduce = row.introduce;
      this.getMerchantAdmin();
      this.editDialogVisible = true;
    },
    // 更新商铺信息
    async updateMerchant() {
      this.$refs.editFormRef.validate(async (valid) => {
        if (!valid) return;
        const { data: res } = await this.$http.put("merchant/", this.editForm);
        if (res.meta.code !== 200) {
          return this.$message.error(res.meta.message);
        }
        this.$message.success(res.meta.message);
        this.editDialogVisible = false;
        this.getMerchantList();
      });
    },
    // 获得管理员选择器内容
    async getMerchantAdmin() {
      const { data: res } = await this.$http.get("merchantAdmin/");
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.admin_select = res.data.admin_list;
    },
    // 打开添加对话框
    openAddDialog() {
      this.getMerchantAdmin();
      this.addDialogVisible = true;
    },
    // 添加商铺
    async addMerchant() {
      this.$refs.addFormRef.validate(async (valid) => {
        if (!valid) return;
        const { data: res } = await this.$http.post("merchant/", this.addForm);
        if (res.meta.code !== 200) {
          return this.$message.error(res.meta.message);
        }
        this.$message.success(res.meta.message);
        this.addDialogVisible = false;
        this.getMerchantList();
      });
    },
    //删除地址对话框
    async deleteMerchant(id) {
      const confirmResult = await this.$confirm(
        "此操作将永久删除该商铺以及该商品下的所有商品, 是否继续?",
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
      const { data: res } = await this.$http.delete("merchant/", { data: { id: id } });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.$message.success(res.meta.message);
      this.getMerchantList();
    },
    // 监听pagesize改变的事件
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize;
      this.getMerchantList();
    },
    // 监听页码值改变的事件
    handleCurrentChange(newPage) {
      this.queryInfo.pagenum = newPage;
      this.getMerchantList();
    },
  },
};
</script>

<style lang="less" scoped></style>
