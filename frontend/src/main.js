import Vue from "vue"
import Vuex from "vuex"
import VueRouter from "vue-router"
import BootstrapVue from "bootstrap-vue"

import axios from "axios"

import App from "./App.vue"

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(BootstrapVue)

Vue.prototype.$http = axios


const store = new Vuex.Store({
  state: {
    user: null,
  },
  getters: {
    user: state => {
      return state.user
    },

    authToken: state => {
      if (state.user !== null){
          if (state.user.authToken) {
            return state.user.authToken
          }
      }
      return null
    },

    loggedIn: state => {
      if (state.user != null){
        if (state.user.authToken != null) {
          return true;
        }
      }
      return false;
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
    setUser (state, user) {
      state.user = user
    },
    removeUser (state) {
      state.user = null
    }
  }
})


new Vue({
  render: h => h(App),
  store: store,
  beforeCreate() {
		this.$store.commit("initialiseStore");
	}
}).$mount("#app")
