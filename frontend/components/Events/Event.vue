<template v-if="event">
  <v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-card>
        <v-container>
          <v-layout row fill-height>
            <v-flex xs6 class="note-title">
              {{ event.title }}
            </v-flex>
            <v-flex xs6 class="grey--text text-xs-right">
              Created By: {{ event.user.name }}
            </v-flex>
          </v-layout>
          <div class="grey--text">{{ event.description }}</div>
          <div class="grey--text">{{ event.started_at }}</div>
        </v-container>
        <v-card-actions>
          <v-btn flat color="red">Report</v-btn>
          <v-spacer v-if="userIsOwner || userIsAdmin"></v-spacer>
          <edit-event-dialog
            :event="event"
            v-if="(userIsAuthenticated && userIsOwner) || userIsAdmin"
          ></edit-event-dialog>
          <delete-event-dialog
            :event="event"
            v-if="(userIsAuthenticated && userIsOwner) || userIsAdmin"
          ></delete-event-dialog>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  import DeleteEventDialog from "../Dialogs/DeleteEventDialog";
  import EditEventDialog from "../Dialogs/EditEventDialog";

  export default {
    name: "Event",
    components: {EditEventDialog, DeleteEventDialog},
    metaInfo: {
      // title will be injected into parent titleTemplate
      title: "Event"
    },
    data() {
      return {

      }
    },
    beforeCreate(){
      let event_id = this.$route.params.event_id
      this.$store.dispatch('getEvent', event_id)
    },
    computed: {
      event(){
        return this.$store.getters.event
      },
      user(){
        return this.$store.getters.user
      },
      userIsOwner(){
        return this.userIsAuthenticated && this.event.user_id === this.user.id
      },
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true
      }
    },
    methods: {

    }
  }
</script>

<style scoped>
  .note-title{
    font-size: 23px;
  }
</style>
