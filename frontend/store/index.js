import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export function createStore () {
  return new Vuex.Store({
    state: {
      user: null,
      loading: false,
      error: null,
    },

    actions: {
      // Register user
      register({commit}, payload){
        commit('setLoading', true);
        commit('clearError');
        // Register User
        commit('setLoading', false);
        const user = {
          id: 'asdfasjdflas',
          email: payload.email
        }
        commit('setUser', user)
        commit('setError', 'Error Message')
      },
      // Login user
      login({commit}, payload){
        commit('setLoading', true);
        commit('clearError');
        // Register User
        commit('setLoading', false);
        const user = {
          id: 'asdfasjdflas',
          email: payload.email,
        }
        commit('setUser', user)
      },
    },

    mutations: {
      setUser(state, payload){
        state.user = payload;
        },
      setLoading (state, payload) {
        state.loading = payload
      },
      setError (state, payload) {
        state.error = payload
      },
      clearError (state, payload) {
        state.error = null
      }
    },

    getters: {
      user(state){
        return state.user;
      },
      authError (state) {
        return state.error
      },
      loading (state) {
        return state.loading
      }
    }
  })
}
