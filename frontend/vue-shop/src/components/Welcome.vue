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

<style></style>
