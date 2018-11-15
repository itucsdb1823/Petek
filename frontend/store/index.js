import Vue from 'vue'
import Vuex from 'vuex'
import Auth from '../services/Auth'

Vue.use(Vuex)

const storeOptions = {
    state: {
      user: null,
      loading: false,
      error: null,
      store: "1",
      notes: [
        {
          id: 1,
          title: 'Title 1',
          content: 'Content 1',
          course: 'BLG 231',
          lecturer: 'Turgut Uyar',
          term: '18/19 Güz',
          user_id: 1,
          date: '06/11/2018',
        },
        {
          id: 2,
          title: 'Title 2',
          content: 'Content 2',
          course: 'BLG 222',
          lecturer: 'Turgut Uyar',
          term: '18/19 Güz',
          user_id: 1,
          date: '06/11/2018',
        },
        {
          id: 1,
          title: 'Title 1',
          content: 'Content 1',
          course: 'BLG 231',
          lecturer: 'Turgut Uyar',
          term: '18/19 Güz',
          user_id: 1,
          date: '06/11/2018',
        },
        {
          id: 2,
          title: 'Title 2',
          content: 'Content 2',
          course: 'BLG 222',
          lecturer: 'Turgut Uyar',
          term: '18/19 Güz',
          user_id: 1,
          date: '06/11/2018',
        },
        {
          id: 1,
          title: 'Title 1',
          content: 'Content 1',
          course: 'BLG 231',
          lecturer: 'Turgut Uyar',
          term: '18/19 Güz',
          user_id: 1,
          date: '06/11/2018',
        },
        {
          id: 2,
          title: 'Title 2',
          content: 'Content 2',
          course: 'BLG 222',
          lecturer: 'Turgut Uyar',
          term: '18/19 Güz',
          user_id: 1,
          date: '06/11/2018',
        }
      ]
    },
    // dispatch
    actions: {
      register({commit}, payload){
        const user = {
          email: payload.email,
          name: payload.name,
          password: payload.password,
          passwordConfirm: payload.passwordConfirm
        }

        Auth.register(user)
          .then((result) => {
            commit('setUser', result.data)
        }).catch((error) => {
          commit('setError', error.response.data.errors)
        })
      },

      // Login user
      login({commit}, payload){
        const user = {
          email: payload.email,
          password: payload.password
        }

        Auth.login(user).then(result => {
          commit('setUser', result.data)
        }).catch(error => {
          commit('setError', error.response.data.errors)
        })
      },
      // Logout
      logout({commit}){
        commit('setUser', null)
        localStorage.setItem('user', null);
      },
      clearError({commit}){
        commit('clearError')
      },
      setError({commit}, payload){
        commit('setError', payload)
      }
    },
    // commit
    mutations: {
      setUser(state, payload){
        state.user = payload;
        localStorage.setItem('user', JSON.stringify(state.user));
      },
      setLoading(state, payload){
        state.loading = payload
      },
      setError(state, payload){
        state.error = payload
      },
      clearError(state){
        state.error = null
      },
      initialiseStore() {
        if(process.browser){
          if(localStorage.getItem('user')) {
            this.state.user = JSON.parse(localStorage.getItem('user'))
          }
        }
		  }
    },
    getters: {
      user(state){
        return state.user
      },
      error(state){
        return state.error
      },
      loading(state){
        return state.loading
      },
      notes(state){
        return state.notes
      }
    }
}

export function createStore() {
    return new Vuex.Store(storeOptions)
}

export const clientStore = new Vuex.Store(storeOptions)
