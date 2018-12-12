<template>
  <v-container>
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <v-container>
            <v-layout row fill-height>
              <v-flex xs6 class="note-title">
                {{ _user === undefined || _user === null ? '' : _user.name }}
              </v-flex>
              <v-flex xs6 class="grey--text text-xs-right">
                {{ _user === undefined || _user === null ? '' : _user.email }}
              </v-flex>
            </v-layout>

          </v-container>
          <v-card-actions v-if="_user !== undefined && _user !== null">
            <v-spacer v-if="userIsOwner || userIsAdmin"></v-spacer>
            <edit-user-dialog
              v-if="((userIsAuthenticated && userIsOwner) || userIsAdmin)"
              :_user="_user"
            ></edit-user-dialog>
            <delete-user-dialog
              :_user="_user"
              v-if="(userIsAuthenticated && userIsOwner) || userIsAdmin"
            ></delete-user-dialog>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import EditUserDialog from "./EditUserDialog";
  import DeleteUserDialog from "./DeleteUserDialog";

  export default {
    name: "User",
    components: {EditUserDialog, DeleteUserDialog},
    beforeCreate(){
      let user_slug = this.$route.params.user_slug
      this.$store.dispatch('get_user', user_slug)
    },
    computed: {
      _user(){
        return this.$store.getters.get_user
      },
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true;
      },
      userIsOwner(){
        return this._user !== undefined && this.userIsAuthenticated && this._user !== null && this._user.id === this.user.id
      },
      user(){
        return this.$store.getters.user
      },
    },
  }
</script>

<style scoped>

</style>
