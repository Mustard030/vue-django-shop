<template>
  <div>
    <el-cascader
      :options="cityOptions"
      v-model="city"
      :props="cityProps"
      @change="changeProvince"
      clearable
    >
    </el-cascader>

    <el-dropdown>
      <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>黄金糕</el-dropdown-item>
        <el-dropdown-item divided>狮子头</el-dropdown-item>
        <el-dropdown-item divided>螺蛳粉</el-dropdown-item>
        <el-dropdown-item divided>蚵仔煎</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
import cityOptions from '../assets/js/citydata'
export default {
  data() {
    return {
      city: [],
      cityOptions,
      cityProps: {
        expandTrigger: 'hover'
      }
    }
  },
  methods: {
    changeProvince() {
      console.log(this.city)
    }
  }
}
</script>

<style lang="less" scoped>
 .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
</style>
