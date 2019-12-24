<template>
    <div @click="clickedScope" id="everything">
        <div @click="clickedScope" class="clicktarget"></div>
        <div class="scope"></div>
        <World />
        <img
            src="../assets/elephant_walk.gif"
            v-bind:style="{
                left: (this.currentX || this.targetX || 0) + 'px',
                transform: 'scale(' + (this.flip == 'R' ? 1 : -1) + ', 1)',
                visibility: this.walking ? 'visible' : 'hidden',
                filter: 'hue-rotate(' + this.hue + 'deg)',
                'z-index': 9999
            }"
            class="my-elephant"
        />
        <img
            src="../assets/elephant_stand.png"
            v-bind:style="{
                left: (this.currentX || this.targetX || 0) + 'px',
                transform: 'scale(' + (this.flip == 'R' ? 1 : -1) + ', 1)',
                visibility: this.walking ? 'hidden' : 'visible',
                filter: 'hue-rotate(' + this.hue + 'deg)',
                'z-index': 9999
            }"
            class="my-elephant"
        />

        <EverybodyElse :ignore="this.id" />

        <div class="menu">
            <input
                type="range"
                v-model="hue"
                name="hue"
                id="hueinput"
                min="0"
                max="360"
                style="width: 50vw; margin: auto;"
            />
            <br />
            <button @click="geolocateMe">Locate Me!</button>
        </div>
    </div>
</template>

<script>
import DeviceUUID from "device-uuid";
import EverybodyElse from "./EverybodyElse";
import World from "./World";
import { lngToPix, BASE_URL, REPORT_FREQUENCY } from "../utils";

const TOLERANCE = 40;
const SPEED = 3;

var du = new DeviceUUID.DeviceUUID().parse();
var dua = [
    du.language,
    du.platform,
    du.os,
    du.cpuCores,
    du.isAuthoritative,
    du.silkAccelerated,
    du.isKindleFire,
    du.isDesktop,
    du.isMobile,
    du.isTablet,
    du.isWindows,
    du.isLinux,
    du.isLinux64,
    du.isMac,
    du.isiPad,
    du.isiPhone,
    du.isiPod,
    du.isSmartTV,
    du.pixelDepth,
    du.isTouchScreen
];
var ID = du.hashMD5(dua.join(":"));

export default {
    name: "MainRender",
    components: {
        EverybodyElse,
        World
    },

    props: {
        name: String
    },

    methods: {
        clickedScope(ev) {
            if (!this.interacting) {
                return;
            }
            this.targetX = ev.pageX - 40;

            fetch(`${BASE_URL}/report/${this.id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    currentX: this.currentX,
                    targetX: this.targetX,
                    hue: this.hue
                })
            })
                .then(res => res.json())
                .then(j => {
                    if (j.response && "hue" in j.response) {
                        this.hue = parseFloat(j.response.hue);
                    }
                });
        },

        geolocateMe() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(position => {
                    this.currentX = lngToPix(position.coords.longitude);
                    this.targetX = lngToPix(position.coords.longitude);
                });
            } else {
                return;
            }
        }
    },
    data() {
        return {
            interacting: false,
            targetX: 0,
            currentX: 0,
            flip: "R",
            walking: false,
            hue: 60,
            speed: 3,
            id: undefined
        };
    },
    mounted() {
        this.id = `${ID}-${this.name}`;
        this.speed = SPEED;
        window.E = this;

        window.onkeyup = ev => {
            if (ev.key == "ArrowLeft") {
                this.targetX = this.targetX - 1000;
            }
            if (ev.key == "ArrowRight") {
                this.targetX = this.targetX + 1000;
            }
        };

        window.goToLng = lng => {
            this.currentX = lngToPix(lng);
            this.targetX = lngToPix(lng);
        };
        window.goToPix = pix => {
            this.currentX = pix;
            this.targetX = pix;
        };

        let renderAll = position => {
            let browserLat = lngToPix(position.coords.longitude);
            this.browserLat = browserLat;

            fetch(`${BASE_URL}/peer/${this.id}`)
                .then(res => {
                    if (res.ok) {
                        return res.json();
                    }
                })
                .then(j => {
                    if ("response" in j && j.response) {
                        this.interacting = true;
                        console.log(j.response);
                        if ("hue" in j.response) {
                            this.hue = parseFloat(j.response.hue);
                        }
                        this.currentX = j.response.currentX || browserLat;
                        this.targetX = j.response.targetX || browserLat;
                    } else {
                        this.currentX = browserLat;
                        this.targetX = browserLat;
                    }

                    this.frameInterval = setInterval(() => {
                        // Array.from(document.querySelectorAll(".my-elephant"))[0].scrollIntoView();
                        window.scroll(this.currentX - window.innerWidth / 2, 0);

                        if (this.currentX < this.targetX - TOLERANCE) {
                            this.currentX += this.speed;
                            this.flip = "R";
                            this.walking = true;
                        } else if (this.currentX > this.targetX + TOLERANCE) {
                            this.currentX -= this.speed;
                            this.flip = "L";
                            this.walking = true;
                        } else {
                            this.walking = false;
                        }

                        if (this.currentX > 240000 - 500) {
                            this.currentX = 500;
                        }
                        if (this.currentX < 500) {
                            this.currentX = 240000 - 500;
                        }
                    }, 60);

                    let reportLocation = () => {
                        fetch(`${BASE_URL}/report/${this.id}`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                currentX: this.currentX,
                                targetX: this.targetX,
                                hue: this.hue
                            })
                        });
                        this.reportInterval = setTimeout(
                            reportLocation,
                            REPORT_FREQUENCY
                        );
                    };
                    reportLocation = reportLocation.bind(this);
                    reportLocation();
                });
        };
        renderAll = renderAll.bind(this);
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(renderAll);
        } else {
            renderAll({ coords: { longitude: 0 } });
        }
    }
};
</script>

<style scoped>
.clicktarget {
    position: fixed;
    width: 100%;
    height: 100%;
}

.scope {
    position: absolute;
    bottom: 25vh;
    width: 240000px;
    border-top: 1em solid #444;
}

.my-elephant {
    height: 4em;
    position: absolute;
    bottom: 25vh;
    box-shadow: 0px 4em 0px -1.9em yellow;
}

.menu {
    width: 100%;
    position: fixed;
    text-align: center;
    bottom: 0;
}
</style>
