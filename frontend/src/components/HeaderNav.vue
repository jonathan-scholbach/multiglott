<template>
   <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item">
                    <router-link to="/" class="nav-link active">Home</router-link>
                </li>
            </ul>
            <ul class="navbar-nav">
                <li v-if="!this.$store.getters.loggedIn" class="nav-item">
                    <router-link to="/login" class="nav-link active">Login</router-link>
                </li>
                <li v-if="!this.$store.getters.loggedIn" class="nav-item">
                    <router-link to="/register" class="nav-link active">Register</router-link>
                </li>
                <li v-if="this.$store.getters.loggedIn" class="nav-item">
                    <router-link to="/logout" class="nav-link active">Logout <span class="username">{{ this.$store.getters.user.name }}</span></router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>