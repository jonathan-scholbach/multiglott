<template>
    <form 
        id="login-form"
        class="card"
        @submit.prevent="login"
    >
        <div class="card-header">
            Login
        </div>

        <div class="card-body">
           <div v-if="error" class="alert alert-danger">
                {{ error }}
            </div>
            <div class="form-group">
                <label for="email">Email</label><br>
                <input 
                    class="form-control" 
                    type="email" 
                    id="email" 
                    v-model="email"
                />
            </div>
            
            <div class="form-group">
                <label for="password">Password</label><br>
                <input class="form-control" type="password" id="password" v-model="password"/>
            </div>
            <div class="text-right">
                <button type="submit" class="btn btn-primary">Login</button>
            </div>    
        </div>
    </form>
</template>

<script>
    export default {
        name: "LoginForm",
        data: function() {
            return {
                error: null,
                name: "",
                email: "",
                password: "",
            }
        },
        methods: {
            login: function () {
                let username = this.email

                let params = new URLSearchParams()
                params.append("username", username)
                params.append("password", this.password)

                this.$http.post(
                    "/auth/token",
                    params,
                    {
                        headers : {
                            "Content-Type": "application/x-www-form-urlencoded"
                        }
                    }
                ).then((response) => {
                    let token = response.data.access_token
                    this.$store.commit(
                        "setToken", 
                        token
                    )
                    this.$router.push('/')
                }).catch((err) => {
                    this.$store.commit("removeToken")
                    this.error = err.response.data.detail
                })
            }
        }
    }
</script>