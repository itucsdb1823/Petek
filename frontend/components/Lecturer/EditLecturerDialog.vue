<template>
  <v-dialog persistent v-model="editLecturerDialog" max-width="590">
    <v-btn slot="activator" flat color="orange" align-end v-if="userIsAdmin">
      <v-icon right dark>edit</v-icon>
      Edit
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Edit Lecturer</v-card-title>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card>
            <v-card-text>
              <v-container>
                <form @submit.prevent="edit_lecturer">
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="name"
                        label="Name"
                        id="name"
                        v-model="lecturer.name"
                        type="text"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="email"
                        label="Email"
                        id="email"
                        v-model="lecturer.email"
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
              <v-btn class="default--text darken-1"
                     flat
                     @click="editLecturerDialog=false"
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
    props: ['lecturer'],
    data(){
      return {
        editLecturerDialog: false,
      }
    },
    computed: {
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true
      },
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      user(){
        return this.$store.getters.user
      },
    },
    methods: {
      onAgree(){
        this.$router.push('/lecturers')
        this.$store.dispatch('adminEditLecturer', this.lecturer)
      }
    },
  }
</script>

<style scoped>

</style>
