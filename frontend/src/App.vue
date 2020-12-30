<template>
  <div id="app">
    <div class="page">
      <div class="header">
        <HeaderNav/>
      </div>

     <div class="page-content">
        <component v-bind:is="currentPage"></component>
      </div>
 
    </div>
  </div>
</template>

<script>
import VueRouter from "vue-router"

import HeaderNav from "./components/HeaderNav.vue"
import HomePage from "./components/HomePage.vue"
import LoginPage from "./components/LoginPage.vue"
import RegisterPage from "./components/RegisterPage.vue"

import "jquery/src/jquery.js";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "./assets/styles/style.scss";



const routes = [
  { path: "/", component: HomePage },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
  { path: "/logout"}
]

const router = new VueRouter({
  routes: routes
})

export default {
  name: "App",
  router: router,
  computed: {
    "currentPage": function() {
      switch(this.$route.fullPath) {
        case "/login":
          return LoginPage
        case "/register":
          return RegisterPage
        case "/logout":
          this.$store.commit("removeUser")
          return HomePage
        default:
          return HomePage
      }
    },
  },
  components: {
    HeaderNav
  },
}
</script>