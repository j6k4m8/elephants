<template>
    <div>
        <!-- <img class="feature-image" src="../assets/locations/dc.png" height=500 /> -->
        <div v-for="feature in features">
            <img
                class="feature-image"
                :src="feature.path"
                :style="{
                    'left': feature.location + 'px'
                }"
                />
        </div>
        <div v-for="tree in trees">
            <img
                class="tree-image"
                :src="tree.path"
                :style="{
                    'left': tree.location + 'px'
                }"
                />
        </div>
    </div>
</template>


<script>
import {lngToPix} from "../utils";

const FEATURES = [{
    name: "Chicago",
    location: lngToPix(-87.63),
    path: require("../assets/locations/chicago.png")
}, {
    name: "Miami",
    location: lngToPix(-80.19),
    path: require("../assets/locations/miami.png")
}, {
    name: "DC",
    location: lngToPix(-77.03),
    path: require("../assets/locations/dc.png")
}, {
    name: "Philadelphia",
    // location: lngToPix(-76.63),
    location: lngToPix(-75.00),
    path: require("../assets/locations/philadelphia.png")
}, {
    name: "NYC",
    location: lngToPix(-74.00),
    path: require("../assets/locations/nyc.png")
}, {
    name: "London",
    location: lngToPix(0.1),
    path: require("../assets/locations/london.png")
}, {
    name: "Barcelona",
    location: lngToPix(2.0),
    path: require("../assets/locations/barcelona.png")
}, {
    name: "Paris",
    location: lngToPix(2.7),
    path: require("../assets/locations/paris.png")
}, {
    name: "Giza",
    location: lngToPix(31.2),
    path: require("../assets/locations/giza.png")
}, {
    name: "Jerusalem",
    location: lngToPix(35.2),
    path: require("../assets/locations/jerusalem.png")
}, {
    name: "Pisa",
    location: lngToPix(10.39),
    path: require("../assets/locations/pisa.png")
}, {
    name: "Rome",
    location: lngToPix(12.49),
    path: require("../assets/locations/rome.png")
}, {
    name: "Moscow",
    location: lngToPix(37.62),
    path: require("../assets/locations/moscow.png")
}, {
    name: "Agra",
    location: lngToPix(78.01),
    path: require("../assets/locations/agra.png")
}, {
    name: "Sydney",
    location: lngToPix(151.21),
    path: require("../assets/locations/sydney.png")
}]


export default {
    data() {
        return {
            features: FEATURES,
            trees: new Array(300).fill(0).map(() => {
                return {
                    location: Math.random() * 240000,
                    path: require(`../assets/trees/tree_1000${Math.ceil(Math.random()*4)}.png`)
                }
            })
        }
    }
}
</script>

<style scoped>
.feature-image {
    position: absolute;
    bottom: 25vh;
    left: 0;
    height: 50vh;
    max-height: 300px;
}

.tree-image {
    position: absolute;
    bottom: 25vh;
    left: 0;
    height: 30vh;
    max-height: 200px;
    z-index: -1;
}
</style>
