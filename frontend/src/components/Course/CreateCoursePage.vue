<template>
     <div>
        <div class="page-body">
            <create-course-form />
        </div>
    </div>
</template>

<script>
import CreateCourseForm from "./CreateCourseForm.vue"

export default {
    name: "CreateCoursePage",
    components: {
        CreateCourseForm,
    },
}
</script>