<template>
  <v-dialog persistent v-model="editUserDialog" max-width="590">
    <v-btn slot="activator" flat color="orange" align-end v-if="userIsOwner || userIsAdmin">
      <v-icon right dark>edit</v-icon>
      Edit
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Edit User</v-card-title>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card>
            <v-card-text>
              <v-container>
                <form @submit.prevent="edit__user">
                  <!--Title Input Field-->
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="name"
                        label="Name"
                        id="title"
                        v-model="updatedUser.name"
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
                        v-model="updatedUser.email"
                        type="text"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout row v-if="!(userIsAdmin && !userIsOwner)">
                    <v-flex xs12>
                      <v-text-field
                        name="password"
                        label="Password"
                        id="password"
                        v-model="updatedUser.password"
                        type="password"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout row v-if="!(userIsAdmin && !userIsOwner)">
                    <v-flex xs12>
                      <v-text-field
                        name="passwordConfirmation"
                        label="Password Confirm"
                        id="passwordConfirmation"
                        v-model="updatedUser.passwordConfirm"
                        type="password"
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
                     @click="editUserDialog=false"
              >Cancel</v-btn>
              <v-btn class="orange--text darken-1" flat @click="edit__user">Update</v-btn>
            </v-card-actions>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    props: ['_user'],
    data(){
      return {
        editUserDialog: false,
        updatedUser: {
          'name': '',
          'password': '',
          'passwordConfirm': '',
          'email': ''
        }
      }
    },
    mounted(){
      this.updatedUser.name = this._user.name;
      this.updatedUser.email = this._user.email;
    },
    computed: {
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true
      },
      userIsOwner () {
        return this._user &&  this.userIsAuthenticated && this._user.id === this.user.id
      },
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      user(){
        return this.$store.getters.user
      },
    },
    methods: {
      edit__user(){
        if(this.userIsAdmin){
          this.$store.dispatch('adminEditUser', {
            'id': this._user.id,
            'name': this.updatedUser.name,
            'email': this.updatedUser.email,
          })
        }else{
          this.updatedUser.id = this._user.id
          this.$store.dispatch('editUser', this.updatedUser)
        }

        this.editUserDialog = false
      }
    },
  }
</script>

<style scoped>

</style>
