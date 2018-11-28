<template>
    <v-container>
      <v-layout row>
        <v-flex xs12 sm12>
          <v-btn color="success" to="notes/create">Create Note</v-btn>
        </v-flex>
      </v-layout>
        <v-layout row>
            <v-flex xs12 sm12>
                <v-data-table
                  :headers="headers"
                  :items="notes"
                  class="elevation-1"
                >
                  <template slot="items" slot-scope="props">
                    <td @click="note(props.item.slug)"><v-icon>visibility</v-icon></td>
                    <td @click="note(props.item.slug)">{{ props.item.title }}</td>
                    <td class="text-xs-left">{{ props.item.course }}</td>
                    <td class="text-xs-left">{{ props.item.lecturer }}</td>
                    <td class="text-xs-left">{{ props.item.term }}</td>
                    <td class="text-xs-left">{{ props.item.date }}</td>
                    <td class="text-xs-left">{{ props.item.user.name }}</td>
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
          { text: 'Code', value: 'code' },
          { text: 'Lecturer', value: 'lecturer' },
          { text: 'Term/Season', value: 'term' },
          { text: 'Date', value: 'date' },
          { text: 'Sharer', value: 'sharer' }
        ],
      }
    },
    methods: {
      note(note_slug){
        console.log(note_slug)
        let go = this.$router.push(`notes/${note_slug}`)
      }
    },
    computed: {
      notes(){
        return this.$store.getters.notes;
      }
    },
    mounted(){
      this.$store.dispatch('getNotes')
    }
  }
</script>
