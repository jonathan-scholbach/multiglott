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
import LessonEditPage from "./components/Lesson/LessonEditPage.vue"
import LessonDescriptionPage from "./components/Lesson/LessonDescriptionPage.vue"
import LoginPage from "./components/Auth/LoginPage.vue"
import ProfilePage from "./components/Pages/ProfilePage.vue"
import RegisterPage from "./components/Auth/RegisterPage.vue"
import SuccessfullyRegisteredPage from "./components/Auth/SuccessfullyRegisteredPage.vue"
import SuccessfullyConfirmedPage from "./components/Auth/SuccessfullyConfirmedPage"


const routes = [
  { 
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: process.env.VUE_APP_FRONTEND_CONFIRMED_PATH,
    name: "confirmed",
    component: SuccessfullyConfirmedPage,
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
    path: "/registered", 
    name: "registered",
    component: SuccessfullyRegisteredPage,
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
    path: "/course/:courseSlug/explanation/:lessonSlug",
    name: "lessonDescription",
    props: true,
    component: LessonDescriptionPage
  },
  {
    path: "/lesson/:id",
    name: "editLesson",
    props: true,
    component: LessonEditPage,
  },
  { 
    path: "/logout",
    name: "logout",
  },
]

const router = new VueRouter({
  routes: routes
})

router.mode = 'html5'

export default {
  name: "App",
  router: router,
  head: {
    title () {
      return {
        inner: multiglott
      }
    },
    meta: [
      // creates a meta description tag in header.
      { name: 'description', content: 'My description' }
    ]
  },
  computed: {
    "currentPage": function() {
      switch(this.$route.name) {
        case "confirmed":
          return SuccessfullyConfirmedPage
        case "login":
          return LoginPage
        case "register":
          return RegisterPage
        case "registered":
          return SuccessfullyRegisteredPage
        case "logout":
          this.$store.commit("removeToken")
          return HomePage
        case "profile":
          return ProfilePage
        case "course":
          return CoursePage
        case "lesson":
          return LessonPage
        case "editLesson":
          return LessonEditPage
        case "lessonDescription":
          return LessonDescriptionPage
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