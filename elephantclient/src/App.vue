<template>
  <div id="app">
    <div v-if="name">
      <MainRender :name="name" />
    </div>
    <div v-else>
      <input type="text" placeholder="Your name" @blur="setName">
      <button>Go</button>
      <div>
        {{name}}
      </div>
    </div>
  </div>
</template>

<script>
import MainRender from './components/MainRender.vue'

export default {
  name: 'app',
  components: {
    MainRender
  },
  data() {
    let name = localStorage.getItem("name");
    return {name,};
  },
  methods: {
    setName(ev) {
      localStorage.setItem("name", ev.target.value);
      this.name = ev.target.value;
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

* {
  box-sizing: border-box;
}

body, html {
  margin: 0;
  overscroll-behavior-y: none;
  overscroll-behavior-x: none;
}

</style>
