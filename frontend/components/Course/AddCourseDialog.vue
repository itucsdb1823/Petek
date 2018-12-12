<template>
  <v-dialog persistent v-model="addCourseDialogg" max-width="290">
    <v-btn slot="activator" flat color="green" align-end v-if="userIsAdmin">
      <v-icon center dark>new</v-icon>
      Add Course
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Add Course</v-card-title>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card>
              <v-card-text>
                <v-container>
                  <form @submit.prevent="onAgree">
                    <!--Title Input Field-->
                    <v-layout row>
                      <v-flex xs12>
                        <v-text-field
                          name="course"
                          label="Course"
                          id="course"
                          v-model="course"
                          type="text"
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
              <v-btn class="orange--text darken-1"
                     flat
                     @click="addCourseDialogg=false"
              >Cancel</v-btn>
              <v-btn class="red--text darken-1" flat @click="onAgree">Add Course</v-btn>
            </v-card-actions>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    data(){
      return {
        course: '',
        addCourseDialogg: false
      }
    },
    name: "AddCourseDialog",
    methods:{
      onAgree(){
        this.$store.dispatch('addCourse', this.course)
        this.addCourseDialogg = false
      }
    },
    computed:{
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      user(){
        return this.$store.getters.user
      },
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true
      }
    },
  }
</script>

<style scoped>

</style>
