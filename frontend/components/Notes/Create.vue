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
                                        >
                                        </v-text-field>
                                    </v-flex>
                                </v-layout>
                              <!--Course ID Dropdown-->
                              <v-layout row justify-space-between align-center>
                                <v-flex sm4>
                                  <v-select
                                    :items="courseIDs"
                                    menu-props="auto"
                                    label="Course ID"
                                    v-model="courseID"
                                  ></v-select>
                                </v-flex>
                              <!--Course Codes Dropdown-->
                                <v-flex sm4>
                                  <v-select
                                    :items="courseCodes"
                                    menu-props="auto"
                                    label="Course Code"
                                    v-model="courseCode"
                                  ></v-select>
                                </v-flex>
                              <!--English Checkbox Button-->
                                <v-flex sm2>
                                <input type="checkbox" id="eng" v-model="English">
                                <label for="eng">English?</label>
                                </v-flex>
                              </v-layout>
                              <!--Lecturers Dropdown-->
                                <v-flex xs12>
                                  <v-select
                                    :items="lecturers"
                                    menu-props="auto"
                                    label="Lecturer"
                                    v-model="lecturer"
                                  ></v-select>
                                </v-flex>
                              <!--Terms Dropdown-->
                                <v-flex xs6>
                                  <v-select
                                    :items="terms"
                                    v-model="term"
                                    menu-props="auto"
                                    label="Terms"
                                    single-line
                                  ></v-select>
                                </v-flex>
                                <!--Course URL Input Field-->
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="url"
                                                label="Course URL (ex: Google Drive Link)"
                                                id="url"
                                                v-model="url"
                                                type="text"
                                        >
                                        </v-text-field>
                                    </v-flex>
                                </v-layout>
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-btn type="submit">
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
        courseIDs: ["ATA", "MAT", "TUR"],
        courseCodes: ["101", "102", "103"],
        lecturers: ["Turgut Uyar", "Hayri Turgut Uyar", "HTU"],
        courseID:"ATA",
        courseCode:"101",
        lecturer:"Turgut Uyar",
        term:"17/18",
        url: '',
        English: false,
        date: '',
        sharer: ''
      }
    },
    methods: {
      create_note() {
        const note = {
          title: this.title,
          courseID: this.courseID,
          courseCode: this.courseCode,
          lecturer: this.lecturer,
          term: this.term,
          url: this.url,
          english: this.English,
          date: this.date,
          sharer: this.sharer
        }
        this.$store.dispatch('createNote', note)
      },
    },
    computed: {
        terms(){
            return this.$store.getters.terms;
        }
    }
  }
</script>

<style scoped>

</style>
