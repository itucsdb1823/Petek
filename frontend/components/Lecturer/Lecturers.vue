<template>
    <v-container>
      <v-layout row>
        <v-flex xs12 sm9>
          <v-btn color="success" to="lecturers/create">Add Lecturer</v-btn>
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
            <template v-for="(item, index) in filteredLecturers.slice(0, limit)">
              <v-list-tile :key="index" avatar ripple @click="lecturer(item.slug)">
                <v-list-tile-content>
                  <v-list-tile-title>{{ item.name }}</v-list-tile-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-icon color="grey lighten-1">arrow_right_alt</v-icon>
                </v-list-tile-action>
              </v-list-tile>
              <v-divider v-if="index + 1 < lecturers.length" :key="`divider-${index}`"></v-divider>
            </template>
          </v-list>
        </v-flex>
      </v-layout>
      <v-layout row justify-center v-if="limit < lecturers.length">
        <v-flex xs6 offset-xs3>
          <v-btn color="orange" @click="limit += 5">Load More</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
  export default {
    components: {},
    data() {
      return {
        search: '',
        limit: 5
      }
    },
    methods: {
      lecturer(lecturer_slug){
        console.log(lecturer_slug)
        let go = this.$router.push(`lecturers/${lecturer_slug}`)
      }
    },
    computed: {
      lecturers(){
        return this.$store.getters.lecturers;
      },
      filteredLecturers(){
        return this.lecturers.filter(lecturer => {
          return lecturer.name.toLowerCase().includes(this.search.toLowerCase())
        })
      }
    },
    mounted(){
      this.$store.dispatch('getLecturers')
    }
  }
</script>
