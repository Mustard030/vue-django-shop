<template>
  <div>
    <el-button type="danger" @click="logout">退出 </el-button>
  </div>
</template>
<script>
export default {
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>
<style lang="less" scoped>
</style>
