<template>
<div>
    <div v-for="(peer_info, id) in elephants" :key="id">
        <ElephantFriend
            :hue="peer_info.hue"
            :currentX="peer_info.currentX"
            :targetX="peer_info.targetX"
            />
    </div>
</div>
</template>

<script>
import ElephantFriend from "./ElephantFriend";
import {BASE_URL} from "../utils";

export default {

    components: {
        ElephantFriend,
    },

    props: {
        ignore: { type: String }
    },

    data() {
        return {
            elephants: {}
        }
    },

    mounted() {
        this.peerInterval = setInterval(() => {
            fetch(`${BASE_URL}/peers/${this.ignore}`).then(res => res.json()).then(j => {
                this.elephants = j;
            })
        }, 4000);
    }
}
</script>

