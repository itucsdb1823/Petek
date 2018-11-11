<template>
  <v-container>
        <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
                <v-card>
                    <v-card-text>
                        <v-container>
                            <form @submit.prevent="createNote">
                                <!--CONFIRM PASSWORD INPUT FIELD-->
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="title"
                                                label="Title"
                                                id="title"
                                                v-model="title"
                                                type="text"
                                        >
                                        </v-text-field>
                                    </v-flex>
                                </v-layout>
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="code"
                                                label="Code"
                                                id="code"
                                                v-model="code"
                                                type="text"
                                        >
                                        </v-text-field>
                                    </v-flex>
                                </v-layout>
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="lecturer"
                                                label="Lecturer"
                                                id="lecturer"
                                                v-model="lecturer"
                                                type="text"
                                        >
                                        </v-text-field>
                                    </v-flex>
                                </v-layout>
                                <v-flex xs6>
                                  <v-select
                                    :items="term"
                                    v-model="t1"
                                    menu-props="auto"
                                    label="Select"
                                    hide-details
                                    single-line
                                  ></v-select>
                                </v-flex>


                                <v-layout row>
                                    <v-flex xs12>
                                        <v-btn type="submit" :disabled="loading" :loading="loading">
                                            Create Note
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
        code: '',
        lecturer: '',
        t1:"17/18",
        term: ['17/18', '16/17', '15/16'],
        date: '',
        sharer: ''
      }
    },
    methods: {
      createNote() {
        const note = {
           title: this.title,
           code: this.code,
           lecturer: this.lecturer,
           term: this.term,
           date: this.date,
           sharer: this.sharer
        }
        this.$store.dispatch('createNote', note)
      },
    }
  }
</script>

<style scoped>

</style>
