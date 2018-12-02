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
                  <!--Course ID Dropdown-->
                  <v-layout row justify-space-between align-center>
                    <v-flex sm4>
                      <v-select
                        :items="courses"
                        item-text="name"
                        item-value="id"
                        label="Course ID"
                        v-model="course_id"
                        required
                      ></v-select>
                    </v-flex>
                    <!--Course Codes Dropdown-->
                    <v-flex sm4>
                      <v-text-field
                        name="course_code"
                        label="Course Code"
                        id="course_code"
                        v-model="course_code"
                        type="number"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                    <!--English Checkbox Button-->
                    <v-flex sm2>
                      <v-checkbox
                        v-model="english"
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
                        v-model="lecturer"
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
                      v-model="term_id"
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
                        v-model="url"
                        type="text"
                        placeholder="ex: Google Drive Link"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout row>
                    <v-flex xs12>
                      <v-btn type="submit" color="success">
                        Create Note
                        <span slot="loader" class="custom-loader">
                          <v-icon light>cached</v-icon>
                        </span>
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </form>
              </v-container>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
  export default {
    components: {},
    data() {
      return {
        title: '',
        course_id: '',
        course_code: '',
        content: 'A',
        lecturer: '',
        term_id: '',
        url: '',
        english: false,
      }
    },
    methods: {
      create_note() {
        if(!this.formIsValid){
          this.$store.commit('setError', ['Please fill all fields!'])
          return;
        }

        const note = {
          title: this.title,
          course_id: this.course_id,
          content: this.content,
          course_code: this.course_code,
          lecturer: this.lecturer,
          term_id: this.term_id,
          url: this.url,
          english: this.english,
        }
        this.$store.dispatch('createNote', note)
      },
      formIsValid() {
        return this.title !== '' && this.course_id !== ''
          && this.course_code !== '' && this.lecturer !== ''
          && this.english !== ''
          && this.term_id !== '' && this.url !== '';
      },
    },
    computed: {
      terms(){
        return this.$store.getters.terms;
      },
      courses(){
        return this.$store.getters.courses;
      },
      noteUploaded(){
        return this.$store.getters.createNote
      }
    },
    created(){
      this.$store.dispatch('getTerms')
      this.$store.dispatch('getCourses')
    },
    updated(){
      if(this.$store.getters.user === null){
        this.$store.commit('setError', ['Please login to create note!'])
      }
    },
    watch: {
      noteUploaded(value){
        if(value === true){
          this.$store.commit('createNote', false)
          this.$router.push('/notes');
        }
      }
    }
  }
</script>

<style scoped>

</style>
