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


Routes
------

Components
----------

Services
--------

Axios
-----

Vuex
-----
