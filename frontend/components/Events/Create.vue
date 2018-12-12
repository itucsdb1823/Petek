<template>
  <v-container>
      <v-layout row>
        <v-flex xs12 sm6 offset-sm3>
          <v-card>
            <v-card-text>
              <v-container>
                <form @submit.prevent="create_event">
                  <!--Title Input Field-->
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="title"
                        label="Title"
                        id="title"
                        v-model="title"
                        type="text"
                        placeholder="Yarın 6'da voleybol maçı"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout row justify-space-between align-center>
                    <v-text-field
                        name="max_participant"
                        label="Max Participant"
                        id="max_participant"
                        v-model="max_participant"
                        type="number"
                        required
                      >
                      </v-text-field>
                  </v-layout>
                  <!--Lecturers Dropdown-->
                  <v-flex xs12>
                    <v-text-field
                        name="description"
                        label="Description"
                        id="description"
                        v-model="description"
                        type="text"
                        placeholder="Merkezi spor salonunda voleybol maçı yapacağız"
                        required
                      >
                      </v-text-field>
                  </v-flex>
                  <v-layout row>
                    <v-flex xs12>
                      <v-date-picker v-model="started_at"></v-date-picker>
                    </v-flex>
                  </v-layout>
                  <v-layout row>
                    <v-flex xs12>
                      <v-btn type="submit" color="success">
                        Create Event
                        <span slot="loader" class="custom-loader">
                          <v-icon light>cached</v-icon>
                        </span>
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </form>
              </v-container>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
  export default {
    components: {},
    data() {
      return {
        title: '',
        description: '',
        started_at: '',
        max_participant: ''
      }
    },
    methods: {
      create_event() {
        if(!this.formIsValid){
          this.$store.commit('setError', ['Please fill all fields!'])
          return;
        }

        const event = {
          title: this.title,
          description: this.description,
          started_at: this.started_at,
          max_participant: this.max_participant,
        }
        this.$store.dispatch('createEvent', event)
        this.$router.push('/events')
      },
      formIsValid() {
        return this.title !== '' && this.description !== '' && this.started_at !== '' && this.max_participant !== ''
      },
    },
    computed: {
    },
    created(){

    },
    updated(){
      if(this.$store.getters.user === null){
        this.$store.commit('setError', ['Please login to create event!'])
      }
    },
    watch: {

    }
  }
</script>

<style scoped>

</style>
