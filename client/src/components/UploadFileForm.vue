<template>
    <form 
        @submit.prevent="submit"
    >
        <div class="form-group">
            <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
        </div>
        
        <div class="text-right">
            <button type="submit" class="btn btn-primary">{{this.buttonCaption}}</button>
        </div>    
    </form>
</template>

<script>
    export default {
        name: "UploadForm",
        props: ["url", "buttonCaption", "additionalData"],
        data: function() {
            return {
                file: "",
            }
        },
        methods: {
            handleFileUpload(){
                this.file = this.$refs.file.files[0]
            },   
            submit: function () {
                let formData = new FormData();
                formData.append("file", this.file)
                
                for (const [key, value] of Object.entries(this.additionalData)){
                    formData.append(key, value)
                }
                
                this.$http.post(
                    this.url,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'       
                        }
                    }
                ).then((response) => {
                    this.$emit("uploaded", response)

                }).catch(
                    (error) => {
                        console.log(error)
                    }
                )
                
            }
        }
    }
</script>