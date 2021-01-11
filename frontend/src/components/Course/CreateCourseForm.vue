<template>
    <form 
        id="create-course-form" 
        class="card"
        @submit.prevent="submit"
    >
        <div class="card-header">
            Create New Course
        </div>

        <div class="card-body">
            <div class="alert alert-danger" v-if="errors.length">
                Please correct the following error(s):
                <ul>
                    <li v-for="error in errors" :key="error">{{error}}</li>
                </ul>
            </div>

            <div class="form-group">
                <label for="title">Title</label><br>
                <input class="form-control" type="title" id="title" v-model="title"/>
            </div>
            <div class="form-group">
                <label for="title">Source Language</label><br>
                <input class="form-control" type="sourceLanguage" id="sourceLanguage" v-model="sourceLanguage"/>
            </div>
            <div class="form-group">
                <label for="title">Target Language</label><br>
                <input class="form-control" type="targetLanguage" id="targetLanguage" v-model="targetLanguage"/>
            </div>
            <div class="text-right">
                <button type="submit" class="btn btn-primary">Create</button>
            </div>    
        </div>
    </form>
</template>

<script>    
    export default {
        name: "CreateCourseForm",
        data: function() {
            return {
                errors: [],
                title: "",
                targetLanguage: "",
                sourceLanguage: "",
            }
        },
        methods: {
            submit: function () {
                console.log(this.$store.state.user.authToken)
                this.errors = [];
                if (!this.title) {
                    this.errors.push("Title is required.");
                }
                
                if (!this.errors.length){
                    this.$http.post(
                        "/courses/",
                        {
                            title: this.title,
                            target_language: this.targetLanguage,
                            source_language: this.sourceLanguage
                        },
                    ).catch((error) => {
                        this.errors.push(error.response.data.detail)
                    })
                }
            }
        }
    }
</script>