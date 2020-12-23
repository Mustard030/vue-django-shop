import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login'
import Home from '../components/Home'
import Welcome from '../components/Welcome'
import User from '../components/user/User'
import Rights from '../components/power/Rights'
import Main from '../components/shop/Main'
import Cate from '../components/goods/Cate'
import GoodsList from '../components/goods/List'
import Add from '../components/goods/Add'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      path: '/',
      redirect: '/shop'
    },
    {
      path: '/admin',
      redirect: '/login'
    },
    {
      path: '/shop',
      component: Main
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/home',
      component: Home,
      redirect: '/welcome',
      children: [
        {
          path: '/welcome', component: Welcome
        },
        {
          path: '/users', component: User
        },
        {
          path: '/rights', component: Rights
        },
        {
          path: '/categories', component: Cate
        },
        {
          path: '/goods', component: GoodsList
        },
        {
          path: '/goods/add', component: Add
        },
      ]
    }
  ]
})

// 挂载路由导航守卫
router.beforeEach((to, from, next) => {
  // to 将要访问的路径
  // from 从哪个路径跳转
  // next 函数，表示放行
  //  next() 放行 next('/login') 强制跳转到login

  if (to.path === '/login') return next()
  // 获取token
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  next()
})

export default router
