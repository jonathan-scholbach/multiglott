<template>
    <div class="material-card container">
        <form 
            @submit.prevent="submit"
            class="material-card-content row">
            <div class="form-group row">
                <label for="source" class="col-sm-2 col-form-label">
                    Source:
                </label>
                <div class="col-sm-10">
                    <input 
                        ref="source"
                        id="source"
                        type="text" 
                        class="form-control"
                        v-model="source"
                    >
                </div>
            </div>    

            <div class="form-group row">
                <label for="target" class="col-sm-2 col-form-label">
                    Target:
                </label>
                <div class="col-sm-10">
                    <input 
                        ref="target" 
                        type="text" 
                        id="target"
                        class="form-control"
                        v-model="target"
                    >
                </div>    
            </div>    

            <div class="form-group row">
                <label for="hint" class="col-sm-2 col-form-label">
                    Hint:
                </label>
                <div class="col-sm-10">
                    <input 
                        ref="hint"
                        id="hint"
                        type="text"
                        class="form-control"
                        v-model="hint"
                    >
                </div>
            </div>    
            <div class="form-group row text-right">
                <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="buttonDisabled"
                >
                    Update
                </button>
            </div>    
        </form>
    </div>
</template>

<script>
export default {
    props: ["vocab"],
    data: function(){
        return {
            source: this.vocab.source,
            target: this.vocab.target,
            hint: this.vocab.hint,
            proceeding: false,
        }
    },
    computed: {
        hasChanges: function() {
            return [
                this.vocab.target != this.target,
                this.vocab.source != this.source,
                this.vocab.hint != this.hint,
            ].some(Boolean)
        },
        buttonDisabled: function(){
            return !this.hasChanges || this.proceeding
        }
    },
    methods: {
        submit: async function(){
            // this.proceeding = true
            // this.vocab = await this.vocab.update({
            //         target: this.target,
            //         source: this.source,
            //         hint: this.hint
            // })
            // this.proceeding = false
            console.log(this.vocab)
        }
    }
}
</script>