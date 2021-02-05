<template>
  <div class="login_container">
    <div class="login_box">
      <!-- 头像区域 -->
      <div class="avatar_box">
        <img src="../assets/logo.png" />
      </div>
      <!-- 登陆表单 -->
      <el-form
        class="register_form"
        :model="RegisterForm"
        :rules="RegisterFormRules"
        ref="RegisterFormRef"
      >
        <!-- 用户名 -->
        <el-form-item prop="username">
          <el-input
            prefix-icon="el-icon-user"
            v-model="RegisterForm.username"
            placeholder="用户名"
          ></el-input>
        </el-form-item>
        <!-- 密码 -->
        <el-form-item prop="password">
          <el-input
            prefix-icon="el-icon-key"
            v-model="RegisterForm.password"
            type="password"
            placeholder="密码"
            show-password
          ></el-input>
        </el-form-item>
        <!-- 手机号 -->
        <el-form-item prop="phone">
          <el-input
            prefix-icon="el-icon-phone"
            v-model="RegisterForm.phone"
            placeholder="手机号"
          ></el-input>
        </el-form-item>
        <!-- 邮箱 -->
        <el-form-item prop="email">
          <el-input
            prefix-icon="el-icon-message"
            v-model="RegisterForm.email"
            placeholder="邮箱"
          ></el-input>
        </el-form-item>
        <!-- 按钮 -->
        <el-form-item class="btns">
          <el-button type="primary" @click="register">注册</el-button>
          <el-button type="info" @click="clearForm">清空</el-button>
        </el-form-item>
      </el-form>
    </div>
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

    return {
      // 登陆表单的数据绑定对象
      RegisterForm: {
        username: "",
        password: "",
        phone: "",
        email: "",
        mg_state: 1,
      },
      // 添加用户表单验证规则对象
      RegisterFormRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          {
            min: 3,
            max: 10,
            message: "长度在 3 到 10 个字符之间",
            trigger: ["blur", "change"],
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
            trigger: ["blur", "change"],
          },
        ],
        phone: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          {
            min: 11,
            max: 11,
            message: "请输入正确格式的手机号码",
            trigger: ["blur", "change"],
          },
        ],
        email: [{ required: true, message: "请输入邮箱", trigger: "blur" }],
      },
    };
  },
  methods: {
    // 重置登陆表单
    clearForm: function () {
      this.$refs.RegisterFormRef.resetFields();
    },
    //3秒后进入跳转页面
    threeGo() {
      const TIME_COUNT = 2;
      if (!this.timer) {
        this.count = TIME_COUNT;
        this.show = false;
        this.timer = setInterval(() => {
          if (this.count > 0 && this.count <= TIME_COUNT) {
            this.count--;
          } else {
            this.show = true;
            clearInterval(this.timer);
            this.timer = null;
            //跳转的页面写在此处
            this.$router.push({
              path: "/",
            });
          }
        }, 1000);
      }
    },
    register: function () {
      this.$refs.RegisterFormRef.validate((valid) => {
        // 登陆请求
        if (!valid) return;
        this.$http
          .post("users/", this.RegisterForm)
          .then((res) => {
            if (res.data.meta.code !== 201) {
              return this.$message.error(res.data.meta.message);
            }
            // console.log(res.data.data)
            window.sessionStorage.setItem("token", res.data.data.token);
            window.sessionStorage.setItem("user", res.data.data.username);
            this.$store.commit("updateUserInfo", res.data.data);
            this.$cookieStore.setCookie("username", this.RegisterForm.username, 86400);
            this.$notify({
              title: "成功",
              message: "注册成功,2秒后跳转至首页",
              type: "success",
            });
            this.threeGo();
          })
          .catch((err) => {
            // console.log(err);
            return this.$message.error("连接服务器失败");
          });
      });
    },
  },
};
</script>

<style lang="less" scoped>
.login_container {
  // background-color: #2b4b6b;
  background: url("http://localhost:80/media/resources/bg.png");
  height: 100%;
}

.login_box {
  width: 450px;
  height: 430px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);

  .avatar_box {
    height: 130px;
    width: 130px;
    border: 1px solid #eee;
    border-radius: 50%;
    padding: 10px;
    box-shadow: 0 0 10px #ddd;
    position: absolute;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;

    img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-color: #eee;
    }
  }
}

.btns {
  display: flex;
  justify-content: flex-end;
}

.register_form {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0 30px;
  box-sizing: border-box;
}
</style>
