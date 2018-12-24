Frontend Guide for Developer
===============

On the frontend directory run::

   npm run dev

command to start the client side of the project.

Vue JS
------

In this project, we used Vue_.js framework to build the frontend side. You can get more information about this framework using this_ link.

.. _Vue: https://vuejs.org/
.. _this: https://vuejs.org/

If we look at to core of the Vue JS::

    <div id="app">
        {{ message }}
    </div>

::

    var app = new Vue({
      el: '#app',
      data: {
        message: 'Hello Vue!'
      }
    })

::

    Hello Vue!


We can assign if statement using **v-if**::

    <div id="app-3">
      <span v-if="seen">Now you see me</span>
    </div>

::

    var app3 = new Vue({
      el: '#app-3',
      data: {
        seen: true
      }
    })

::

    Now you see me


Similarly, to run for loop::

    <div v-for="item in items">
        {{ item }} <br>
    </div>

::

    var app4 = new Vue({
        data: {
            items: ['item1', 'item2']
        }
    })

::

    item1
    item2


Vuetify
-------
Vuetify_ is a material component framework for VueJS. Since Vuetify follows the material design standard, it allows you to create good looking applications.

Here is some code samples from vuetify::

  <template>
    <v-container>
      <v-layout row>
        <v-flex xs12 sm6 offset-sm3>
          <v-card>
            <v-card-text>
              <v-container>
                <form @submit.prevent="create_note">
                  <!--Title Input Field-->
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="title"
                        label="Title"
                        id="title"
                        v-model="title"
                        type="text"
                        placeholder="Ata 101 Çıkmış Sorular"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                </form>
              </v-container>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container
  </template>


In here, it creates a responsive NoteCreate form. *You can find this code in this* Link_. For example, **v-layout** tag is used for `<div class="row">` tag.

.. _Link: https://github.com/itucsdb1823/itucsdb1823/blob/master/frontend/components/Notes/Create.vue

To give a column, we can use **v-flex** tag.

For more information, you can visit official documentation page_

.. _page: https://vuetifyjs.com/en/
.. _Vuetify: https://vuetifyjs.com/en/


Routes
------

We have implemented our routes in frontend/router/index.js file_

.. _file: https://github.com/itucsdb1823/itucsdb1823/blob/master/frontend/router/index.js

For example, when **/login** route is fired, it runs the **Login** component::

    {
      path: '/login',
      name: 'Login',
      component: Login
    },

Login component is defined in **/frontend/components/User/Login.vue** directory. You can also see the import code of it::

    import Login from '../components/User/Login.vue'


Components
----------

In **/components/** folder, we have several components such as `Login`, `Register`, `Note` etc. Each components has three sections:

* Template
* Script
* Style

Template
"""""""""

Between **template** tags, we run our **HTML** codes. Since we use **Vuetify**, we did not write too much HTML codes. Instead, we used Vuetify styled tags. For example::

    <template>
        <v-btn @click="some_method" class="some_class">
            Click Me
        </v-btn>
    </template>

Script
"""""""""

Between **script** tags, we can write our JavaScript codes such as::

    <script>
        export default {
            methods: {
                some_method(){
                    console.log('You clicked me');
                }
            }
        }
    </script>

Style
"""""""""

Between **style** tags, we can write our own css such as::

    <style scoped>
        .some_class{
            font-size: 23px;
        }
    </style>

Services
--------

To communicate with API, we used some services which are located under the **services** folder. For example, to get the notes from backend we can run this command::

    import Api from '../Api'
    export default {
      getNotes(){
        return Api().get('notes')
      },
    }

It will send a request to **http://backend_url/api/notes** endpoint and will return a response. To make requests, we used Axios.

To make get request::

    Api().get('url')

To make post request::

    Api().post('url', data)


Axios
-----

Axios is the Javascript library allows you to make HTTP requests. We have created main Api.js file in **/services** folder. All services communicates with this file.::

    import axios from 'axios'
    export default () => {
        return axios.create({
            baseURL: 'http://localhost:5000/api',
        })
    }


Vuex
-----

We also used state management system which is Vuex. In **store/index.js** file, we created our functions to communicate with the services. This functions are called from components.

For example, inside of the Notes/Note.vue file, we are fetching the note from the backend::

    beforeCreate(){
      let note_slug = this.$route.params.note_slug
      this.$store.dispatch('getNote', note_slug)
    },

When we dispatch the getNote function, its called from actions object in the **store/index.js** file::

    import Note from '../services/Note'

    const storeOptions = {
        state: {
            note: null
        }
        actions: {
            getNote(){
                Note.getNote(payload).then(result => {
                  commit('setNote', result.data.notes)
                  commit('getRequest', true)
                }).catch(error => {
                  commit('getRequest', false)
                  commit('setError', error.response.data.errors)
                })
            }
        }
    }

After getting the note, we are setting the state.note variable with `commit('setNote')` command: ::

    setNote(state, payload){
      state.note = payload;
    }

In that way, we will be able to reach the note variable from the Note component with::

    computed: {
      note(){
        return this.$store.getters.note // state.note
      },
    }


