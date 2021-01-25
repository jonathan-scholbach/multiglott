<template>
    <div 
        v-if="lesson"
        class="page-body"
    >
        <div class="material-card title-card">
            <div class="material-card-content">
                <div class="row">
                    <div class="col-md-6">
                        <strong>EDIT:</strong> {{ lesson.title }}
                    </div>
                </div>    
            </div>
        </div>

        <div class="material-card">
            <div class="material-card-content">
                <form>
                    <div class="form-group">
                        <input 
                            type="text"
                            ref="lessonTitle"
                            id="lessonTitle"
                            v-model="lesson.title"
                            class="form-control"
                        >
                    </div>    
                    <div class="form-group text-right">
                        <button 
                            class="btn btn-primary"
                            @click="saveLessonTitle"
                        >Save Lesson Title
                        </button>
                    </div>
                </form>    
            </div>
        </div>
        <div class="material-card">
            <div class="material-card-content">
                <form
                    @submit.prevent="saveLessonDescription"
                >
                    <div class="form-group">
                        <textarea 
                            ref="lessonDescription"
                            v-model="description"
                            class="form-control"
                            rows=10
                        >
                        </textarea>
                    </div>            
                    <div class="form-group text-right">
                        <button
                            type="submit"
                            class="btn btn-primary"
                        >
                            Save Lesson Description
                        </button> 
                    </div>
                </form>
                
                <markdown-div v-bind:rawMarkdown=this.description></markdown-div>
            </div>
            
        </div>
        <vocab-edit-form 
            v-for="vocab in lesson.vocabs" :key="vocab.id"
            v-bind:vocab="vocab"
        ></vocab-edit-form> 
    </div>
</template>
<script>
import marked from "marked"

import { findApiModel, updateInstanceByData } from '../../models/ApiModel'
import Lesson from "../../models/Lesson"
import { Vocab } from "../../models/Vocab"
import VocabEditForm from "./VocabEditForm.vue"
import MarkdownDiv from '../MarkdownDiv.vue'


export default {
    props: ["id"],
    data: function() {
        return {
            description: "",
            lesson: null
        }
    },
    methods: {
        getLesson: async function(){
            this.lesson = await findApiModel(
                this.$http, 
                Lesson,
                "id", 
                this.lessonId, 
                ["vocabs"]
            )
            this.description = this.lesson.description
        },
        saveLessonTitle: async function() {
            let lesson = JSON.parse(JSON.stringify(this.lesson))
            lesson = updateInstanceByData(new Lesson(), lesson)
            await lesson.update(this.$http)
            this.getLesson()
        },
        saveLessonDescription: async function() {
            let lesson = JSON.parse(JSON.stringify(this.lesson))
            lesson = updateInstanceByData(new Lesson(), lesson)
            lesson.description = this.description
            await lesson.update(this.$http)
            this.getLesson()
        },
    },
    computed: {
        lessonId: function() {
            return this.$route.params.id
        },
    },
    components: {
        VocabEditForm,
        MarkdownDiv
        },
    created: async function() {
        await this.getLesson()
    }
}
</script>