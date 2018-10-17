import Vue from 'vue'
import Vuex from 'vuex'
import Auth from '../services/Auth'

Vue.use(Vuex)

export function createStore () {
  return new Vuex.Store({
    state: {
      user: null,
      token: null,
      email: null,
      loading: false,
      error: null,
    },

    actions: {
      register({commit}, payload){
        commit('setLoading', true)
        commit('clearError')
        const user = {
          email: payload.email,
          name: payload.name,
          password: payload.password
        }

        Auth.register(user)
          .then((data) => {
            commit('setUser', data)
        }).catch((error) => {
          console.log(error)
          commit('setError', 'Error Message')
        })
        commit('setLoading', false)
      },

      // Login user
      login({commit}, payload){
        commit('setLoading', true)
        commit('clearError')

        const user = {
          email: payload.email,
          password: payload.password
        }

        Auth.login(user).then(data => {
          commit('setUser', data)
        }).catch(error => {
          console.log(error)
        })
      },

      // Logout
      logout({commit}) {
        commit('setUser', null)
      }
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
