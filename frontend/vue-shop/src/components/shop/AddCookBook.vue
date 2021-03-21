<template>
  <div>
    <!-- 卡片视图区域 -->
    <el-card>
      <!-- 添加文章提示信息 -->
      <el-alert
        title="添加文章"
        type="info"
        :closable="false"
        center
        show-icon
      ></el-alert>

      <!-- 表单区域 -->
      <el-form
        :model="addEssayForm"
        :rules="addEssayRules"
        ref="addEssayFormRef"
        label-width="100px"
        label-position="top"
      >
        <el-form-item label="菜谱标题" prop="title">
          <el-input v-model="addEssayForm.title" width="300px"></el-input>
        </el-form-item>
        <!-- <el-form-item label="作者" prop="author">
          <el-select
            v-model="addEssayForm.author"
            filterable
            clearable
            placeholder="请选择"
          >
            <el-option
              v-for="user in userList"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            ></el-option>
          </el-select>
        </el-form-item> -->
        <el-form-item label="正文" prop="content">
          <!-- 富文本编辑器组件 -->
          <quill-editor
            v-model="addEssayForm.content"
            :options="editorOption"
          ></quill-editor>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="submitForm" icon="el-icon-edit">保存并添加</el-button>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 富文本编辑器选项
      editorOption: {
        placeholder: '开始编辑吧',
        modules: {
          toolbar: [
            ['bold', 'italic', 'underline', 'strike'], // toggled buttons
            ['blockquote', 'code-block'],

            [{ header: 1 }, { header: 2 }], // custom button values
            [{ list: 'ordered' }, { list: 'bullet' }],
            [{ script: 'sub' }, { script: 'super' }], // superscript/subscript
            [{ indent: '-1' }, { indent: '+1' }], // outdent/indent
            [{ direction: 'rtl' }], // text direction

            [{ size: ['small', false, 'large', 'huge'] }], // custom dropdown
            [{ header: [1, 2, 3, 4, 5, 6, false] }],

            [{ color: [] }, { background: [] }], // dropdown with defaults from theme
            [{ font: [] }],
            [{ align: [] }],

            ['clean'], // remove formatting button
            ['link', 'image', 'video']
          ],
          // 调整图片大小
          imageResize: {
            displayStyles: {
              backgroundColor: 'black',
              border: 'none',
              color: 'white'
            },
            modules: ['Resize', 'DisplaySize', 'Toolbar']
          }
        }
      },
      // 添加文章表单
      addEssayForm: {
        title: '',
        author: this.$store.state.userInfo.userId,
        content: ''
      },
      // 作者选项
      userList: [],
      // 表单规则
      addEssayRules: {
        title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
        author: [{ required: true, message: '请选择作者', trigger: 'blur' }],
        content: [{ required: true, message: '请输入正文', trigger: 'blur' }]
      }
    }
  },
  created() {
    // this.getUserList();
  },
  methods: {
    // 添加文章
    async submitForm() {
    //   console.log(this.addEssayForm);
      this.$refs.addEssayFormRef.validate(async (valid) => {
        if (!valid) {
          return this.$message.error('请填写必要的表单项')
        } else {
          // 执行添加
          const { data: res } = await this.$http.post('cookbooks/', this.addEssayForm)
          if (res.meta.code !== 200) {
            return this.$message.error(res.meta.message)
          }
          this.$message.success(res.meta.message)
          this.$router.push('/user/cookbook')
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.el-form{
    margin-top: 15px;
}
.el-button{
    float: right;
    margin-top: 15px;
    margin-bottom: 15px;
    right: 35px;
}
</style>
