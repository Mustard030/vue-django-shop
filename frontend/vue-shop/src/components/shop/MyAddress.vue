<template>
  <div>
    <el-card>
      <div slot="header">
        <span>收货地址</span>
      </div>
      <div v-for="o in 4" :key="o" class="text item">
        {{ "列表内容 " + o }}
      </div>
    </el-card>
  </div>
</template>

<script>
export default {};
</script>

<style lang="less" scoped>
.el-card__header{
  box-shadow: 0 1 1 rgba(0, 0, 0, 0.15) !important;
}
</style>
