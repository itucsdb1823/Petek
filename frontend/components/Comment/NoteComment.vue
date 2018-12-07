<template>
    <v-dialog persistent v-model="addNoteCommentDialog" max-width="590">
    <v-btn slot="activator" flat color="green" align-end :disabled="!userIsAuthenticated">
      <v-icon right dark>add</v-icon>
      Add Comment
    </v-btn>
    <v-card>
      <v-container>
      <v-layout row>
        <v-flex xs12>
          <v-card>
            <v-card-text>
              <v-container>
                <form @submit.prevent="add_note_comment">
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="comment"
                        label="Comment"
                        id="comment"
                        v-model="comment"
                        type="text"
                        placeholder="Paylaşım için teşekkürler!"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout row>
                    <v-flex xs12>
                      <v-btn type="submit" color="success">
                        Add Comment
                        <span slot="loader" class="custom-loader">
                          <v-icon light>cached</v-icon>
                        </span>
                      </v-btn>
                      <v-btn @click="addLecturerCommentDialog=false" type="submit" color="red">
                        Close
                        <span slot="loader" class="custom-loader">
                          <v-icon light>cached</v-icon>
                        </span>
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </form>
              </v-container>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
    export default {
      props: ['note'],
      name: "NoteComment",
      data(){
        return{
          addNoteCommentDialog: false,
          comment: ''
        }
      },
      computed: {
        commentUploaded(){
          return this.$store.getters.postRequest
        },
        userIsAuthenticated(){
          return this.user !== null && this.user !== undefined;
        },
        user(){
          return this.$store.getters.user
        },
      },
      methods: {
        add_note_comment(){
          const comment = {
            comment: this.comment,
            type_id: this.note.id
          }

          this.$store.dispatch('addNoteComment', comment)
          this.addNoteCommentDialog = false
        }
      },
      watch: {
        commentUploaded(value){
          if(value === true){
            this.$store.commit('postRequest', null)
            this.addNoteCommentDialog = false
          }
        }
      }
    }
</script>

<style scoped>

</style>
