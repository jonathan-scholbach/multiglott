<template>
    <div 
        v-if="this.lesson !== null"
        class="page-body"
    >
        <div class="material-card title-card">
            <div class="material-card-content">
                EDIT {{ lesson.title }}
            </div>
        </div>
        <vocab-edit-form 
            v-for="vocab in lesson.vocabs" :key="vocab.id"
            v-bind:vocab="vocab"
        ></vocab-edit-form> 
    </div>
</template>
<script lang="ts">
import Lesson from "../../models/Lesson"
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
            this.lesson = await Lesson.find("id", this.lessonId, ["vocabs"])
            console.log(this.lesson)
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