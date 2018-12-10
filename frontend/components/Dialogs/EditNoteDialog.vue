<template>
  <v-dialog persistent v-model="editNoteDialog" max-width="590">
    <v-btn slot="activator" flat color="orange" align-end v-if="userIsOwner || userIsAdmin">
      <v-icon right dark>edit</v-icon>
      Edit
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Edit Note</v-card-title>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card>
            <v-card-text>
              <v-container>
                <form @submit.prevent="edit_note">
                  <!--Title Input Field-->
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="title"
                        label="Title"
                        id="title"
                        v-model="note.title"
                        type="text"
                        placeholder="Ata 101 Çıkmış Sorular"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <!--Course ID Dropdown-->
                  <v-layout row justify-space-between align-center>
                    <v-flex sm4>
                      <v-select
                        :items="courses"
                        item-text="name"
                        item-value="id"
                        label="Course ID"
                        v-model="note.course_id"
                        required
                      ></v-select>
                    </v-flex>
                    <!--Course Codes Dropdown-->
                    <v-flex sm4>
                      <v-text-field
                        name="course_code"
                        label="Course Code"
                        id="course_code"
                        v-model="note.course_code"
                        type="number"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                    <!--English Checkbox Button-->
                    <v-flex sm2>
                      <v-checkbox
                        v-model="note.english"
                        label="English?"
                      ></v-checkbox>
                    </v-flex>
                  </v-layout>
                  <!--Lecturers Dropdown-->
                  <v-flex xs12>
                    <v-text-field
                        name="lecturer"
                        label="Lecturer"
                        id="lecturer"
                        v-model="note.lecturer"
                        type="text"
                        placeholder="ex. Sanem Kabadayı"
                        required
                      >
                      </v-text-field>
                  </v-flex>
                  <!--Terms Dropdown-->
                  <v-flex xs6>
                    <v-select
                      :items="terms"
                      v-model="note.term_id"
                      menu-props="auto"
                      label="Terms"
                      item-value="id"
                      single-line
                      required
                    >
                      <template slot="selection" slot-scope="data">
                        {{ data.item.term_year }} - {{ data.item.season }}
                      </template>
                      <template slot="item" slot-scope="data">
                        {{ data.item.term_year }} - {{ data.item.season }}
                      </template>
                    </v-select>
                  </v-flex>
                  <!--Course URL Input Field-->
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="url"
                        label="Course URL"
                        id="url"
                        v-model="note.link"
                        type="text"
                        placeholder="ex: Google Drive Link"
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
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-actions>
              <v-btn class="default--text darken-1"
                     flat
                     @click="editNoteDialog=false"
              >Cancel</v-btn>
              <v-btn class="orange--text darken-1" flat @click="onAgree">Update</v-btn>
            </v-card-actions>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    props: ['note'],
    data(){
      return {
        editNoteDialog: false,
      }
    },
    computed: {
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true
      },
      userIsOwner () {
        return this.userIsAuthenticated && this.note.user_id === this.user.id
      },
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      user(){
        return this.$store.getters.user
      },
      noteEdited(){
        return this.$store.getters.postRequest
      },
      terms(){
        return this.$store.getters.terms;
      },
      courses(){
        return this.$store.getters.courses;
      },
    },
    methods: {
      onAgree(){
        if(this.userIsAdmin){
          this.$store.dispatch('adminEditNote', this.note)
        }else{
          this.$store.dispatch('editNote', this.note)
        }
        this.editNoteDialog = false
      }
    },
    watch: {
      noteEdited(value){
        if(value === true){
          this.editNoteDialog = false
          this.$router.push('/notes/' + this.note.slug)
          this.$store.commit('postRequest', null)
        }else if(value === false){
          this.$store.commit('postRequest', null)
        }
      }
    },
    created() {
      this.$store.dispatch('getTerms')
      this.$store.dispatch('getCourses')
    }
  }
</script>

<style scoped>

</style>
