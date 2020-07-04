<template>
  <div id="app">
    <ki-title class="title"></ki-title>
    <div class="search-content">
      <search-bar class="search-bar" @search="performAnalysis($event)"></search-bar>
      <spinner class="spinner" v-if="waitingForServer" />
      <span class="info" v-else-if="analysisError">{{ analysisError }}</span>
      <template v-else-if="analysisData">
        <span class="info">{{ analysisTime }}</span>
        <span class="info" v-for="warning of analysisData.warnings" :key="warning">
          {{ warning }}
        </span>
        <word-analysis class="analysis" :data="analysisData"></word-analysis>
      </template>
      <usage-text class="info" v-else />
    </div>
    <credit-text class="info" />
  </div>
</template>

<script>
import KiTitle from './components/KiTitle.vue';
import SearchBar from './components/SearchBar.vue';
import WordAnalysis from './components/WordAnalysis.vue';
import Spinner from './components/Spinner.vue';
import UsageText from './components/UsageText.vue';
import CreditText from './components/CreditText.vue';

export default {
  name: 'App',
  components: {
    KiTitle,
    SearchBar,
    WordAnalysis,
    Spinner,
    UsageText,
    CreditText
  },
  data() {
    return {
      analysisData: null,
      waitingForServer: false,
      analysisError: null
    };
  },
  computed: {
    analysisTime: function() {
      const timeUsed = this.analysisData?.time;

      const trunctuatedTime = parseFloat(timeUsed.toFixed(4));

      return `Analysis took ${trunctuatedTime}s`;
    }
  },
  methods: {
    startWaiting() {
        this.waitTimeout = setTimeout(() => this.waitingForServer = true, 600);
    },
    stopWaiting() {
        clearTimeout(this.waitTimeout);
        this.waitingForServer = false;
    },
    async performAnalysis(input) {
      try {
        this.analysisError = null;
        this.startWaiting();

        const response = await fetch(`/analyse_word/${input}`)
        const json = await response.json();

        this.stopWaiting();

        if (json.error) {
          this.analysisError = json.error;
          return;
        }

        this.analysisData = json;
      } catch (ex) {
        this.stopWaiting();
        this.analysisError = 'The server could not be reached';
        console.error(ex);
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
    min-height: 78vh;
  }

  .title {
    font-size: 2em;
    margin-bottom: 2em;
  }

  .search-bar {
    font-size: 1.5em;
    margin-bottom: 1em;
  }

  .analysis {
    font-size: 1em;
    margin-left: 1.75em;
    overflow-wrap: break-word;
  }

  .search-content {
    width: min(30em, 90%);
    flex-grow: 1;
  }

  .spinner {
    width: 60px;
    margin: auto;
  }

  .info {
    display: block;
    color: gray;
    font-size: 0.7em;
    text-align: center;
  }
</style>
