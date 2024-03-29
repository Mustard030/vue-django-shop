import Vue from 'vue'
import Vuex from 'vuex'
import createVuexAlong from 'vuex-along'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    BACKEND_URL: 'http://localhost',
    userInfo: {
      userId: null,
      avatar: null,
      username: null,
      token: null,
      is_superuser: false
    },
    itemInCart: [],
    searchResult: []
  },
  mutations: {
    // 用于变更state数据
    updateUserInfo(state, userObj) {
      state.userInfo.userId = userObj.id
      state.userInfo.avatar = userObj.avatar
      state.userInfo.username = userObj.username
      state.userInfo.token = userObj.token
      state.userInfo.phone = userObj.phone
      state.userInfo.email = userObj.email
      state.userInfo.is_superuser = userObj.is_superuser
    },
    clearLocalStorage(state) {
      state.userInfo = {}
    },
    // 更新购物车数据
    updateCart(state, cartList) {
      state.itemInCart = cartList
    },
    // 更新用户头像
    updateUserAvatar(state, avatarUrl) {
      state.userInfo.avatar = avatarUrl
    },
    // 更新搜索数据
    updateSearchResult(state, results) {
      state.searchResult = results
    }
  },
  actions: {},
  modules: {},
  plugins: [createVuexAlong()]
})
