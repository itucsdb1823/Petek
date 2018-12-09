import Vue from 'vue'
import Vuex from 'vuex'
import Auth from '../services/Auth'
import Note from '../services/Note'
import Lecturer from '../services/Lecturer'
import Term from '../services/Term'
import Course from '../services/Course'
import GradeDistribution from '../services/GradeDistribution'
import LecturerComment from '../services/LecturerComment'
import NoteComment from '../services/NoteComment'

Vue.use(Vuex)

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

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
      lecturer: {},
      lecturers: [],
      gradeDistributions: [],
      gradeDistribution: {},
      /*
      If request is null, no request is sent recently.
      If request is true, post request sent and returned success recently.
      If request is false, post request sent and returned error recently.
       */
      getRequest: null,
      postRequest: null,
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
            commit('setUser', result.data.user)
            commit('postRequest', true)
        }).catch((error) => {
          commit('setError', error.response.data.errors)
          commit('postRequest', false)
        })
      },

      // Login user
      login({commit}, payload){
        const user = {
          email: payload.email,
          password: payload.password
        }

        Auth.login(user).then(result => {
          commit('setUser', result.data.user)
          commit('postRequest', true)
          console.log('as')
        }).catch(error => {
          console.log(error.response.data.errors)
          commit('setError', error.response.data.errors)
          commit('postRequest', false)
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
          commit('postRequest', true)
        }).catch(error => {
          commit('setError', error.response.data.errors)
          console.log(error)
          commit('postRequest', false)
        })
      },

      getLecturers({commit}, payload){
        Lecturer.getLecturers().then(result => {
          commit('setLecturers', result.data.lecturers)
          commit('getRequest', true)
        }).catch(error => {
          commit('setError', ['could not get the lecturers.'])
          commit('getRequest', false)
        })
      },

      getLecturer({commit}, payload){
        Lecturer.getLecturer(payload).then(result => {
          commit('setLecturer', result.data.lecturer)
        }).catch(error => {
          commit('setError', error.response.data.errors)
        })
      },

      createGradeDistribution({commit}, payload){
        let file = payload.image;
        getBase64(file).then(
          data => {
            payload.image = data;
            console.log(payload.image)
            GradeDistribution.createGradeDistribution(payload)
              .then(result => {
                commit('postRequest', true)
              }).catch(error => {
                commit('postRequest', false)
                commit('setError', error.response.data.errors)
            });
          }
        )
          .catch(error => {
            commit('setError', ['Could not encode the image!'])
          });
      },

      addLecturerComment({commit}, payload){
        if(payload.comment === ''){
          commit('setError', ['Please fill all fields!'])
          return;
        }

        LecturerComment.create(payload.type_id, payload)
          .then(result => {
            let comment = {
              comment: result.data.comment,
              user: {
                id: this.getters.user.id
              }
            }
            console.log(comment)
            commit('postRequest', true)
            commit('appendLecturerComment', comment)
          })
          .catch(error => {
            commit('postRequest', false)
            commit('setError', error.response.data.errors)
          })
      },

      addNoteComment({commit}, payload){
        if(payload.comment === ''){
          commit('setError', ['Please fill all fields!'])
          return;
        }

        NoteComment.create(payload.type_id, payload)
          .then(result => {
            let comment = {
              comment: result.data.comment,
              user: {
                name: this.getters.user.name,
                slug: this.getters.user.slug,
                id: this.getters.user.id
              }
            }
            console.log(comment)
            commit('postRequest', true)
            commit('appendNoteComment', comment)
          })
          .catch(error => {
            commit('postRequest', false)
            commit('setError', error.response.data.errors)
          })
      },

      deleteNoteComment({commit}, payload){
        NoteComment.delete(payload.note_id, payload.comment_id)
          .then(result => {
            commit('postRequest', true)
            commit('deleteNoteComment', payload.comment_index)
          }).catch(error => {
            commit('postRequest', false)
            commit('setError', error.response.data.errors)
        })
      },

      deleteLecturerComment({commit}, payload){
        LecturerComment.delete(payload.lecturer_id, payload.comment_id)
          .then(result => {
            commit('postRequest', true)
            commit('deleteLecturerComment', payload.comment_index)
          }).catch(error => {
            commit('postRequest', false)
            commit('setError', error.response.data.errors)
        })
      },

      // Create Note
      createNote({commit}, payload){
        if(payload.course_id === '' || payload.term_id === ''){
          commit('setError', ['Please fill all fields!'])
          return;
        }

        Note.create(payload).then(result => {
          commit('postRequest', true)
        }).catch(error => {
          commit('setError', error.response.data.errors)
          commit('postRequest', false)
        })
      },

      getNotes({commit}, payload){
        Note.getNotes().then(result => {
          commit('setNotes', result.data.notes)
          commit('getRequest', true)
        }).catch(error => {
          commit('getRequest', false)
          commit('setError', error.response.data.errors);
        })
      },
      getNote({commit}, payload){
        Note.getNote(payload).then(result => {
          commit('setNote', result.data.notes)
          commit('getRequest', true)
        }).catch(error => {
          commit('getRequest', false)
          commit('setError', error.response.data.errors)
        })
      },
      getTerms({commit}, payload){
        Term.getTerms().then(result => {
          commit('setTerms', result.data.terms)
          commit('getRequest', true)
        }).catch(error => {
          commit('getRequest', false)
          commit('setError', error.response.data.errors)
        })
      },
      getCourses({commit}, payload){
        Course.getCourses().then(result => {
          commit('setCourses', result.data.courses)
          commit('getRequest', true)
        }).catch(error => {
          commit('getRequest', false)
          commit('setError', error.response.data.errors)
        })
      },
      deleteNote({commit}, payload){
        Note.deleteNote(payload).then(result => {
          commit('postRequest', true)
        }).catch(error => {
          commit('postRequest', false)
          commit('setError', error.response.data.errors)
        })
      },
      editNote({commit}, payload){
        Note.editNote(payload).then(result => {
          commit('postRequest', true)
        }).catch(error => {
          commit('postRequest', false)
          commit('setError', error.response.data.errors)
        })
      }
    },
    // commit
    mutations: {
      appendNoteComment(state, payload){
        state.note.comments.unshift(payload)
      },
      deleteNoteComment(state, payload){
        state.note.comments.splice(payload, 1)
      },
      appendLecturerComment(state, payload){
        state.lecturer.comments.unshift(payload)
      },
      deleteLecturerComment(state, payload){
        state.lecturer.comments.splice(payload, 1)
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
		  },
      getRequest(state, payload){
        state.getRequest = payload
      },
      postRequest(state, payload){
        state.postRequest = payload
      }
    },
    getters: {
      getRequest(state){
        return state.getRequest
      },
      postRequest(state){
        return state.postRequest
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
