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
          <v-layout row>
            <v-flex xs12>
              <v-toolbar-title style="color: aquamarine; margin-top: 50px;">Comments</v-toolbar-title>
              <v-list two-line>
                <template v-for="(item, index) in note.comments.slice(0, limit)">
                  <v-list-tile :key="index" avatar ripple>
                    <v-list-tile-content>
                      <v-list-tile-title><b style="color: #1E90FF;">{{ item.user.name}}:</b> {{ (item.comment.comment === undefined || item.comment.comment === null) ? item.comment : item.comment.comment }}</v-list-tile-title>
                    </v-list-tile-content>
                    <v-list-tile-action v-if="(userIsAuthenticated && user.id === item.user.id) || userIsAdmin">
                      <v-icon color="red lighten-1" @click="deleteComment(item.id, index)">delete</v-icon>
                    </v-list-tile-action>
                  </v-list-tile>
                  <v-divider v-if="index + 1 < note.comments.length" :key="`divider-${index}`"></v-divider>
                </template>
              </v-list>
              <v-layout row justify-left v-if="limit < note.comments.length">
                <v-flex xs6>
                  <v-btn color="orange" @click="limit += 3">Load More</v-btn>
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-container>

        <v-layout row fill-width>
          <note-comment
            :note="note"
            :disabled="!userIsAuthenticated"
          ></note-comment>
        </v-layout>
        <v-card-actions>
          <v-btn flat color="green" :href="note.link" target="_blank">Go To Link</v-btn>
          <v-btn flat color="red">Report</v-btn>
          <v-spacer v-if="userIsOwner || userIsAdmin"></v-spacer>
          <edit-note-dialog
            :note="note"
            v-if="(userIsAuthenticated && userIsOwner) || userIsAdmin"
          ></edit-note-dialog>
          <delete-note-dialog
            :note="note"
            v-if="(userIsAuthenticated && userIsOwner) || userIsAdmin"
          ></delete-note-dialog>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  import DeleteNoteDialog from "../Dialogs/DeleteNoteDialog";
  import EditNoteDialog from "../Dialogs/EditNoteDialog";
  import NoteComment from "../Comment/NoteComment";

  export default {
    name: "Note",
    components: {EditNoteDialog, DeleteNoteDialog, NoteComment},
    metaInfo: {
      // title will be injected into parent titleTemplate
      title: "Note"
    },
    data() {
      return {
        limit: 3
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
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true
      }
    },
    methods: {
      deleteComment(comment_id, index){
        const deleteComment = {
          comment_id: comment_id,
          note_id: this.note.id,
          comment_index: index
        }
        if(this.userIsAdmin){
          this.$store.dispatch('adminDeleteNoteComment', deleteComment)
        }else{
          this.$store.dispatch('deleteNoteComment', deleteComment)
        }
      }
    }
  }
</script>

<style scoped>
  .note-title{
    font-size: 23px;
  }
</style>
