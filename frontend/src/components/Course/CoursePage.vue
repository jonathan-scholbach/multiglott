<template>
    <div
        v-if="this.course" 
        class="page-body container"
    >    
        <div class="material-card title-card">
            <div class="material-card-content">
                {{ course.title }}
            </div>
        </div>
        
        <lesson-card
            v-for="lesson in this.course.lessons" :key="lesson.title"
            v-bind:slug="lesson.slug"
            v-bind:courseSlug="course.slug"
        >
        </lesson-card>
 

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
import UploadFileForm from "../UploadFileForm.vue"
import LessonCard from "../Lesson/LessonCard.vue"

import Course from "../../models/Course"


export default {
  components: { UploadFileForm, LessonCard },
    name: "CoursePage",
    data: function() {
        return {
            course: null,
            user: {},
        }
    },
    created: async function() {
        let course = await this.getCourse()
        this.course = course
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
        getCourse: async function() {
            let course = await Course.find(
                "slug", this.$route.params.slug, ["lessons"]
            )
            return course
        },
    },
    computed: {
        allowEdit: function() {
            try {
                return this.course.author_id == this.user.id
            }
            catch{
                return false
            }
        }
    }
}
</script>