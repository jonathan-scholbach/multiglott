<template>
    <div>
        <div 
            class="material-card"
        >
            <div class="material-card-content title-card">
                Explanation: <span class="title">{{this.lesson.title}}</span>
            </div> 
            <div class="material-card-right">
                <router-link
                    :to="{
                        name: 'lesson',
                        params: {
                            lessonSlug: this.lessonSlug,
                            courseSlug: this.courseSlug
                        }
                    }"
                >
                    Practice this Lesson
                </router-link>
            </div>   
        </div>
        <div class="material-card">
            <div class="material-card-content">
                <markdown-div 
                    v-if="this.lesson"
                    v-bind:rawMarkdown=lesson.description>
                </markdown-div>
            </div>
        </div> 
    </div>
</template>

<script>
import { findApiModel } from "../../models/ApiModel"

import Lesson from "../../models/Lesson"
import MarkdownDiv from "../MarkdownDiv"


export default {
    data: function() {
        return {
            lesson: null,
            lessonSlug: this.$route.params.lessonSlug,
            courseSlug: this.$route.params.courseSlug
        }
    },
    methods: {
        getLesson: async function() {
            console.log(this.lessonSlug)
            this.lesson = await findApiModel(this.$http, Lesson, "slug", this.lessonSlug)
        }
    },
    mounted: async function() {
        await this.getLesson()
    },
    components: {
        MarkdownDiv
    }
}
</script>