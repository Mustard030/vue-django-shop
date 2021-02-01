<template>
  <div>
    <el-card>
      <div slot="header">
        <span style="font-size:20px;">我的菜谱</span>
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

<style></style>
