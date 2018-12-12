import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/User/Login.vue'
import Register from '../components/User/Register.vue'
import Notes from '../components/Notes/Notes.vue'
import Lecturers from '../components/Lecturer/Lecturers.vue'
import Lecturer from '../components/Lecturer/Lecturer.vue'
import LecturerCreate from '../components/Lecturer/Create.vue'
import Note from '../components/Notes/Note.vue'
import NoteCreate from '../components/Notes/Create.vue'
import Users from '../components/User/Users'
import User from '../components/User/User'
import Event from '../components/Events/Event'
import Events from '../components/Events/Events'
import EventCreate from '../components/Events/Create'
import Courses from '../components/Course/Courses'
import Terms from '../components/Term/Terms'

// The meta data for your routes
const meta = require('./meta.json')

// Function to create routes
// Is default lazy but can be changed
function route (path, view) {
  return {
    path: path,
    meta: meta[path],
    component: resolve => import(`pages/${view}View.vue`).then(resolve)
  }
}

Vue.use(Router)

export function createRouter () {
    const router = new Router({
      base: __dirname,
      mode: 'history',
      scrollBehavior: () => ({ y: 0 }),
      routes: [
        route('/', 'Welcome'),
        route('/inspire', 'Inspire'),
        // Global redirect for 404
        { path: '*', redirect: '/' },
        {
          path: '/register',
          name: 'Register',
          component: Register
        },
        {
          path: '/login',
          name: 'Login',
          component: Login
        },
        {
          path: '/notes',
          name: 'Notes',
          component: Notes
        },
        {
          path: '/notes/create',
          name: 'NoteCreate',
          component: NoteCreate
        },
        {
          path: '/notes/:note_slug',
          name: 'Note',
          component: Note
        },
        {
          path: '/events',
          name: 'Events',
          component: Events
        },
        {
          path: '/events/create',
          name: 'EventCreate',
          component: EventCreate
        },
        {
          path: '/events/:event_id',
          name: 'Event',
          component: Event
        },
        {
          path: '/lecturers/create',
          name: 'LecturerCreate',
          component: LecturerCreate
        },
        {
          path: '/lecturers',
          name: 'Lecturers',
          component: Lecturers
        },
        {
          path: '/lecturers/:lecturer_slug',
          name: 'Lecturer',
          component: Lecturer
        },
        {
          path: '/admin/users',
          name: 'Users',
          component: Users
        },
        {
          path: '/users/:user_slug',
          name: 'User',
          component: User
        },
        {
          path: '/admin/courses',
          name: 'Courses',
          component: Courses
        },
        {
          path: '/admin/terms',
          name: 'Terms',
          component: Terms
        }
      ]
    })

    // Send a pageview to Google Analytics
    router.beforeEach((to, from, next) => {
      if (typeof ga !== 'undefined') {
        ga('set', 'page', to.path)
        ga('send', 'pageview')
      }
      next()
    })

    return router
}
