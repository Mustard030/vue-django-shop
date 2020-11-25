import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'element-ui'
import './plugins/element.js'
import './assets/css/global.css'
import axios from 'axios'

// 配置请求根路径
axios.defaults.baseURL = 'http://localhost:80/api/private/'
Vue.prototype.$http = axios

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
