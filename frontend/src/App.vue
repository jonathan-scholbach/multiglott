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


import CoursePage from "./components/Course/CoursePage.vue"
import CreateCoursePage from "./components/Course/CreateCoursePage.vue"
import HeaderNav from "./components/Pages/HeaderNav.vue"
import HomePage from "./components/Pages/HomePage.vue"
import LessonPage from "./components/Lesson/LessonPage.vue"
import LoginPage from "./components/Pages/LoginPage.vue"
import ProfilePage from "./components/Pages/ProfilePage.vue"
import RegisterPage from "./components/Pages/RegisterPage.vue"


const routes = [
  { 
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/login", 
    name: "login",
    component: LoginPage,
  },
  { 
    path: "/register", 
    name: "register",
    component: RegisterPage,
  },
  { 
    path: "/profile", 
    name: "profile",
    component: ProfilePage},
  { 
    path: "/create-course", 
    name: "createCourse",
    component: CreateCoursePage },
  { 
    path: "/course/:slug", 
    name: "course",
    props: true,
    component: CoursePage,
  },
  {
    path: "/course/:courseSlug/lesson/:lessonSlug",
    name: "lesson",
    component: LessonPage,
  },
  { 
    path: "/logout",
    name: "logout",
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
      switch(this.$route.name) {
        case "login":
          return LoginPage
        case "register":
          return RegisterPage
        case "logout":
          this.$store.commit("removeToken")
          return HomePage
        case "profile":
          return ProfilePage
        case "course":
          return CoursePage
        case "lesson":
          return LessonPage
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