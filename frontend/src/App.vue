<template>
  <div id="app">
    <ki-title class="title"></ki-title>
    <search-bar class="search-bar" @search="performAnalysis($event)"></search-bar>
    <word-analysis class="analysis" v-if="analysisData" :data="analysisData"></word-analysis>
    <template v-else>
      <p>Try out a word and press enter!</p>
    </template>
  </div>
</template>

<script>
import KiTitle from './components/KiTitle.vue';
import SearchBar from './components/SearchBar.vue';
import WordAnalysis from './components/WordAnalysis.vue';

export default {
  name: 'App',
  components: {
    KiTitle,
    SearchBar,
    WordAnalysis
  },
  data() {
    return {
      analysisData: null
    };
  },
  methods: {
    async performAnalysis(input) {
      try {
        const response = await fetch(`/analyse_word/${input}`)
        const json = await response.json();

        if (json.error) {
          return;
        }

        this.analysisData = json;
      } catch (ex) {
        console.log(ex);
      }
    }
  }
}
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;

    display: flex;
    flex-direction: column;
    align-items: center;

    margin-top: 20vh;
  }

  .title {
    font-size: 3vh;
    margin-bottom: 2em;
    width: 20%;
  }

  .search-bar {
    font-size: 2.5vh;
    margin-bottom: 1em;
    width: 20%;
  }

  .analysis {
    font-size: 1em;
    width: 20%;
  }

</style>
