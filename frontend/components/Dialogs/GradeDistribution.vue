<template>
    <v-dialog persistent v-model="gradeDistributionDialog" max-width="590">
      <v-img
        slot="activator"
        :src="`${url1}/images/${n.image}`"
        :lazy-src="`${url1}/images/${n.image}`"
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
              :src="`${url1}/images/${n.image}`"
              :lazy-src="`${url1}/images/${n.image}`"
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
                <v-spacer></v-spacer>
                <v-btn
                  v-if="userCanDelete"
                  class="default--text darken-2"
                  flat
                  color="red"
                  @click="deleteGradeDistribution(n)"
                >Delete</v-btn>
              </v-card-actions>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-dialog>
</template>

<script>
  export default {
    props: ['n', 'index'],
    name: "GradeDistribution",
    data(){
      return {
        gradeDistributionDialog: false,
        url1: 'http://localhost:5000',
        url2: 'https://dummy-server-08.herokuapp.com'
      }
    },
    computed: {
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      user(){
        return this.$store.getters.user
      },
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true;
      },
      userCanDelete(){
        return this.userIsAdmin || (this.userIsAuthenticated && this.n.user_id === this.user.id)
      }
    },
    methods:{
      deleteGradeDistribution(grade){
        this.$store.dispatch('deleteGradeDistribution', {
          'id': grade.id,
          'index': this.index
        })
        this.gradeDistributionDialog = false;
      }
    }
  }
</script>

<style scoped>

</style>
