<template>
    <div class="material-card row" v-if="this.lesson">
        <div class="col-md-10">
            <router-link 
                v-if="this.canRead"
                :to="{
                    name: 'lesson',
                    params: {
                        lessonSlug: this.lesson.slug,
                        courseSlug: this.course.slug
                    }
            }">{{lesson.title}}</router-link>
        </div>
        <div 
            v-if="this.lesson.accomplishment !== undefined"
            class="md-col-2"
        >
            {{lesson.accomplishment}}%
        </div>
    </div>
</template>

<script>
import Lesson from "../../models/Lesson"

export default {
    name: "LessonCard",
    props: ["slug", "course"],
    data: function() {
        return {
            lesson: null
        }

    },
    methods: {
        getLesson: async function() {
            let lesson = new Lesson()
            lesson.slug = this.slug
            await lesson.find()
            return lesson
        },
    },
    created: async function() {
        let lesson = await this.getLesson()
        this.lesson = lesson
        let accomplishment = await this.lesson.getAccomplishment(this.$http)
        this.lesson.accomplishment = accomplishment
    },
    computed: {
        canRead: function() {
            if (this.lesson) {
                return this.lesson.privileges.includes("CAN_READ")
            }
            return false
        }
    }
    
}
</script>