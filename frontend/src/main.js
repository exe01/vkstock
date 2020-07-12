/* eslint-disable no-param-reassign */
import axios from 'axios';
import Vue from 'vue';
import Vuetify from 'vuetify';
import App from './App.vue';
import router from './router';
import store from './store';
// import './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import 'font-awesome/css/font-awesome.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import 'vuetify/dist/vuetify.min.css'; // Ensure you are using css-loader

Vue.config.productionTip = false;

axios.defaults.baseURL = 'http://localhost:8000/';
// axios.defaults.params = {};
// axios.defaults.params.api_url = axios.defaults.baseURL;
axios.interceptors.request.use((config) => {
  config.params = config.params || {};
  config.params.media_url = `${axios.defaults.baseURL}media`;
  return config;
});

Vue.prototype.$axios = axios;

Vue.use(Vuetify);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
