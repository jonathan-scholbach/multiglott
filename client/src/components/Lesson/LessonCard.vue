<template>
    <div>
        <div 
            v-if="this.lesson"
            class="material-card row"
        >
            <accomplishment-badge 
                v-if="this.lesson.accomplishment !== undefined"
                v-bind:accomplishment="this.accomplishment"
                class="material-card-badge"
            ></accomplishment-badge>
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
import Course from "../../models/Course"
import Lesson from "../../models/Lesson"
import { findApiModel } from "../../models/ApiModel"

import AccomplishmentBadge from "./AccomplishmentBadge"


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
            try{
                this.lesson = await findApiModel(
                    this.$http, Lesson, "slug",  this.slug, ["course"]
                )
            } catch (error) {
                console.log(error)
            }
            try {
                this.lesson.accomplishment = await this.lesson.getAccomplishment(
                    this.$http
                )
            } catch(error) {
                console.log("getAccomplishment Error")
                console.log(error)
            }
        },
        getCourse: async function() {
            this.course = await findApiModel(
                this.$http, 
                Course,
                "id", 
                this.lesson.course_id
            )
        }
    },
    created: async function() {
        await this.getLesson()
        await this.getCourse()
    },
    computed: {
        accomplishment: function () {
            if (this.lesson) {
                if (this.lesson.accomplishment) {
                    return this.lesson.accomplishment
                }
            }
            return 0
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
    },
    components: {
        AccomplishmentBadge
    }
    
}
</script>