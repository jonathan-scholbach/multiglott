<template>
    <div 
        v-if="this.lesson !== null"
        class="page-body"
    >
        <div class="material-card title-card">
            <div class="material-card-content">
                <input 
                    type="text"
                    ref="lessonTitle"
                    id="lessonTitle"
                    v-model="lesson.title">
            </div>
            <div class="material-card-right"> 
                <button 
                    class="btn btn-success"
                    @click="updateLessonTitle"
                >Update Lesson Title
                </button>
            </div>
        </div>
        <vocab-edit-form 
            v-for="vocab in lesson.vocabs" :key="vocab.id"
            v-bind:vocab="vocab"
        ></vocab-edit-form> 
    </div>
</template>
<script>
import { findApiModel } from '../../models/ApiModel'
import Lesson from "../../models/Lesson"
import { Vocab } from "../../models/Vocab"
import VocabEditForm from "./VocabEditForm.vue"


export default {
    props: ["id"],
    data: function() {
        return {
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
        },
        updateLessonTitle: async function() {

        }
    },
    components: {
        VocabEditForm
    },
    computed:  {
        lessonId: function() {
            return this.$route.params.id
        }
    },
    created: async function() {
        await this.getLesson()
    }
}
</script>