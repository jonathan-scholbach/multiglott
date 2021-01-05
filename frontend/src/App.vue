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

import "jquery/src/jquery.js";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import "./assets/styles/style.scss";


import CoursePage from "./components/CoursePage.vue"
import CreateCoursePage from "./components/CreateCoursePage.vue"
import HeaderNav from "./components/HeaderNav.vue"
import HomePage from "./components/HomePage.vue"
import LoginPage from "./components/LoginPage.vue"
import ProfilePage from "./components/ProfilePage.vue"
import RegisterPage from "./components/RegisterPage.vue"


const routes = [
  { 
    path: "/",
    name: "home",
    component: HomePage 
  },
  {
    path: "/login", 
    name: "login",
    component: LoginPage },
  { 
    path: "/register", 
    name: "register",
    component: RegisterPage },
  { 
    path: "/profile", 
    name: "profile",
    component: ProfilePage},
  { 
    path: "/create-course", 
    name: "createCourse",
    component: CreateCoursePage },
  { 
    path: "/course/:id", 
    name: "course",
    component: CoursePage
  },
  { 
    path: "/logout",
    name: "logout"
  },
]

const router = new VueRouter({
  routes: routes
})

export default {
  name: "App",
  router: router,
  computed: {
    "currentPage": function() {
      console.log(this.$route)
      switch(this.$route.name) {
        case "login":
          return LoginPage
        case "register":
          return RegisterPage
        case "logout":
          this.$store.commit("removeUser")
          return HomePage
        case "profile":
          return ProfilePage
        case "course":
          return CoursePage
        case "createCourse":
          return CreateCoursePage
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