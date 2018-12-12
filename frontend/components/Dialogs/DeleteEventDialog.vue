<template>
  <v-dialog persistent v-model="deleteEventDialog" max-width="290">
    <v-btn slot="activator" flat color="red" align-end v-if="userIsOwner || userIsAdmin">
      <v-icon right dark>delete</v-icon>
      Delete
    </v-btn>
    <v-card>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-title>Delete Event</v-card-title>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-text>Do you really want to delete this event?</v-card-text>
          </v-flex>
        </v-layout>
        <v-layout row wrap>
          <v-flex xs12>
            <v-card-actions>
              <v-btn class="orange--text darken-1"
                     flat
                     @click="deleteEventDialog=false"
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
    props: ['event'],
    data(){
      return {
        deleteEventDialog: false
      }
    },
    computed: {
      userIsOwner () {
        return this.userIsAuthenticated && this.event.user_id === this.user.id
      },
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
        if(this.userIsAdmin){
          this.$store.dispatch('adminDeleteEvent', this.event.id)
        }else{
          this.$store.dispatch('deleteEvent', this.event.id)
        }
        this.$router.push('/events')
      }
    },
    watch: {
    }
  }
</script>

<style scoped>

</style>
