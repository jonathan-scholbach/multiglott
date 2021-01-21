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
import Vocab from "../../models/Vocab"

export default {
    props: ["vocab"],
    data: function(){
        return {
            delimiter: " | ",
            source: this.vocab.source.join(" | "),
            target: this.vocab.target.join(" | "),
            hint: this.vocab.hint,
        }
    },
    computed: {
        hasChanges: function() {
            return [
                this.vocab.target.join(this.delimiter) != this.target,
                this.vocab.source.join(this.delimiter) != this.source,
                this.vocab.hint != this.hint,
            ].some(Boolean)
        },
        buttonDisabled: function(){
            return !this.hasChanges || this.proceeding
        }
    },
    methods: {
        submit: async function(){
            const targetUpdate = this.target.split(this.delimiter)
            const sourceUpdate = this.source.split(this.delimiter)
            
            let model = new Vocab(
                this.vocab.id, 
                sourceUpdate, 
                targetUpdate, 
                this.hint
            )
            this.vocab = await model.update(this.$http)
        }
    }
}
</script>