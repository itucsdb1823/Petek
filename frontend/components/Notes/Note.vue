<template v-if="note">
  <v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-card>
        <v-container>
          <v-layout row fill-height>
            <v-flex xs6 class="note-title">
              {{ note.title }}
            </v-flex>
            <v-flex xs6 class="grey--text text-xs-right">
              {{ note.user.name }}
            </v-flex>
          </v-layout>
          <div class="grey--text">{{ note.content }}</div>
        </v-container>
        <v-card-actions>
          <v-btn flat color="green" :href="note.link" target="_blank">Go To Link</v-btn>
          <v-btn flat color="red">Report</v-btn>
          <v-spacer v-if="userIsOwner"></v-spacer>
          <edit-note-dialog
            :note="note"
            v-if="userIsAuthenticated && userIsOwner"
          ></edit-note-dialog>
          <delete-note-dialog
            :note="note"
            v-if="userIsAuthenticated && userIsOwner"
          ></delete-note-dialog>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  import DeleteNoteDialog from "../Dialogs/DeleteNoteDialog";
  import EditNoteDialog from "../Dialogs/EditNoteDialog";

  export default {
    name: "Note",
    components: {EditNoteDialog, DeleteNoteDialog},
    metaInfo: {
      // title will be injected into parent titleTemplate
      title: "Note"
    },
    data() {
      return {

      }
    },
    beforeCreate(){
      let note_slug = this.$route.params.note_slug
      this.$store.dispatch('getNote', note_slug)
    },
    computed: {
      note(){
        return this.$store.getters.note
      },
      user(){
        return this.$store.getters.user
      },
      userIsOwner(){
        return this.userIsAuthenticated && this.note.user_id === this.user.id
      },
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
    },
  }
</script>

<style scoped>
  .note-title{
    font-size: 23px;
  }
</style>
