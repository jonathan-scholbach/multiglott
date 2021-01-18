<template>
    <div>
       <div class="page-body">
            <login-form />
        </div>
    </div>
</template>

<script>
import LoginForm from "./LoginForm.vue"

export default {
    name: "LoginPage",
    components: {
        LoginForm
    }
}
</script>