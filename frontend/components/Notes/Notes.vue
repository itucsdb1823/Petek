<template>
    <v-container>
        <v-layout row>
            <v-flex xs12 sm12>
                <v-data-table
                  :headers="headers"
                  :items="notes"
                  class="elevation-1"
                >
                  <template slot="items" slot-scope="props">
                    <td>{{ props.item.title }}</td>
                    <td class="text-xs-left">{{ props.item.course }}</td>
                    <td class="text-xs-left">{{ props.item.lecturer }}</td>
                    <td class="text-xs-left">{{ props.item.term }}</td>
                    <td class="text-xs-left">{{ props.item.date }}</td>
                    <td class="text-xs-left">{{ props.item.user_id }}</td>
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

        },
        computed: {
            notes(){
                return this.$store.getters.notes;
            }
        }
    }
</script>
