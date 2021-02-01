<template>
  <div>
    <el-card>
      <div slot="header">
        <span style="font-size: 20px">个人信息</span>
      </div>
      <div>
        <div class="ava">
          <el-upload
            class="avatar-uploader"
            :action="uploadUrl"
            :show-file-list="false"
            :headers="headersObj"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <img
              v-if="imageUrl"
              :src="this.$store.state.BACKEND_URL + this.$store.state.userInfo.avatar"
              class="avatar"
            />
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
          <p class="tishi">点击头像可修改</p>
        </div>
        <div class="info">
          <p>
            绑定手机:{{
              this.$store.state.userInfo.phone | phoneHidden
            }}&nbsp;&nbsp;<el-link icon="el-icon-edit" @click="showEditPhoneDialog"
              >编辑</el-link
            >
          </p>
          <p>
            绑定邮箱:{{ this.$store.state.userInfo.email }}&nbsp;&nbsp;<el-link
              icon="el-icon-edit"
              @click="showEditEmailDialog"
              >编辑</el-link
            >
          </p>
          <el-link type="primary" @click="showEditPasswordDialog">修改密码</el-link>
        </div>
      </div>
    </el-card>
    <!-- 修改手机号对话框 -->
    <el-dialog title="修改手机号" :visible.sync="editPhoneDialogVisible" width="30%" @closed="editPhoneDialogClosed">
      <el-form
        ref="editPhoneFormRef"
        :model="editPhoneForm"
        :rules="editFormRules"
        label-width="70px"
        label-position="left"
      >
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="editPhoneForm.phone"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editPhoneDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updatePhone">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改邮箱的对话框 -->
    <el-dialog title="修改邮箱" :visible.sync="editEmailDialogVisible" width="30%" @closed="editEmailDialogClosed">
      <el-form
        ref="editEmailFormRef"
        :model="editEmailForm"
        :rules="editFormRules"
        label-width="70px"
        label-position="left"
      >
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editEmailForm.email"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editEmailDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateEmail">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改密码的对话框 -->
    <el-dialog title="修改密码" :visible.sync="editPasswordDialogVisible" width="30%" @closed="editPasswordDialogClosed">
      <el-form
        ref="editPasswordFormRef"
        :model="editPasswordForm"
        :rules="editFormRules"
        label-width="100px"
        label-position="left"
      >
        <el-form-item label="密码" prop="password">
          <el-input v-model="editPasswordForm.password" show-password></el-input>
        </el-form-item>
        <el-form-item label="再次输入密码" prop="secPassword">
          <el-input v-model="editPasswordForm.secPassword" show-password></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editPasswordDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updatePassword">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    var checkUsername = (rule, value, callback) => {
      var data = this.$http.get(`checkUsable/${value}`).then((res) => {
        // console.log(res.data);
        if (res.data.meta.code !== 200) {
          callback(new Error("用户名已被使用！"));
        } else {
          callback();
        }
      });
    };
    var doublePassWord = (rule,value,callback) => {
      if (value !== this.editPasswordForm.password){callback(new Error("两次密码不一致！"));}
      else{callback();}
    };
    return {
      // 图片上传地址
      uploadUrl: "http://localhost:80/api/private/userAvatar/",
      // 文件上传的请求头
      headersObj: {
        Authorization: window.sessionStorage.getItem("token"),
      },
      // 头像地址
      imageUrl: this.$store.state.BACKEND_URL + this.$store.state.userInfo.avatar,
      // 修改用户密码对话框显示
      editPasswordDialogVisible: false,
      // 修改手机号对话框显示
      editPhoneDialogVisible: false,
      // 修改邮箱对话框显示
      editEmailDialogVisible: false,
      // 修改密码表单
      editPasswordForm: {
        id: this.$store.state.userInfo.userId,
        password: "",
        secPassword: "",
      },
      // 修改手机号表单
      editPhoneForm: {
        id: this.$store.state.userInfo.userId,
        phone: "",
      },
      // 修改邮箱表单
      editEmailForm: {
        id: this.$store.state.userInfo.userId,
        email: "",
      },
      // 修改用户表单规则
      editFormRules: {
        password: [
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
        secPassword:[
          {
            validator: doublePassWord,
            message: "两次密码不一致！",
            trigger: "blur",
          },
        ],
        phone: [
          {
            min: 11,
            max: 11,
            message: "请输入正确格式的手机号码",
            trigger: "blur",
          },
          {
            min: 11,
            max: 11,
            message: "请输入正确格式的手机号码",
            trigger: "change",
          },
        ],
        email: [
          {
            type: "string",
            message: "邮箱格式不正确",
            trigger: "blur",
            transform(value) {
              if (
                !/^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/.test(
                  value
                )
              ) {
                return true;
              } else {
              }
            },
          },
          { type: "string", message: "长度不能超过30位", trigger: "blur", max: 30 },
        ],
      },
    };
  },
  filters: {
    phoneHidden: function (phone) {
      let reg = /^(.{3}).*(.{4})$/;
      return phone.replace(reg, "$1****$2");
    },
  },
  created() {},
  methods: {
    // 修改手机号对话框显示
    showEditPhoneDialog() {
      this.editPhoneDialogVisible = true;
    },
    showEditEmailDialog() {
      this.editEmailDialogVisible = true;
    },
    showEditPasswordDialog() {
      this.editPasswordDialogVisible = true;
    },
    // 修改用户手机号
    updatePhone() {
      this.$refs.editPhoneFormRef.validate(async (valid) => {
        if (!valid) return;
        const { data: res } = await this.$http.put("users/", this.editPhoneForm);
        // console.log(res)
        if (res.meta.code !== 201) {
          return this.$message.error(res.meta.message);
        }
        this.$message.success(res.meta.message);
        // 隐藏添加提示框
        this.editPhoneDialogVisible = false;
        // 重新获取用户数据
        this.$store.commit('updateUserInfo',res.data)
      });
    },
    // 修改用户邮箱
    updateEmail() {
      this.$refs.editEmailFormRef.validate(async (valid) => {
        if (!valid) return;
        const { data: res } = await this.$http.put("users/", this.editEmailForm);
        // console.log(res)
        if (res.meta.code !== 201) {
          return this.$message.error(res.meta.message);
        }
        this.$message.success(res.meta.message);
        // 隐藏添加提示框
        this.editEmailDialogVisible = false;
        // 重新获取用户数据
        this.$store.commit('updateUserInfo',res.data)
      });
    },
    // 修改用户密码
    updatePassword() {
      this.$refs.editPasswordFormRef.validate(async (valid) => {
        if (!valid) return;
        const { data: res } = await this.$http.put("users/", this.editPasswordForm);
        // console.log(res)
        if (res.meta.code !== 201) {
          return this.$message.error(res.meta.message);
        }
        this.$message.success(res.meta.message);
        // 隐藏添加提示框
        this.editPasswordDialogVisible = false;
        // 重新获取用户数据
        this.$store.commit('updateUserInfo',res.data)
      });
    },
    // 监听修改密码对话框的关闭事件
    editPasswordDialogClosed() {
      this.$refs.editPasswordFormRef.resetFields();
    },
    // 监听修改手机号对话框的关闭事件
    editPhoneDialogClosed() {
      this.$refs.editPhoneFormRef.resetFields();
    },
    // 监听修改邮箱对话框的关闭事件
    editEmailDialogClosed() {
      this.$refs.editEmailFormRef.resetFields();
    },
    // 显示编辑用户的对话框
    async showEditDialog(id) {
      const { data: res } = await this.$http.get("users/" + id);
      if (res.meta.code !== 200) return this.$message.error("获取信息失败");
      this.editForm = res.data;
      this.editDialogVisible = true;
      // console.log(id)
    },
    handleAvatarSuccess(res, file) {
      if (res.meta.code !== 200) {
        return this.$message.error(res.meta.message);
      }
      this.$store.commit("updateUserAvatar", res.data.url);
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("上传头像图片只能是 JPG 格式!");
      }
      if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
      }
      return isJPG && isLt2M;
    },
  },
};
</script>

<style lang="less" scoped>
.ava {
  width: 210px;
  padding: 24px;
  float: left;
  i {
    float: right;
    position: relative;
    right: 10px;
    bottom: 20px;
    font-size: 19px;
  }
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
.info {
  float: right;
  width: 358px;
  margin-top: 35px;
  p {
    font-size: 14px;
    color: #757575;
  }
}
.tishi {
  font-size: 12px;
  color: #757575;
  margin-left: 12px;
}
</style>
