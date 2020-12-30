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
                <input class="form-control" type="email" id="email" v-model="email"/>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label><br>
                <input class="form-control" type="password" id="password" v-model="password"/>
            </div>

            <button type="submit" class="btn btn-primary">Login</button>
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
                     this.$http.post(
                        "http://localhost:8000/v1/users/login",
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
                    ).then((response) => {
                        if (response.status == 200) {
                            this.$store.commit(
                                "setUser", 
                                {
                                    name: response.data["name"],
                                    authToken: response.data["auth_token"]
                                }
                            )
                            this.$router.push('/')
                            
                        }
                    }).catch((error) => {
                        this.$store.commit("removeUser")
                        this.error = error.response.data["detail"]
                    })
                }
            }
        }
    }
</script>