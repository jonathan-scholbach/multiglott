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
                this.errors = [];
                

                if (!this.errors.length){
                    var username = this.email

                    var params = new URLSearchParams()
                    params.append("username", username)
                    params.append("password", this.password)

                     this.$http.post(
                        "http://localhost:8000/v1/auth/token",
                        params,
                        {
                            headers : {
                                "Content-Type": "application/x-www-form-urlencoded"
                            }
                        }
                    ).then((response) => {
                        if (response.status == 200) {
                            let token = response.data.access_token
                            this.$store.commit(
                                "setUser", 
                                {
                                    name: username,
                                    authToken: token
                                }
                            )
                            this.$router.push('/')
                        }
                    })
                }
            }
        }
    }
</script>