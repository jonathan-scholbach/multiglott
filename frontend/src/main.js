import Vue from "vue"
import VueRouter from "vue-router"
import axios from "axios" 

import App from "./App.vue"

import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"

require("@/assets/styles/style.scss")


Vue.config.productionTip = false
Vue.prototype.$http = axios

Vue.use(VueRouter)

new Vue({
  render: h => h(App),
}).$mount("#app")
