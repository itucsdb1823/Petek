<template>
  <v-dialog persistent v-model="deleteUserDialog" max-width="290">
    <v-btn slot="activator" flat color="red" align-end v-if="userIsOwner || userIsAdmin">
      <v-icon right dark>delete</v-icon>
      Delete
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Delete User</v-card-title>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-text>Do you really want to delete this user?</v-card-text>
          </v-flex>
        </v-layout>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-actions>
              <v-btn class="orange--text darken-1"
                     flat
                     @click="deleteUserDialog=false"
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
    props: ['_user'],
    data(){
      return {
        deleteUserDialog: false
      }
    },
    computed: {
      userIsOwner () {
        return this._user && this.userIsAuthenticated && this._user.id === this.user.id
      },
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      user(){
        return this.$store.getters.user
      },
      userDeleted(){
        return this.$store.getters.postRequest
      },
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true
      }
    },
    methods: {
      onAgree(){
        if(this.userIsAdmin){
          if(this.user.id === this._user.id){
            this.$store.commit('setError', ['Admin cannot delete himself'])
            this.deleteUserDialog = false;
            return;
          }
          this.deleteUserDialog = false
          this.$router.push('/admin/users')
          this.$store.dispatch('adminDeleteUser', this._user.id)
        }else{
          this.$store.dispatch('deleteUser', this.user.id)
          this.$router.push('/')
        }
      }
    },
  }
</script>

<style scoped>

</style>
