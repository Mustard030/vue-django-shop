import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'element-ui'
import './plugins/element.js'
import './assets/css/global.css'
import axios from 'axios'
import TreeTable from 'vue-table-with-tree-grid'
// 富文本编辑器
import VueQuillEditor from 'vue-quill-editor'
import { Quill } from 'vue-quill-editor'
import { ImageDrop } from 'quill-image-drop-module'
import ImageResize from 'quill-image-resize-module'

// require styles 引入样式
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

// NProgress
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// cookies全局方法
import { setCookie, getCookie, delCookie } from './assets/js/cookie'
Quill.register('modules/imageDrop', ImageDrop)
Quill.register('modules/imageResize', ImageResize)
Vue.prototype.$cookieStore = {
  setCookie,
  getCookie,
  delCookie
}

Vue.use(VueQuillEditor)

Vue.component('tree-table', TreeTable)

// 配置请求根路径
axios.defaults.baseURL = 'http://localhost:80/api/private/'
// 在request拦截器中展示进度条
axios.interceptors.request.use(config => {
  NProgress.start()
  // config.headers.Authorization = window.sessionStorage.getItem('token')
  config.headers.Authorization = JSON.parse(window.localStorage.getItem('vuex-along')).root.userInfo.token
  // console.log(config.headers.Authorization)
  return config
})
// 在response拦截器中隐藏进度条
axios.interceptors.response.use(config => {
  NProgress.done()
  return config
})
Vue.prototype.$http = axios

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
