<script>
export default {
    name: "Lesson",
    props: ["lessonSlug", "courseSlug"],
    data: function() {
        return {
            lesson: {},
            canEdit: false,
            canRead: false,
            canDelete: false,
            accomplishment: null,
            nextVocab: {},
        }
    },
    mounted: function() {
        this.getLesson()
        this.loadNextVocable()
    },
    methods: {
        loadNextVocable: function() {
            var self = this
            var url = "/me/lesson/" + this.lessonSlug
            console.log(url)
            this.$http.get(
                url
            ).then(
                (response) => {
                    self.nextVocab = response.data.vocab
                    self.accomplishment = response.data.accomplishment
                }
            )
        },
        getLesson: function() {
            var self = this
            this.$http.get(
                "/courses/" + this.courseSlug + "/lessons/" + this.lessonSlug
            ).then(
                (response) => {
                    self.lesson = response.data
                }
            ).catch(
                (error) => {
                    console.log(error)
                }
            )

            this.$http.post(
                "/privileges/",
                {
                    entity_type: "Lesson",
                    entity_key: "slug",
                    entity_value: self.lessonSlug
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
        },
    },
    render: function() {
        return this.$scopedSlots.default({})
    },
}
</script>