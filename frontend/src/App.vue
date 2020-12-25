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
import WelcomePage from "./components/WelcomePage.vue"
import LoginPage from "./components/LoginPage.vue"
import RegisterPage from "./components/RegisterPage.vue"

const routes = [
  { path: "/", component: WelcomePage },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
]

const router = new VueRouter({
  routes: routes
})

export default {
  name: "App",
  computed: {
    "currentPage": function() {
      switch(this.$route.fullPath) {
        case "/login":
          return LoginPage
        case "/register":
          return RegisterPage
        default:
          return WelcomePage
      }
    }
  },
  components: {
    HeaderNav
  },
  router: router
}
</script>

<style>
  @import "/bootstrap/dist/css/bootstrap.min.css";
  @import "/bootstrap/dist/js/bootstrap.min.js";
  @import "/jquery/src/jquery.js";
  @import "/assets/styles/style.scss";
</style>