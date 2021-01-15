<template>
     <div>
        <div class="page-body">
            <register-form />
        </div>
    </div>
</template>

<script lang="ts">
import RegisterForm from "./RegisterForm.vue"

export default {
    name: "RegisterPage",
    components: {
        RegisterForm,
    },
}
</script>