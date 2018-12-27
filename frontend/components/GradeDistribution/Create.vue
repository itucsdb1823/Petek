<template>
  <v-dialog persistent v-model="addGradeDistributionDialog" max-width="590">
    <v-btn slot="activator" flat color="green" align-end v-if="userIsAuthenticated">
      <v-icon right dark>add</v-icon>
      Add Grade Distribution
    </v-btn>
    <v-card>
      <v-container>
      <v-layout row>
        <v-flex xs12>
          <v-card>
            <v-card-text>
              <v-container>
                <form @submit.prevent="create_grade_distribution">
                  <v-layout row justify-space-between align-center>
                    <v-flex sm12>
                      <v-select
                        :items="lecturers"
                        item-text="name"
                        item-value="id"
                        label="Lecturer"
                        v-model="lecturer_id"
                        required
                      ></v-select>
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

                  <v-layout row>
                    <v-flex xs12 sm6 offset-sm3>
                      <v-btn raised class="primary" @click="onPickFile">Upload Image</v-btn>
                      <input type="file" hidden ref="fileInput" accept="image/*" @change="onFilePicked">
                    </v-flex>
                  </v-layout>
                  <v-layout row>
                    <v-flex xs12 sm6 offset-sm3>
                      <img :src="imageURL" height="150"/>
                    </v-flex>
                  </v-layout>

                  <v-layout row>
                    <v-flex xs12>
                      <v-btn type="submit" color="success">
                        Create Grade Distribution
                        <span slot="loader" class="custom-loader">
                          <v-icon light>cached</v-icon>
                        </span>
                      </v-btn>
                      <v-btn @click="addGradeDistributionDialog=false" type="submit" color="red">
                        Close
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
    </v-card>
  </v-dialog>
</template>

<script>
    export default {
      props: ['lecturer'],
      name: "Create",
        data() {
        return {
          addGradeDistributionDialog: false,
          course_id: '',
          course_code: '',
          lecturer_id: '',
          term_id: '',
          english: false,
          image: '',
          imageURL: '',
        }
      },
      methods: {
        onPickFile(){
          this.$refs.fileInput.click();
        },
        onFilePicked(event){
          const files = event.target.files;
          let filename = files[0].name;
          if (filename.lastIndexOf('.') <= 0) {
            return alert('Please add a valid file!')
          }

          const fileReader = new FileReader();
          fileReader.addEventListener('load', () => {
            this.imageURL = fileReader.result;
          });
          fileReader.readAsDataURL(files[0]);
          this.image = files[0]
        },
        create_grade_distribution(){
          // if(!this.formIsValid){
          //  this.$store.commit('setError', ['Please fill all fields!'])
          //   return;
          // }

          const gradeDistribution = {
            course_id: this.course_id,
            course_code: this.course_code,
            lecturer_id: this.lecturer_id,
            term_id: this.term_id,
            english: this.english,
            image: this.image
          }


          this.$store.dispatch('createGradeDistribution', gradeDistribution)

          this.addGradeDistributionDialog = false
          this.$store.commit('setError', ['Image is loading, please wait'])
        }
      },
      formIsValid() {
        return this.course_id !== '' && this.course_code !== ''
          && this.lecturer_id !== '' && this.term_id !== '';
      },
      computed: {
        terms(){
          return this.$store.getters.terms;
        },
        courses(){
          return this.$store.getters.courses;
        },
        lecturers(){
          return this.$store.getters.lecturers;
        },
        gradeDistributionUploaded(){
          return this.$store.getters.postRequest
        },
        userIsAuthenticated(){
          return this.user !== null && this.user !== undefined;
        },
        user(){
          return this.$store.getters.user
        },
        gradeAdded(){
          return this.$store.getters.gradeAdded
        }
      },
      created(){
        this.$store.dispatch('getTerms')
        this.$store.dispatch('getCourses')
        this.$store.dispatch('getLecturers')
      },
      updated(){
        if(this.$store.getters.user === null){
          this.$store.commit('setError', ['Please login to create note!'])
        }
        this.lecturer_id = this.lecturer.id
      },
      watch: {
        gradeDistributionUploaded(value){
          if(value === true){
            this.$store.commit('postRequest', null)
            this.addGradeDistributionDialog = false
          }
        },
        gradeAdded(value){
          if(value === true){
            this.addGradeDistributionDialog = false;
            // location.reload();
          }
        }
      }
    }
</script>

<style scoped>

</style>
