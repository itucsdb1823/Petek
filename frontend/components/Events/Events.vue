<template>
  <v-container>
    <v-layout row>
      <v-flex xs12 sm12>
        <v-btn color="success" to="events/create">Create Event</v-btn>
      </v-flex>
    </v-layout>
      <v-layout row>
          <v-flex xs12 sm12>
              <v-data-table
                :headers="headers"
                :items="events"
                class="elevation-1"
              >
                <template slot="items" slot-scope="props">
                  <td @click="event(props.item.id)"><v-icon>visibility</v-icon></td>
                  <td @click="event(props.item.id)">{{ props.item.title }}</td>
                  <td class="text-xs-left">{{ props.item.max_participant }}</td>
                  <td class="text-xs-left">{{ props.item.started_at }}</td>
                  <td @click="event(props.item.event.id)" class="text-xs-left">{{ props.item.user.name }}</td>
                </template>
              </v-data-table>
          </v-flex>
      </v-layout>
  </v-container>
</template>

<script>
  export default {
    components: {},
    data() {
      return {
        headers: [
          {
            text: '#',
            align: 'left',
            sortable: false,
          },
          {
            text: 'Title',
            align: 'left',
            sortable: false,
            value: 'name'
          },
          { text: 'Max Participant', value: 'max_participant' },
          { text: 'Starts At', value: 'started_at' },
          { text: 'Sharer', value: 'sharer' }
        ],
      }
    },
    methods: {
      event(event_id){
        let go = this.$router.push(`events/${event_id}`)
      },
      user(slug){
        let go = this.$router.push(`users/${slug}`)
      }
    },
    computed: {
      events(){
        return this.$store.getters.events;
      }
    },
    mounted(){
      this.$store.dispatch('getEvents')
    }
  }
</script>
