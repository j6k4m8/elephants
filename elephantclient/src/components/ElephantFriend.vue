<template>
    <div>
        <img
        src='../assets/elephant_walk.gif'
        v-bind:style="{
                'left': (this.currentX_ || this.targetX || 0 ) + 'px',
                'transform': 'scale(' + (this.flip == 'R' ? 1 : -1) + ', 1)',
                'visibility': this.walking ? 'visible' : 'hidden',
                'filter': 'hue-rotate('+ this.hue + 'deg)'
            }"
        class="peer-elephant" />
    <img
        src='../assets/elephant_stand.png'
        v-bind:style="{
                'left': (this.currentX_ || this.targetX || 0 ) + 'px',
                'transform': 'scale(' + (this.flip == 'R' ? 1 : -1) + ', 1)',
                'visibility': this.walking ? 'hidden' : 'visible',
                'filter': 'hue-rotate('+ this.hue + 'deg)'
            }"
        class="peer-elephant" />
    </div>
</template>

<script>
import {BASE_URL} from "../utils";
import EverybodyElse from "./EverybodyElse";

const TOLERANCE = 40;
const SPEED = 3;


export default {
    name: 'ElephantFriend',
    components: {
        EverybodyElse,
    },

    props: {
        hue: {type: Number},
        currentX: {type: Number},
        targetX: {type: Number},
    },

    data() {
        return {
            targetX_: 0,
            currentX_: 0,
            flip: "R",
            walking: false,
        }
    },
    mounted() {
        this.currentX_ = this.currentX;
        this.targetX_ = this.targetX;
        this.frameInterval = setInterval(() => {
            if (this.currentX_ < (this.targetX - TOLERANCE)) {
                this.currentX_ += SPEED;
                this.flip = "R";
                this.walking = true;
            } else if (this.currentX_ > (this.targetX + TOLERANCE)) {
                this.currentX_ -= SPEED;
                this.flip = "L";
                this.walking = true;
            } else {
                this.walking = false;
            }
        }, 60);
    }
}

</script>

<style scoped>
.peer-elephant {
    height: 4em;
    position: absolute;
    bottom: 25vh;
}
</style>
