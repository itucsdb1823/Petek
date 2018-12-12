<template>
  <v-dialog persistent v-model="deleteNoteDialog" max-width="290">
    <v-btn slot="activator" flat color="red" align-end v-if="userIsOwner || userIsAdmin">
      <v-icon right dark>delete</v-icon>
      Delete
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Delete Note</v-card-title>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-text>Do you really want to delete this note?</v-card-text>
          </v-flex>
        </v-layout>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-actions>
              <v-btn class="orange--text darken-1"
                     flat
                     @click="deleteNoteDialog=false"
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
    props: ['note'],
    data(){
      return {
        deleteNoteDialog: false
      }
    },
    computed: {
      userIsOwner () {
        return this.userIsAuthenticated && this.note.user_id === this.user.id
      },
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      user(){
        return this.$store.getters.user
      },
      noteDeleted(){
        return this.$store.getters.postRequest
      },
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true
      }
    },
    methods: {
      onAgree(){
        if(this.userIsAdmin){
          this.$store.dispatch('adminDeleteNote', this.note.id)
        }else{
          this.$store.dispatch('deleteNote', this.note.id)
        }
        this.$router.push('/notes')
      }
    },
    watch: {
      noteDeleted(value){
        if(value === true){
          this.deleteNoteDialog = false
          this.$router.push('/notes')
          this.$store.commit('postRequest', null)
        }else if(value === false){
          this.$store.commit('postRequest', null)
        }
      }
    }
  }
</script>

<style scoped>

</style>
