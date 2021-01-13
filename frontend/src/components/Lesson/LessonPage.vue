<template>
    <div 
        v-if="this.lesson !== null"
        class="page-body"
    >
        <div class="material-card container title-card">
            <div class="row">
                <div class="col-md-6">
                    <router-link :to="{
                        name: 'course',
                        params: {
                            slug: this.courseSlug,
                        }
                    }"
                    >Back To Course</router-link>
                </div>
                <div class="col-md-6 text-right">
                    {{ lesson.title }}

                    (<span class="highlight">{{Math.round(accomplishment * 100)}} %</span>)
                </div>
            </div>
        </div>
        <vocab-test-form v-if="nextVocab" v-bind:vocab="nextVocab"></vocab-test-form> 
    </div>
</template>

<script>

import VocabTestForm from "../VocabTestForm.vue"
import Lesson from "../../models/Lesson"

export default {
    name: "LessonPage",
    props: ["lessonSlug, courseSlug"],
    data: function() {
        return {
            lesson: null,
        }
    },
    methods: {
        getLesson: async function() {
            this.lesson = await Lesson.find("slug", this.lessonSlug, ["course"])
        },
    },
    created: async function() {
        await this.getLesson()
    },
    components: {
        VocabTestForm
    }
}
</script>