<template>
  <v-container>
    <v-layout row>
      <v-flex xs12 sm9>
        <add-term-dialog
        ></add-term-dialog>
      </v-flex>
      <v-flex xs12 sm3>
        <v-text-field
          v-model="search"
          label="Search:"
        ></v-text-field>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex xs12 sm12>
        <v-list two-line>
          <template v-for="(item, index) in terms.slice(0, limit)">
            <v-list-tile :key="index" avatar ripple>
              <v-list-tile-content>
                <v-list-tile-title>{{ item.season + ' - ' + item.term_year  }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-layout>
                  <v-flex xs12>
                    <delete-term-dialog
                      :term="item"
                    ></delete-term-dialog>
                  </v-flex>
                  <v-flex xs12>
                    <edit-term-dialog
                      :term="item"
                    ></edit-term-dialog>
                  </v-flex>
                </v-layout>
              </v-list-tile-action>
            </v-list-tile>
            <v-divider v-if="index + 1 < terms.length" :key="`divider-${index}`"></v-divider>
          </template>
        </v-list>
      </v-flex>
    </v-layout>
    <v-layout row justify-center v-if="limit < terms.length">
      <v-flex xs6 offset-xs3>
        <v-btn color="orange" @click="limit += 5">Load More</v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import AddTermDialog from './AddTermDialog'
  import EditTermDialog from './EditTermDialog'
  import DeleteTermDialog from "./DeleteTermDialog";

  export default {
    components: {DeleteTermDialog, AddTermDialog, EditTermDialog},
    name: "Terms",
    data(){
      return {
        search: '',
        limit: 5
      }
    },
    computed: {
      terms(){
        return this.$store.getters.terms
      },
    },
    beforeCreate(){
      this.$store.dispatch('getTerms')
    }
  }
</script>

<style scoped>

</style>
