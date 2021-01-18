<template>
    <div>
        <div 
            v-if="this.lesson"
            class="material-card row"
        >      
            <div  
                v-if="this.lesson.accomplishment !== undefined"
                class="material-card-badge"
            >
                {{ accomplishment }}%
            </div>
            <div class="material-card-content">
                <router-link
                    v-if="this.course && this.canRead"
                    :to="{
                        name: 'lesson',
                        params: {
                            lessonSlug: this.lesson.slug,
                            courseSlug: this.course.slug,
                        },
                        props: {
                            lesson:this.lesson
                        }
                }">{{lesson.title}}</router-link>
            </div>
            <div class="material-card-right">
                <router-link 
                    :to="{
                        name: 'editLesson',
                        params: {
                            id: this.lesson.id
                        }
                    }"
                    v-if="this.canEdit"
                >
                    ⚙
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import { findCourse, Course } from "../../models/Course"
import { findLesson, Lesson } from "../../models/Lesson"

export default {
    name: "LessonCard",
    props: ["slug"],
    data: function() {
        return {
            lesson: null,
            course: null,
        }
    },
    methods: {
        getLesson: async function() {
            this.lesson = await findLesson(
                this.$http, "slug",  this.slug, ["course"]
            )
            this.lesson.accomplishment = await this.lesson.getAccomplishment(this.$http)
        },
        getCourse: async function() {
            console.log("course.id, ", this.lesson.course_id)
            this.course = await findCourse(this.$http, "id", this.lesson.course_id)
        }
    },
    created: async function() {
        await this.getLesson()
        await this.getCourse()
    },
    computed: {
        accomplishment: function () {
            return Math.round(this.lesson.accomplishment * 100)
        },
        canRead: function() {
            if (this.lesson) {
                return this.lesson.privileges.includes(
                    this.$privileges.CAN_READ
                )
            }
            return false
        },
        canEdit: function() {
            if (this.lesson) {
                return this.lesson.privileges.includes(
                    this.$privileges.CAN_EDIT
                )
            }
            return false
        },
        canDelete: function() {
            if (this.lesson) {
                return this.lesson.privileges.includes(
                    this.$privileges.CAN_DELETE
                )
            }
            return false
        },
    }
    
}
</script>