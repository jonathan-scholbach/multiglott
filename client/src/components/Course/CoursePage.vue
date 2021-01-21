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
        
        <draggable 
            v-model="lessons" 
            @start="drag=true" 
            @end="drag=false"
            @change="updateLessonsOrder"
        >
            <lesson-card
                v-for="lesson in this.lessons" :key="lesson.title"
                v-bind:slug="lesson.slug"
                v-bind:courseSlug="course.slug"
            >
            </lesson-card>
        </draggable>
 

        <div class="text-right">
        <b-button 
            v-if="this.canEdit" 
            v-b-toggle.add-lesson variant="primary"
        >
            Add Lesson
        </b-button>
        </div>
        <b-collapse id="add-lesson">
            <div v-if="this.canEdit" class="material-card">
                <div class="material-card-content">
                    <upload-file-form 
                        @uploaded="refresh"
                        url="/lessons/"
                        buttonCaption="Add New Lesson"
                        v-bind:additionalData="{
                            course_id: course.id
                        }"
                    ></upload-file-form>
                </div>    
            </div>
        </b-collapse>    
    </div>
</template>

<script>
import draggable from "vuedraggable"

import UploadFileForm from "../UploadFileForm.vue"
import LessonCard from "../Lesson/LessonCard.vue"

import Course from "../../models/Course"
import { findApiModel, updateInstanceByData } from "../../models/ApiModel"

export default {
  components: { draggable, UploadFileForm, LessonCard },
    name: "CoursePage",
    data: function() {
        return {
            course: null,
            user: {},
            lessons: [],
        }
    },
    created: async function() {
        this.user = await this.getUser()
        this.refresh()
    },
    methods: {
        refresh: async function(){
            this.course = await this.getCourse()
            this.lessons = this.course.lessons
        },
        getUser: async function() {
            let user = null
            try {
                user = await this.$http.get("/me").data
            } catch (error) {
                console.log("No authenticated user.")
            }
            return user
        },
        getCourse: async function() {
            let course = null
            try {
                course = await findApiModel(
                    this.$http, Course, "slug", this.$route.params.slug, ["lessons"]
                )
            } catch (error) {
                console.log(error)
            }
            return course
        },
        updateLessonsOrder: async function(){
            this.course.lesson_order = this.lessons.map((lesson) => lesson["id"])
            let course = JSON.parse(JSON.stringify(this.course))
            course = updateInstanceByData(new Course(), course)
            this.course = await course.update(this.$http)
        }
    },
    computed: {
        canRead: function() {
            return this.course.privileges.includes(this.$privileges.CAN_READ)
        },
        canEdit: function() {
            return this.course.privileges.includes(this.$privileges.CAN_EDIT)
        },
        canDelete: function() {
            return this.course.privileges.includes(this.$privileges.CAN_DELETE)
        }
    }
}
</script>