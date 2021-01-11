<template>
   <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item">
                    <router-link to="/" class="nav-link active">Courses</router-link>
                </li>
                 <li v-if="this.$store.getters.loggedIn" class="nav-item">
                    <router-link to="/profile" class="nav-link active">Profile</router-link>
                </li>
            </ul>
            <ul v-if="!this.$store.getters.loggedIn" class="navbar-nav">
                <li class="nav-item">
                    <router-link to="/login" class="btn btn-outline-primary nav-link active">Login</router-link>
                </li>
                <li class="nav-item">
                    <router-link to="/register" class="btn btn-primary nav-link active">Register</router-link>
                </li>
            </ul>

            <ul v-if="this.$store.getters.loggedIn" class="navbar-nav">
                <li class="nav-item">
                    <router-link to="/create-course" class="btn btn-outline-primary nav-link active">Create Course</router-link>
                </li>
                <li class="nav-item">
                    <router-link to="/logout" class="nav-link active">Logout</router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>