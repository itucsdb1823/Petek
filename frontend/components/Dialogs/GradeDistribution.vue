<template>
    <v-dialog persistent v-model="gradeDistributionDialog" max-width="590">
      <v-img
        slot="activator"
        :src="`http://localhost:5000/images/${n.image}`"
        :lazy-src="`http://localhost:5000/images/${n.image}`"
        aspect-ratio="2"
        class="grey lighten-2"
      >
        <v-layout
          slot="placeholder"
          fill-height
          align-center
          justify-center
          ma-0
        >
          <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
        </v-layout>
      </v-img>
      <v-card>
        <v-container>
          <v-layout row wrap>
            <v-img
              :src="`http://localhost:5000/images/${n.image}`"
              :lazy-src="`http://localhost:5000/images/${n.image}`"
              aspect-ratio="1"
              class="grey lighten-2"
            >
              <v-layout
                slot="placeholder"
                fill-height
                align-center
                justify-center
                ma-0
              >
                <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
              </v-layout>
            </v-img>
          </v-layout>
          <v-layout row wrap>
            <v-flex xs12>
              <v-card-actions>
                <v-btn class="default--text darken-1"
                 flat
                 @click="gradeDistributionDialog=false"
                >Close</v-btn>
              </v-card-actions>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-dialog>
</template>

<script>
  export default {
    props: ['n'],
    name: "GradeDistribution",
    data(){
      return {
        gradeDistributionDialog: false,
      }
    },
  }
</script>

<style scoped>

</style>
