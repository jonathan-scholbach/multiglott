<template>
    <div 
        v-if="this.compiledMarkdown"
        v-html="this.compiledMarkdown"
    >
    </div>
</template>

<script>
import marked from "marked"

import findApiModel from "../models/ApiModel"
import Lesson from "../models/Lesson"

export default {
    props: {
        "rawMarkdown": String,
    },
    computed: {
        compiledMarkdown: function() {
            if (this.rawMarkdown) {
                return marked(this.rawMarkdown)
            } else {
                return ""
            }
        }
    },
}
</script>