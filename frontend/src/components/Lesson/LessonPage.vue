<template>
    <div 
        v-if="this.lesson !== null"
        class="page-body"
    >
        <div class="material-card title-card">
            <div 
                v-if="this.lesson.accomplishment !== undefined"
                class="material-card-badge"
            >
                {{Math.round(lesson.accomplishment * 100)}}%
            </div>
            <div class="material-card-content">
                <div class="row">
                    <div class="col-md-6">
                        {{ lesson.title }}
                    </div>
                    <div class="col-md-6 text-right">
                        <router-link 
                            :to="{
                                name: 'course',
                                params: {
                                    slug: this.courseSlug,
                                }
                            }"
                        >
                            Back To Course
                        </router-link>
                    </div>
                </div>    
            </div>
        </div>
        <vocab-test-form 
            v-if="currentVocab" 
            v-bind:vocab="currentVocab"
            @vocabFinished="loadVocab"
        ></vocab-test-form> 
    </div>
</template>

<script>

import VocabTestForm from "./VocabTestForm.vue"
import Lesson from "../../models/Lesson"

export default {
    name: "LessonPage",
    data: function() {
        return {
            currentVocab: null,
            lesson: null,
        }
    },
    methods: {
        getLesson: async function() {
            this.lesson = await Lesson.find("slug", this.lessonSlug, ["course"])
            this.lesson.accomplishment = await this.lesson.getAccomplishment()
        },
        loadVocab: async function() {
            this.currentVocab = await this.lesson.getNextVocab()
        }
    },
    created: async function() {
        await this.getLesson()
        await this.loadVocab()
    },
    computed: {
        lessonSlug: function() {
            return this.$route.params.lessonSlug
        },
        courseSlug: function() {
            return this.$route.params.courseSlug
        }
    },
    components: {
        VocabTestForm
    }
}
</script>