<template v-if="note">
  <v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-card>
        <v-container>
          <v-layout row fill-height>
            <v-flex xs6 class="lecturer-title">
              {{ lecturer.name }}
            </v-flex>
            <v-flex xs6 class="grey--text text-xs-right">
              {{ lecturer.email }}
            </v-flex>
          </v-layout>
        </v-container>
        <v-card-actions>
          <v-btn flat color="red">Report</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

  export default {
    name: "Lecturer",
    metaInfo: {
      // title will be injected into parent titleTemplate
      title: "Lecturer"
    },
    data() {
      return {

      }
    },
    beforeCreate(){
      let lecturer_slug = this.$route.params.lecturer_slug
      this.$store.dispatch('getLecturer', lecturer_slug)
    },
    computed: {
      lecturer(){
        return this.$store.getters.lecturer
      },
    },
  }
</script>

<style scoped>
  .lecturer-title{
    font-size: 23px;
  }
</style>
