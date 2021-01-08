<template>
  <div>
    <!-- 面包屑导航栏 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>用户收货地址</el-breadcrumb-item>
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
            @change="getDeliveryList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getDeliveryList"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-cascader
            :options="cityOptions"
            v-model="queryInfo.province"
            :props="cityProps"
            clearable
            filterable
            @change="getDeliveryList"
          >
          </el-cascader>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="openAddDialog">添加地址</el-button>
        </el-col>
        <el-col :span="2">
          <el-button icon="el-icon-refresh" circle @click="getDeliveryList"></el-button>
        </el-col>
      </el-row>

      <!-- 卡片视图区域 -->
      <el-table :data="deliveryList" border stripe>
        <el-table-column label="ID" prop="id"></el-table-column>
        <el-table-column label="收件人" prop="recipient"></el-table-column>
        <el-table-column label="电话" prop="phone"></el-table-column>
        <el-table-column label="省/市" prop="province"></el-table-column>
        <el-table-column label="详细地址" prop="address"></el-table-column>
        <el-table-column label="归属用户" prop="user"></el-table-column>
        <el-table-column label="用户ID" prop="userID" v-if="false"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <!-- 修改按钮 -->
            <el-tooltip
              class="item"
              effect="dark"
              content="修改"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
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
                @click="deleteDelivery(scope.row.id)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 修改地址的对话框 -->
    <el-dialog
      title="修改地址信息"
      :visible.sync="editDialogVisible"
      width="30%"
      @close="editDialogClosed"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editFormRules"
        label-width="80px"
      >
        <el-form-item label="收货人" prop="recipient">
          <el-input v-model="editForm.recipient"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="editForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="省/市" prop="province">
          <el-cascader
            :options="cityOptions"
            v-model="editForm.province"
            :props="cityProps"
            clearable
            filterable
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="详细地址" prop="address">
          <el-input v-model="editForm.address"></el-input>
        </el-form-item>
        <el-form-item label="归属用户" prop="user">
          <el-select
            v-model="editForm.user"
            filterable
            clearable
            placeholder="请选择"
            :disabled="this.$store.state.userInfo.is_superuser ? false : true"
          >
            <el-option
              v-for="item in userList"
              :key="item.id"
              :label="item.username"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateDelivery">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 添加收货地址的对话框 -->
    <el-dialog
      title="添加地址"
      :visible.sync="addDialogVisible"
      width="30%"
      @close="addDialogClosed"
    >
      <!-- 内容主体 -->
      <el-form ref="addFormRef" :model="addForm" :rules="addFormRules" label-width="80px">
        <el-form-item label="收货人" prop="recipient">
          <el-input v-model="addForm.recipient"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="addForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="省/市" prop="province">
          <el-cascader
            :options="cityOptions"
            v-model="addForm.province"
            :props="cityProps"
            clearable
            filterable
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="详细地址" prop="address">
          <el-input v-model="addForm.address"></el-input>
        </el-form-item>
        <el-form-item label="归属用户" prop="user">
          <el-select
            v-model="addForm.user"
            filterable
            clearable
            placeholder="请选择"
            :disabled="this.$store.state.userInfo.is_superuser ? false : true"
          >
            <el-option
              v-for="item in userList"
              :key="item.id"
              :label="item.username"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <!-- 底部区域 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addDelivery">确 定</el-button>
      </span>
    </el-dialog>

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
  </div>
</template>

<script>
import cityOptions from "../../assets/js/citydata";
export default {
  data() {
    return {
      cityOptions,
      cityProps: {
        expandTrigger: "hover",
      },
      // 获取收货地址列表对象
      queryInfo: {
        query: "",
        province: [],
        pagenum: 1,
        pagesize: 10,
      },
      //添加表单
      addForm: {
        recipient: "",
        phone: "",
        province: [],
        address: "",
        user: this.$store.state.userInfo.username,
      },
      //修改表单
      editForm: {
        id: 0,
        recipient: "",
        phone: "",
        province: [],
        address: "",
        user: "",
      },
      //添加表单规则
      addFormRules: {
        recipient: [{ required: true, message: "请输入收件人姓名", trigger: "blur" }],
        phone: [
          { required: true, message: "请输入联系电话", trigger: "blur" },
          { min: 11, max: 11, message: "请输入正确格式的手机号码", trigger: "blur" },
          { min: 11, max: 11, message: "请输入正确格式的手机号码", trigger: "change" },
        ],
        province: [
          { required: true, message: "请选择省/市", trigger: "blur" },
          { required: true, message: "请选择省/市", trigger: "change" },
        ],
        address: [{ required: true, message: "请输入详细地址", trigger: "blur" }],
        user: [
          { required: true, message: "请选择归属用户", trigger: "blur" },
          { required: true, message: "请选择归属用户", trigger: "change" },
        ],
      },
      //修改表单规则
      editFormRules: {
        recipient: [{ required: true, message: "请输入收件人姓名", trigger: "blur" }],
        phone: [
          { required: true, message: "请输入联系电话", trigger: "blur" },
          { min: 11, max: 11, message: "请输入正确格式的手机号码", trigger: "blur" },
          { min: 11, max: 11, message: "请输入正确格式的手机号码", trigger: "change" },
        ],
        province: [
          { required: true, message: "请选择省/市", trigger: "blur" },
          { required: true, message: "请选择省/市", trigger: "change" },
        ],
        address: [{ required: true, message: "请输入详细地址", trigger: "blur" }],
        user: [
          { required: true, message: "请选择归属用户", trigger: "blur" },
          { required: true, message: "请选择归属用户", trigger: "change" },
        ],
      },
      //收货地址信息列表
      deliveryList: [],
      //添加收货地址归属的请求用户列表
      userList: [],
      //收货地址信息列表返回总数
      total: 0,
      //添加收货地址对话框
      addDialogVisible: false,
      //修改收货地址对话框
      editDialogVisible: false,
    };
  },
  created() {
    this.getDeliveryList();
    this.getUserList();
  },
  methods: {
    //获取收货地址列表
    async getDeliveryList() {
      const { data: res } = await this.$http.get("delivery/", { params: this.queryInfo });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      //   console.log(this.queryInfo)
      this.deliveryList = res.data.deliveryList;
      this.total = res.data.total;
    },
    //获取用户列表
    async getUserList() {
      const { data: res } = await this.$http.get("users/", {
        params: {
          query: "",
          pagenum: 1,
          pagesize: 10000000,
        },
      });
      if (res.meta.code !== 200) return this.$message.error("获取用户列表失败！");
      this.userList = res.data.userlist;
    //   console.log(this.userList)
    },
    //显示修改对话框
    showEditDialog(row) {
        console.log(row)
      this.editForm.id = row.id;
      this.editForm.recipient = row.recipient;
      this.editForm.phone = row.phone;
      this.editForm.address = row.address;
      var temp = row.province.split("/");
      this.editForm.province = temp;
      this.editForm.user = row.userID;
      this.editDialogVisible = true;
    },
    //删除地址对话框
    async deleteDelivery(id) {
      const confirmResult = await this.$confirm(
        "此操作将永久删除该地址, 是否继续?",
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
      const { data: res } = await this.$http.delete("delivery/", { data: { id: id } });
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.$message.success(res.meta.message);
      this.getDeliveryList();
    },
    // 打开添加对话框
    openAddDialog() {
      this.addDialogVisible = true;
      //   console.log(this.userList);
    },
    //添加地址
    async addDelivery() {
      this.$refs.addFormRef.validate(async (valid) => {
        if (!valid) return;
        const { data: res } = await this.$http.post("delivery/", this.addForm);
        // console.log(res)
        if (res.meta.code !== 200) {
          return this.$message.error(res.meta.message);
        }
        this.$message.success(res.meta.message);
        // 隐藏添加提示框
        this.addDialogVisible = false;
        // 重新获取地址数据
        this.getDeliveryList();
      });
    },
    //修改地址
    async updateDelivery() {
      console.log(this.editForm);
      this.$refs.editFormRef.validate(async (valid) => {
        if (!valid) return;
        const { data: res } = await this.$http.put("delivery/", this.editForm);
        // console.log(res)
        if (res.meta.code !== 200) {
          return this.$message.error(res.meta.message);
        }
        this.$message.success(res.meta.message);
        // 隐藏添加提示框
        this.editDialogVisible = false;
        // 重新获取地址数据
        this.getDeliveryList();
      });
    },
    //添加地址对话框关闭事件
    addDialogClosed() {
      this.$refs.addFormRef.resetFields();
    },
    //修改地址对话框关闭事件
    editDialogClosed() {
      this.$refs.editFormRef.resetFields();
    },
    //每页数量变化
    handleSizeChange() {
      this.queryInfo.pagesize = newSize;
      this.getDeliveryList();
    },
    //页码变化
    handleCurrentChange() {
      this.queryInfo.pagenum = newPage;
      this.getDeliveryList();
    },
  },
};
</script>

<style lang="less" scoped>
.el-cascader {
  width: 100%;
}
.el-select {
  width: 100%;
}
</style>
