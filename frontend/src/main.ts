import Vue from "vue"
import Vuex from "vuex"
import VueRouter from "vue-router"
import BootstrapVue from "bootstrap-vue"

import axios from "axios"
import AxiosInstance from "axios"

import App from "./App.vue"
import apiSetup from "./middleware/axios"

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(BootstrapVue)


const privileges = {
  "CAN_READ": "CAN_READ",
  "CAN_EDIT": "CAN_EDIT",
  "CAN_DELETE": "CAN_DELETE",
}

Vue.prototype.$privileges = privileges


const store = new Vuex.Store({
  state: {
    token: null,
  },
  getters: {
    token: state => {
      return state.token
    },
    loggedIn: state => {
      return Boolean(state.token)
    }
  },
  mutations: {
    initialiseStore(state) {
      if(localStorage.getItem("store")) {
        this.replaceState(
          Object.assign(state, JSON.parse(localStorage.getItem("store")))
        );
      }
      this.subscribe((mutation, state) => {
        localStorage.setItem("store", JSON.stringify(state))
      });
    },
    setToken (state, token) {
      state.token = token
    },
    removeToken (state) {
      state.token = null
    }
  }
})

var API_URL = (
  "http://" 
  + process.env.VUE_APP_API_DOMAIN 
  + ":" + process.env.VUE_APP_API_PORT 
  + "/" + process.env.VUE_APP_API_VERSION
)

export const axiosInstance = axios.create({
  baseURL: API_URL
})

apiSetup(store, axiosInstance)
Vue.prototype.$http = axiosInstance


new Vue({
  render: h => h(App),
  store: store,
  beforeCreate() {
		this.$store.commit("initialiseStore");
	}
}).$mount("#app")
