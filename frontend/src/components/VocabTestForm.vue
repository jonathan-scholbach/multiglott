<template>
    <div>
        <div class="material-card vocab-card">
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

        <div v-if="answerCorrect" class="alert alert-success alert-answer-correct">
                🎉 🥳 Well done! 🥳 🎉
            <div v-if="correctAnswers.length">
                Keep naming synonyms. {{this.correctAnswers}}
                <div class="given-answer" v-for="givenAnswer in givenAnswers" :key="givenAnswer">
                    {{ givenAnswer }}
                </div>                        
        </div>
        </div>
        
        <div v-if="answerCorrect === false" class="alert alert-danger alert-answer-wrong">
            Oh no! The correct answer(s) would have been:
            <ul>
                <li v-for="answer in correctAnswers" :key="answer">{{answer}}</li>
            </ul> 
        </div>   
    </div>        
</template>

<script>
export default {
    props: ["vocab"],
    data: function(){
        return {
            showHint: false,
            answer: "",
            sourceText: "",
            givenAnswers: [],
            correctAnswers: [],
            answerCorrect: null,
        }
    },
    computed: {
        finished: function() {
            return (!this.correctAnswers.length) || (this.answerCorrect === false)
        },
        hint: function() {
            if (this.vocab.hint) {
                return this.vocab.hint
            }
            else {
                if (this.finished){
                    return ""
                }
                
                let nextAnswer = this.correctAnswers[0]
                
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
        initialiseCorrectAnswer: function() {
            this.correctAnswers = this.vocab.target
        },
        revealHint: function() {
            this.showHint = true
            this.answer = ""
        },
        submit: function(){
            if (this.finished){
                this.goToNextVocab()
            } else {
                this.processAnswer()
            }
        },
        processAnswer: function() {
            if (this.answer == "?"){
                this.revealHint()
            }
            else {
                this.givenAnswers.push(this.answer)

                if (this.correctAnswers.includes(this.answer)) {
                    this.answerCorrect = true
                    this.correctAnswers.splice(
                        this.correctAnswers.indexOf(this.answer), 
                        1
                    )    
                } else {
                    this.answerCorrect = false
                }
                if (this.finished) {
                    this.postProgress()   
                }
            }
        },
        postProgress: function () {
            console.log(this.answerCorrect)
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
        goToNextVocab: async function() {
            this.showHint = false
            this.answer = ""
            this.givenAnswers = []
            this.answerCorrect = null
            console.log(this.finished)

            await this.$parent.loadVocable()
            console.log(this.vocab)
            console.log("correctAnswers.length", this.correctAnswers.length)
            console.log(this.finished)
            this.initialiseCorrectAnswer()
            console.log("correctAnswers.length", this.correctAnswers.length)
            console.log(this.finished)

            this.$nextTick(() => this.$refs.answer.focus())
        }
    },
    created: function() {
        this.initialiseCorrectAnswer()
        this.$nextTick(() => this.$refs.answer.focus())
    },
}
</script>