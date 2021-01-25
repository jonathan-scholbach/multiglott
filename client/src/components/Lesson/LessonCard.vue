<template>
    <div>
        <div 
            v-if="this.lesson"
            class="material-card row"
        >
            <accomplishment-badge 
                v-if="this.loggedIn"
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
            this.lesson = await findApiModel(
                this.$http, Lesson, "slug",  this.slug, ["course"]
            )
            if (this.loggedIn){
                this.lesson.accomplishment = await this.lesson.getAccomplishment(
                    this.$http
                )
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
        loggedIn: function() {
            console.log(this.$store)
            return this.$store.getters.loggedIn
        },
        accomplishment: function () {
            if (this.lesson) {
                if (this.lesson.accomplishment === 0){
                    return 0
                }
                if (this.lesson.accomplishment) {
                    return this.lesson.accomplishment
                }
                
            }
            
        },
        canRead: function() {
            console.log("lesson ", this.lesson)
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