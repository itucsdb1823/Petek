<template>
  <v-dialog persistent v-model="editEventDialog" max-width="590">
    <v-btn slot="activator" flat color="orange" align-end v-if="userIsOwner || userIsAdmin">
      <v-icon right dark>edit</v-icon>
      Edit
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Edit Event</v-card-title>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card>
            <v-card-text>
              <v-container>
                <form @submit.prevent="edit_event">
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="title"
                        label="Title"
                        id="title"
                        v-model="event.title"
                        type="text"
                        placeholder="Yarın 6'da voleybol maçı"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout row justify-space-between align-center>
                    <v-text-field
                        name="max_participant"
                        label="Max Participant"
                        id="max_participant"
                        v-model="event.max_participant"
                        type="number"
                        required
                      >
                      </v-text-field>
                  </v-layout>
                  <v-flex xs12>
                    <v-text-field
                        name="description"
                        label="Description"
                        id="description"
                        v-model="event.description"
                        type="text"
                        placeholder="Merkezi spor salonunda voleybol maçı yapacağız"
                        required
                      >
                      </v-text-field>
                  </v-flex>
                  <v-layout row>
                    <v-flex xs12>
                      <v-datetime-picker
                        label="Start time"
                        v-model="event.started_at">
                      </v-datetime-picker>
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
                     @click="editEventDialog=false"
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
    props: ['event'],
    data(){
      return {
        editEventDialog: false,
      }
    },
    computed: {
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true
      },
      userIsOwner () {
        return this.userIsAuthenticated && this.event.user_id === this.user.id
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
        if(this.userIsAdmin){
          this.$store.dispatch('adminEditEvent', this.event)
        }else{
          this.$store.dispatch('editEvent', this.event)
        }
        this.editEventDialog = false
      }
    },
    watch: {

    },
    created() {

    }
  }
</script>

<style scoped>

</style>
