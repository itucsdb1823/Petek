import Vue from 'vue'
import Vuex from 'vuex'
import Auth from '../services/Auth'
import Note from '../services/Note'
import Lecturer from '../services/Lecturer'
import Term from '../services/Term'
import Course from '../services/Course'

Vue.use(Vuex)

const storeOptions = {
    state: {
      user: null,
      note: null,
      loading: false,
      error: null,
      store: "1",
      terms: [],
      courses: [],
      notes: [],
      deleteNote: false,
      editNote: false,
      createNote: false,
      createLecturer: false,
      deleteLecturer: false,
      editLecturer: false,
      lecturer: {},
      lecturers: []
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
      },

      createLecturer({commit}, payload){
        Lecturer.create(payload).then(result => {
          commit('createLecturer', true)
        }).catch(error => {
          commit('setError', ['yüklenemedi!'])
          console.log(error)
        })
      },

      getLecturers({commit}, payload){
        Lecturer.getLecturers().then(result => {
          console.log(result)
          commit('setLecturers', result.data.lecturers)
        }).catch(error => {
          console.log(error)
          commit('setError', ['could not get the lecturers.'])
        })
      },

      getLecturer({commit}, payload){
        Lecturer.getLecturer(payload).then(result => {
          commit('setLecturer', result.data.lecturer)
        }).catch(error => {
          commit('setError', error.errors)
        })
      },

      // Create Note
      createNote({commit}, payload){
        Note.create(payload).then(result => {
          commit('createNote', true)
        }).catch(error => {
          commit('setError', ['yüklenemedi'])
          console.log(error)
        })
      },

      getNotes({commit}, payload){
        Note.getNotes().then(result => {
          commit('setNotes', result.data.notes)
        }).catch(error => {
          console.log(error)
          commit('setError', ['An error has occured']);
        })
      },
      getNote({commit}, payload){
        Note.getNote(payload).then(result => {
          commit('setNote', result.data.note)
        }).catch(error => {
          commit('setError', error.errors)
        })
      },
      getTerms({commit}, payload){
        Term.getTerms().then(result => {
          commit('setTerms', result.data.terms)
        }).catch(error => {
          commit('setError', ['An error has occured'])
        })
      },
      getCourses({commit}, payload){
        Course.getCourses().then(result => {
          commit('setCourses', result.data.courses)
        }).catch(error => {
          commit('setError', ['An error has occured'])
        })
      },
      deleteNote({commit}, payload){
        Note.deleteNote(payload).then(result => {
          commit('deleteNote', true)
        }).catch(error => {
          commit('setError', error.errors)
        })
      },
      editNote({commit}, payload){
        Note.editNote(payload).then(result => {
          commit('editNote', true)
        }).catch(error => {
          commit('setError', error.errors)
        })
      }
    },
    // commit
    mutations: {
      createLecturer(state, payload){
        state.createLecturer = payload;
      },
      deleteLecturer(state, payload){
        state.deleteLecturer = payload;
      },
      editLecturer(state, payload){
        state.editLecturer = payload;
      },
      createNote(state, payload){
        state.createNote = payload;
      },
      deleteNote(state, payload){
        state.deleteNote = payload;
      },
      editNote(state, payload){
        state.editNote = payload;
      },
      setCourses(state, payload){
        state.courses = payload
      },
      setTerms(state, payload){
        state.terms = payload
      },
      setNotes(state, payload){
        state.notes = payload;
      },
      setNote(state, payload){
        state.note = payload;
      },
      setLecturers(state, payload){
        state.lecturers = payload;
      },
      setLecturer(state, payload){
        state.lecturer = payload;
      },
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
      createLecturer(state){
        return state.createLecturer
      },
      deleteLecturer(state){
        return state.deleteLecturer
      },
      editLecturer(state){
        return state.editLecturer
      },
      createNote(state){
        return state.createNote
      },
      deleteNote(state){
        return state.deleteNote
      },
      editNote(state){
        return state.editNote
      },
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
      },
      note(state){
        return state.note
      },
      terms(state){
        return state.terms
      },
      courses(state){
        return state.courses
      },
      lecturers(state){
        return state.lecturers
      },
      lecturer(state){
        return state.lecturer
      }
    }
}

export function createStore() {
    return new Vuex.Store(storeOptions)
}

export const clientStore = new Vuex.Store(storeOptions)
