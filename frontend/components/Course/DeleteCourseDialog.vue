<template>
  <v-dialog persistent v-model="deleteCourseDialog" max-width="290">
    <v-btn slot="activator" flat color="red" align-end v-if="userIsAdmin">
      <v-icon right dark>delete</v-icon>
      Delete
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Delete Course</v-card-title>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-text>Do you really want to delete this course?</v-card-text>
          </v-flex>
        </v-layout>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-actions>
              <v-btn class="orange--text darken-1"
                     flat
                     @click="deleteCourseDialog=false"
              >Cancel</v-btn>
              <v-btn class="red--text darken-1" flat @click="onAgree">Yes</v-btn>
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
    name: "DeleteCourseDialog",
    data(){
      return {
        deleteCourseDialog: false
      }
    },
    computed: {
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
    methods: {
      onAgree(){
        this.$router.push('/admin/courses')
        this.$store.dispatch('deleteCourse', this.course.id)
      }
    },
  }
</script>

<style scoped>

</style>
