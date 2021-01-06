import Vue from 'vue'
import Vuex from 'vuex'
import createVuexAlong from 'vuex-along'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    BACKEND_URL:'http://localhost',
    userInfo: {
      userId: null,
      avatar: null,
      username: null,
      token:null
    },

  },
  mutations: {
    //用于变更state数据
    updateUserInfo(state,userObj){
      state.userInfo.userId = userObj.id
      state.userInfo.avatar = userObj.avatar
      state.userInfo.username = userObj.username
      state.userInfo.token = userObj.token
    }
  },
  actions: {},
  modules: {},
  plugins: [createVuexAlong()]
})
