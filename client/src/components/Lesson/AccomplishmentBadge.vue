<template>
    <div 
        class="material-card-badge"
        :style="cardStyles"
    >
        {{accomplishmentPercentage}}%
    </div>
</template>

<script>
import chroma from "chroma-js";
import style from "../../assets/styles/style.scss";


export default {
    props: {
        accomplishment: Number
    },
    computed:
    {
        accomplishmentPercentage() {
            return Math.round(this.accomplishment * 100)
        },
        cardStyles() {
            return {
                "background-color": chroma.mix(
                    style.themeDisabledColor,
                    style.themeColor,
                    this.accomplishment
                )
            }
    }
  }
}
</script>