import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login'
import Home from '../components/Home'
import Welcome from '../components/Welcome'
import User from '../components/user/User'
import Delivery from '../components/user/Delivery'
import Rights from '../components/power/Rights'
import Main from '../components/shop/Main'
import Cate from '../components/goods/Cate'
import GoodsList from '../components/goods/List'
import GoodAdd from '../components/goods/Add'
import GoodEdit from '../components/goods/Edit'
import MerchantList from '../components/merchant/List'
import Order from '../components/order/Order'
import Cookbook from '../components/cookbook/Cookbook'
import CookbookEdit from '../components/cookbook/Edit'
import CookbookAdd from '../components/cookbook/Add'


Vue.use(VueRouter)

const router = new VueRouter({
  routes: [{
      path: '/',
      component: Main
    },
    {
      path: '/admin',
      redirect: '/login'
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/home',
      component: Home,
      redirect: '/welcome',
      children: [{
          path: '/welcome',
          component: Welcome
        },
        {
          path: '/users',
          component: User
        },
        {
          path: '/rights',
          component: Rights
        },
        {
          path: '/categories',
          component: Cate
        },
        {
          path: '/goods',
          component: GoodsList
        },
        {
          path: '/goods/add',
          component: GoodAdd
        },
        {
          path: '/goods/edit',
          component: GoodEdit
        },
        {
          path: '/order',
          component: Order
        },
        {
          path: '/delivery',
          component: Delivery
        },
        {
          path: '/merchant',
          component: MerchantList
        },
        {
          path: '/cookbook',
          component: Cookbook
        },
        {
          path: '/cookbook/add',
          component: CookbookAdd
        },
        {
          path: '/cookbook/edit',
          component: CookbookEdit
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

  if (to.path === '/login' || to.path === '/') {return next()}
  // 获取token
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr){ return next('/login')}
  next()
})

export default router
