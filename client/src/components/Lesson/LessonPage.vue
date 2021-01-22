<template>
    <div 
        v-if="this.lesson !== null"
        class="page-body"
    >        
        <div class="material-card">
            
            <accomplishment-badge :accomplishment="this.lesson.accomplishment">
            </accomplishment-badge>
            
            <div class="material-card-content title-card">
                <span class="title">{{ lesson.title }}</span>
            </div>
            
            <div class="material-card-right">
                <div v-if=this.lesson.description>
                    <router-link 
                        
                        :to="{
                            name: 'lessonDescription',
                            params: {
                                courseSlug: this.courseSlug,
                                lessonSlug: this.lessonSlug
                            }
                        }"
                    >
                        Explanation for this Lesson
                    </router-link>
                </div>
                <div>
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
import AccomplishmentBadge from './AccomplishmentBadge.vue'
import { findApiModel } from '../../models/ApiModel'

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
            this.lesson = await findApiModel(this.$http, Lesson, "slug", this.lessonSlug, ["course"])
            this.lesson.accomplishment = await this.lesson.getAccomplishment(this.$http)
        },
        loadVocab: async function() {
            this.currentVocab = await this.lesson.getNextVocab(this.$http)
            this.lesson.accomplishment = await this.lesson.getAccomplishment(this.$http)
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
        VocabTestForm,
        AccomplishmentBadge
    }
}
</script>