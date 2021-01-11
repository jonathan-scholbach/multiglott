<template>
    <div class="page-body">
        <div class="material-card container">
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

                    (<span class="brand">{{Math.round(accomplishment * 100)}} %</span>)
                </div> 
            </div>
        </div>
        <vocab-test-form v-if="nextVocab" v-bind:vocab="nextVocab"></vocab-test-form> 
    </div>
</template>

<script>

import VocabTestForm from "../VocabTestForm.vue"

export default {
    name: "LessonPage",
    data: function() {
        return {
            lessonSlug: this.$route.params.lessonSlug,
            courseSlug: this.$route.params.courseSlug,
            lesson: {},
            canEdit: false,
            canRead: false,
            canDelete: false,
            accomplishment: 0,
            nextVocab: false,
        }
    },
    created: async function() {
        await this.getLesson()
        await this.loadVocable()
    },
    methods: {
        loadVocable: async function() {
            var self = this
            console.log("leson.id: ", this.lesson.id)
            var url = "/me/lesson/" + this.lesson.id
            this.$http.get(
                url
            ).then(
                (response) => {
                    self.nextVocab = response.data.vocab
                    self.accomplishment = response.data.accomplishment
                    console.log("nextVocab in LessonPage: ", self.nextVocab)
                }
            )
        },
        getLesson: async function() {
            var self = this
            this.$http.get(
                "/courses/" + this.courseSlug + "/lessons/" + this.lessonSlug
            ).then(
                (response) => {
                    self.lesson = response.data
                    this.$http.post(
                        "/privileges/",
                        {
                            entity_type: "Lesson",
                            entity_key: "id",
                            entity_value: self.lesson.id
                        },
                        {
                            headers: {
                                "Content-Type": "application/json"
                            }
                        }
                    ).then(
                        (response) => {
                            let privileges = response.data
                            self.canEdit = privileges.includes(this.$privileges.CAN_EDIT)
                            self.canRead = privileges.includes(this.$privileges.CAN_READ)
                            self.canDelete = privileges.includes(this.$privileges.CAN_DELETE)
                        }
                    ).catch(
                        (error) => {
                            console.log(error)
                        }
                    )
                }
            ).catch(
                (error) => {
                    console.log(error)
                }
            )

            
        },
    },
    components: {
        VocabTestForm
    }
}
</script>