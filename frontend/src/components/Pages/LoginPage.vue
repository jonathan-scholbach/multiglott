<template>
    <div>
       <div class="page-body">
            <login-form />
        </div>
    </div>
</template>

<script lang="ts">
import LoginForm from "./LoginForm.vue"

export default {
    name: "LoginPage",
    components: {
        LoginForm
    }
}
</script>