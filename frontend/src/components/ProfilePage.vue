<template>
    <div>
        <div class="page-body">
            <div class="page-title">Profile: <strong>{{this.user.name}}</strong></div>
            <h1>Courses</h1>
            <div 
                class="material-card" 
                v-for="course in this.courses" :key="course.created_at"
            >
                <div class="material-card-title">
                    <router-link :to="{name: 'course', params: {'id': course.id}}">{{course.title}}</router-link>
                    [{{course.source_language.name}} → {{course.target_language.name}}]
                </div>
                <div class="material-card-body">
                    
                </div>
            </div>
                

        </div>
    </div>
</template>

<script>
export default {
    name: "ProfilePage",
    data: function() {
        return {
            "user": {},
            "courses": [],
        }
    },
    mounted: function () {
      this.getUser()
      this.getCourses()
    },
    methods: {
        "getUser": function() {
            var self = this
            this.$http.get(
                "http://localhost:8000/v1/me"
            ).then((response) => {
                if (response.status == 200) {
                    self.user = response.data
                }
            }).catch((error) => {
                console.log("error")
                console.log(error.response.data.detail)
            })
        },
        "getCourses": function() {
            var self = this
            this.$http.get("http://localhost:8000/v1/me/courses").then(
                (response) => {
                    if (response.status == 200) {
                        self.courses = response.data
                    }
                }
            )
        }
    }
}
</script>