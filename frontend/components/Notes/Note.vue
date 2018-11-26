<template>
   <v-container grid-list-md text-xs-center>
    <v-layout row wrap>
      <div>
        <v-btn color="success">{{ note.title }}</v-btn>
      </div>
    </v-layout>
   </v-container>
</template>

<script>
  export default {
    name: "Note",
    data() {
      return {
      }
    },
    created(){
      let note_slug = this.$route.params.note_slug
      this.$store.dispatch('getNote', note_slug)
    },
    computed: {
      note(){
        return this.$store.getters.note;
      }
    },
  }
</script>

<style scoped>

</style>
