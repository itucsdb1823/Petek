<template>
  <v-dialog persistent v-model="editCourseDialog" max-width="290">
    <v-btn slot="activator" flat color="orange" align-end v-if="userIsAdmin">
      <v-icon right dark>edit</v-icon>
      Edit
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Edit Course</v-card-title>
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
                          v-model="course.name"
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
                     @click="editCourseDialog=false"
              >Cancel</v-btn>
              <v-btn class="red--text darken-1" flat @click="onAgree">Edit Course</v-btn>
            </v-card-actions>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    props: ['course'],
    data(){
      return {
        editCourseDialog: false
      }
    },
    name: "EditCourseDialog",
    methods:{
      onAgree(){
        this.$store.dispatch('editCourse', this.course)
        this.editCourseDialog = false
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
    }
  }
</script>

<style scoped>

</style>
