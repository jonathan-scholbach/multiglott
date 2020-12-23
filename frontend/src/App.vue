<template>
  <div id="app">
    <div class="page">
      <div class="header">
        <HeaderNav/>
      </div>
      <div id="page-content">
        <component v-bind:is="page"></component>
      </div> 
    </div>
  </div>
</template>

<script>
import HeaderNav from "./components/HeaderNav.vue"
import WelcomePage from "./components/WelcomePage.vue"
import LoginPage from "./components/LoginPage.vue"

export default {
  name: "App",
  data: function() {
    return {
      page: "WelcomePage"
    }
  },
  components: {
    HeaderNav,
    WelcomePage,
    LoginPage
  }
}
</script>

<style>
  @import "/assets/styles/style.sass";
</style>