<template>
    <div class="material-card row" v-if="this.lesson">
        <div class="col-md-10">
            <router-link 
                v-if="this.canRead"
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
        <div 
            v-if="this.lesson.accomplishment !== undefined"
            class="md-col-2"
        >
            {{lesson.accomplishment}} %
        </div>
    </div>
</template>

<script>
import Course from "../../models/Course"
import Lesson from "../../models/Lesson"


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
            this.lesson = await Lesson.find("slug", this.slug, ["course"])
            this.lesson.accomplishment = await this.lesson.getAccomplishment(this.$http)
        },
        getCourse: async function() {
            this.course = await Course.find("id", this.lesson.course_id)
        }
    },
    created: async function() {
        await this.getLesson()
        await this.getCourse()
    },
    computed: {
        canRead: function() {
            if (this.lesson) {
                return this.lesson.privileges.includes(this.$privileges.CAN_READ)
            }
            return false
        }
    }
    
}
</script>