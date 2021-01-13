<template>
    <div>
        <div class="material-card vocab-card">
            <div class="material-card-content">
                <div 
                    v-if="vocab.source"
                    class="form-group vocab-question"
                >
                    <span 
                        v-for="(entry, index) in vocab.source" :key="index">
                        {{entry}}
                    <span class="normal-text" v-if="index != vocab.source.length-1"> | </span>
                    </span>
                </div>

                <div v-if="showHint" class="form-group vocab-hint">
                    {{ hint }}
                </div>

                <div class="form-group vocab-answer">
                    <input 
                        class="form-control" 
                        type="text" 
                        id="answer"
                        ref="answer"
                        v-model="answer"
                        autocomplete="off"
                    />
                </div>
                
                <div class="text-right vertical-distance-buttons">
                    <button 
                        @click="revealHint"
                        class="btn btn-outline-primary" 
                        data-toggle="tooltip" 
                        data-placement="top" 
                        title='Get a hint by typing "?"'
                        tabindex="3"
                    >
                        ?
                    </button>

                    <button
                        v-on:click="submit"
                        class="btn btn-primary" 
                        tabindex="2"
                    >
                        {{ buttonCaption }}
                    </button>
                </div>    
            </div>
        </div>

        <div v-if="answerCorrect" class="alert alert-success alert-answer-correct">
                🎉 🥳 Well done! 🥳 🎉
            <div v-if="possibleAnswers.length">
                Keep naming synonyms.
                <div class="given-answer" v-for="givenAnswer in givenAnswers" :key="givenAnswer">
                    {{ givenAnswer }}
                </div>                        
        </div>
        </div>
        
        <div v-if="answerCorrect === false" class="alert alert-danger alert-answer-wrong">
            Oh no! The correct answer(s) would have been:
            <ul>
                <li v-for="answer in possibleAnswers" :key="answer">{{answer}}</li>
            </ul> 
        </div>   
    </div>        
</template>

<script>
export default {
    props: ["vocab"],
    data: function(){
        return this.initialState();
    },
    computed: {
        possibleAnswers: function() {
            return this.vocab.target.filter(
                answer=>!this.givenAnswers.includes(answer)
            )
        },
        finished: function() {
            return (!this.possibleAnswers.length) || (this.answerCorrect === false)
        },
        hint: function() {
            if (this.vocab.hint) {
                return this.vocab.hint
            }
            else {
                if (this.finished){
                    return ""
                }
                
                let nextAnswer = this.possibleAnswers[0]
                
                let obusccatedHintWords = []
                nextAnswer.split(" ").forEach(
                    word => {
                        let obfuscatedWord = word[0] + "*".repeat(word.length - 1)
                        obusccatedHintWords.push(obfuscatedWord)
                    }
                )
                return obusccatedHintWords.join(" ")
            }
        },
        buttonCaption: function() {
            if (this.finished) {
                return "Continue"
            } else {
                return "Answer"
            }
        }
    },
    methods: {
        initialState(){
            return {
                showHint: false,
                answer: "",
                sourceText: "",
                givenAnswers: [],
                answerCorrect: null,
            }
        },
        refresh: async function(){
            Object.assign(this.$data, this.initialState())
        },
        revealHint: function() {
            this.showHint = true
            this.answer = ""
        },
        submit: function(){
            if (this.finished){
                this.$emit("vocabFinished")
                this.refresh()
            } else {
                this.processAnswer()
            }
        },
        processAnswer: function() {
            if (this.answer == "?"){
                this.revealHint()
            }
            else {
                this.answerCorrect = this.possibleAnswers.includes(this.answer)
                this.givenAnswers.push(this.answer)

                if (this.finished) {
                    this.postProgress()   
                }
            }
        },
        postProgress: function () {
            this.$http.post(
                "/me/vocab/" + this.vocab.id,
                {
                    answer_correct: this.answerCorrect
                },
                {
                    headers: {
                        "Content-Type": "application/json ",
                    },
                }

            ).catch(
                (error) => {
                    console.log(error)
                }
            )
        },
    },
}
</script>