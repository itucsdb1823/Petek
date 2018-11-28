import Vue from 'vue'
import {
  Vuetify,
  VApp,
  VNavigationDrawer,
  VFooter,
  VList,
  VBtn,
  VIcon,
  VGrid,
  VToolbar,
  VCard,
  transitions, VTextField, VAlert, VDataTable, VSelect, VCheckbox, VDivider, VDialog
} from 'vuetify'
import '../node_modules/vuetify/src/stylus/app.styl'
import App from './App.vue'
import Components from 'components/_index'
import AlertComp from '../components/Shared/Alert'
import Meta from 'vue-meta'
// import DataTable from 'v-data-table'

import { createStore, clientStore } from 'store/index'
import { createRouter } from 'router/index'
import { sync } from 'vuex-router-sync'

Vue.use(Vuetify, {
  components: {
    VApp,
    VNavigationDrawer,
    VFooter,
    VList,
    VBtn,
    VIcon,
    VGrid,
    VToolbar,
    VCard,
    transitions,
    VAlert,
    VTextField,
    VDataTable,
    VSelect,
    VCheckbox,
    VDivider,
    VDialog
  },
  theme: {
    primary: '#ee44aa',
    secondary: '#424242',
    accent: '#82B1FF',
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107'
  }
})

Vue.use(Meta)

Vue.component('app-alert', AlertComp);

Object.keys(Components).forEach(key => {
  Vue.component(key, Components[key])
})

// Expose a factory function that creates a fresh set of store, router,
// app instances on each call (which is called for each SSR request)
export function createApp (ssrContext) {
  // create store and router instances
  const router = createRouter()
  let store
  if (process.env.VUE_ENV === 'server') {
    store = createStore()
  } else {
    store = clientStore
  }

  // sync the router with the vuex store.
  // this registers `store.state.route`
  sync(store, router)

  // create the app instance.
  // here we inject the router, store and ssr context to all child components,
  // making them available everywhere as `this.$router` and `this.$store`.
  const app = new Vue({
    router,
    store,
    ssrContext,
    render: h => h(App),
    mounted() {
		  this.$store.commit('initialiseStore');
	  }
  })

  // expose the app, the router and the store.
  // note we are not mounting the app here, since bootstrapping will be
  // different depending on whether we are in a browser or on the server.
  return { app, router, store }
}
