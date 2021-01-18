<template>
    <form 
        id="register-form" 
        class="card"
        @submit.prevent="submit"
    >
        <div class="card-header">
            Register
        </div>

        <div class="card-body">
            <div class="alert alert-danger" v-if="errors.length">
                Please correct the following error(s):
                <ul>
                    <li v-for="error in errors" :key="error">{{error}}</li>
                </ul>
            </div>

            <div class="form-group">
                <label for="email">Email</label><br>
                <input class="form-control" type="email" id="email" v-model="email"/>
            </div>
            <div class="form-group">
                <label for="name">Name</label><br>
                <input class="form-control" type="text" id="name" v-model="name"/>
            </div>
            <div class="form-group">
                <label for="password">Password</label><br>
                <input class="form-control" type="password" id="password" v-model="password"/>
            </div>
            <div class="form-group">
                <label for="repeatPassword">Repeat Password</label><br>
                <input class="form-control" type="password" id="repeatPassword" v-model="repeatPassword"/>
            </div>
            <div class="text-right">
                <button type="submit" class="btn btn-primary">Register</button>
            </div>    
        </div>
    </form>
</template>

<script>
    import { validatePassword } from "./authUtils"

    export default {
        name: "RegisterForm",
        data: function() {
            return {
                errors: [],
                name: "",
                email: "",
                password: "",
                repeatPassword: "",
            }
        },
        methods: {
            submit: function () {
                this.errors = [];
                
                if (!this.name) {
                    this.errors.push("Name required.");
                }
                if (!this.email) {
                    this.errors.push("Email required.");
                }

                const validationErrors = validatePassword(
                    this.password, this.repeatPassword, this.name
                )

                this.errors = this.errors.concat(validationErrors)

                if (!this.errors.length){
                    this.$http.post(
                        "/users/",
                        {
                            name: this.name,
                            email: this.email,
                            password: this.password
                        },
                        {
                            headers: {
                                "Content-Type": "plain/text ",
                            }
                        }
                    ).then(
                        this.$router.push("/")
                    ).catch((error) => {
                        this.errors.push(error.response.data.detail)
                    })
                }
            }
        }
    }
</script>