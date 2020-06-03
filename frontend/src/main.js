import Vue from 'vue';
import App from './App.vue';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faSearch, faLandmark, faComment, faPen } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faSearch);
library.add(faLandmark);
library.add(faComment);
library.add(faPen);

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app');
