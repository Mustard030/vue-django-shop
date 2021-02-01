import Vue from 'vue'
import VueRouter from 'vue-router'
import AdminLogin from '../components/Login'
import Home from '../components/Home'
import Welcome from '../components/Welcome'
import Users from '../components/user/User'
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
import AllGoodsList from '../components/shop/GoodsList'
import Days from '../components/shop/Days'
import UserLogin from '../components/UserLogin'
import Cart from '../components/shop/Cart'
import CarouselList from '../components/CarouselPics/List'
import Detail from '../components/shop/Detail'
import ItemSearch from '../components/shop/ItemSearch'
import CookbookSearch from '../components/shop/CookbookSearch'
import Portal from '../components/shop/UserPortal'
import Mycookbook from '../components/shop/Mycookbook'
import MyOrder from '../components/shop/MyOrder'
import MyAddress from '../components/shop/MyAddress'
import User from '../components/shop/User'
import Checkout from '../components/shop/Checkout'
import Pay from '../components/shop/Pay'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [{
      path: '/',
      component: Main,
      redirect: '/days',
      children: [{
          path: '/days',
          component: Days,
        },
        {
          path: '/category/list',
          component: AllGoodsList,
        },
        {
          path: '/buy/detail',
          component: Detail
        },
        {
          path: '/search/item',
          component: ItemSearch,
        },
        {
          path: '/search/cookbook',
          component: CookbookSearch,
        },
        {
          path: '/buy/cart',
          component: Cart,
        },
        {
          path:'/buy/checkout',
          component:Checkout,
        },
        {
          path:'/order/payment',
          component:Pay,
        },
        {
          path: '/user',
          component: User,
          redirect: '/user/portal',
          children: [{
              path: "/user/portal",
              component: Portal,
            },
            {
              path: '/user/cookbook',
              component: Mycookbook,
            },
            {
              path: '/user/order',
              component: MyOrder,
            },
            {
              path: '/user/address',
              component: MyAddress,
            },
          ]
        },

      ]
    },
    {
      path: '/login',
      component: UserLogin,
    },
    {
      path: '/admin',
      redirect: '/adminlogin'
    },
    {
      path: '/adminlogin',
      component: AdminLogin
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
          component: Users
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
        {
          path: '/carouselList',
          component: CarouselList
        }
      ]
    }
  ]
})
import {
  Notification
} from 'element-ui'

// 挂载路由导航守卫
router.beforeEach((to, from, next) => {
  // to 将要访问的路径
  // from 从哪个路径跳转
  // next 函数，表示放行
  //  next() 放行 next('/login') 强制跳转到login

  if (to.path === '/adminlogin' || to.path === '/') {
    return next()
  }
  // 获取token
  const requireAdmin = ['/categories', '/goods', '/users', '/delivery',
    '/merchant', '/order', '/cookbook', '/welcome',
    '/carouselList'
  ]
  const requireLogin = ['/user/portal', '/user', '/user/cookbook',
    '/user/address', '/user/order', '/buy/detail', '/cookbook/detail',
    '/buy/checkout'
  ]
  const tokenStr = window.sessionStorage.getItem('token')
  // 管理员页面登陆验证
  if (requireAdmin.indexOf(to.path) !== -1 &&
    (!tokenStr || !JSON.parse(window.localStorage.getItem('vuex-along')).root.userInfo.is_superuser)
  ) {
    return next('/adminlogin')
  }
  // 商品界面登陆验证并跳转
  if (requireLogin.indexOf(to.path) !== -1 && !tokenStr) {
    window.sessionStorage.setItem('frompath',from.path)
    Notification.error({
      title: '错误',
      message: '请先登录'
    });
    return next('/login')
  }
  next()
})

export default router
