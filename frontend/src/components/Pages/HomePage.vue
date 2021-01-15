<template>
    <div class="page-body">
        <div 
            class="material-card" 
            v-for="course in courses" :key="course.id"
        >
            <div class="material-card-content">
                <div class="material-card-title">
                    <router-link :to="{name: 'course', params: {'slug': course.slug}}">{{course.title}}</router-link>
                    [{{course.source_language}} → {{course.target_language}}]
                </div>
            </div>
        </div>
    </div>     
</template>

<script lang="ts">
export default {
    name: "HomePage",
    data: function() {
        return {
            courses: [],
        }
    },
    methods: {
        getCourses: async function() {
            var self = this
            await this.$http.get("/courses").then(
                (response) => {
                    self.courses = response.data
                }
            ).catch(
                (error) => {
                    console.log(error)
                }
            )
        }
    },
    mounted: function() {
        this.getCourses()
    }

}
</script>