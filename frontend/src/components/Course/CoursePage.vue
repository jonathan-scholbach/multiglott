<template>
    <div> 
        <div class="page-body">
            <div class="title">{{course.title}}</div>
        </div>
        <div 
            class="material-card"
            v-for="lesson in this.course.lessons" :key="lesson.title"
        >
            <router-link :to="{
                name: 'lesson',
                params: {
                    courseSlug: course.slug,
                    lessonSlug: lesson.slug
                }
            }">{{lesson.title}}</router-link>
            <span v-if="$store.getters.loggedIn" style="float:right">78 %</span>
        </div> 

        <div class="text-right">
        <b-button 
            v-if="this.allowEdit" 
            v-b-toggle.add-lesson variant="primary"
        >
            Add Lesson
        </b-button>
        </div>
        <b-collapse id="add-lesson">
            <div v-if="this.allowEdit" class="material-card">
                <upload-file-form 
                    url='/lessons/'
                    buttonCaption="Add New Lesson"
                    v-bind:additionalData="{
                        course_id: course.id
                    }"
                ></upload-file-form>
                    
            </div>
        </b-collapse>    
    </div>
</template>

<script>
import UploadFileForm from '../UploadFileForm.vue'
import Course from "../../models/Course.ts"



export default {
  components: { UploadFileForm },
    name: "CoursePage",
    data: function() {
        return {
            course: Course,
            user: {},
        }
    },
    mounted: function() {
        this.getCourse()
        this.getUser()
    },
    methods: {
        getUser: function() {
            var self = this
            this.$http.get(
                "/me"
            ).then((response) => {
                self.user = response.data
            }).catch((error) => {
                console.log(error)
            })
        },
        getCourse: function() {
            this.course.slug = this.$route.params.slug,
            this.course.find()
        },
    },
    computed: {
        allowEdit: function() {
            try{
                return this.course.author_id == this.user.id
            }
            catch{
                return false
            }
        }
    }
}
</script>