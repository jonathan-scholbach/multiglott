<template>
    <div class="material-card">
        You have successfully confirmed your email! You can now 
        <router-link 
            :to="{
                name: 'login',
            }"
            >Login</router-link>
    </div>
</template>