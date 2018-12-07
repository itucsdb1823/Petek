<template>
  <v-container>
      <v-layout row>
        <v-flex xs12 sm6 offset-sm3>
          <v-card>
            <v-card-text>
              <v-container>
                <form @submit.prevent="create_lecturer">
                  <!--Title Input Field-->
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="name"
                        label="Name"
                        id="name"
                        v-model="name"
                        type="text"
                        placeholder="Hayri Turgut Uyar"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout row>
                    <v-flex xs12>
                      <v-text-field
                        name="email"
                        label="Email"
                        id="email"
                        v-model="email"
                        type="text"
                        placeholder="uyar@itu.edu.tr"
                        required
                      >
                      </v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout row>
                    <v-flex xs12>
                      <v-btn type="submit" color="success">
                        Add Lecturer
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
        name: '',
        email: ''
      }
    },
    methods: {
      create_lecturer() {
        if(!this.formIsValid){
          this.$store.commit('setError', ['Please fill all fields!'])
          return;
        }

        const lecturer = {
          name: this.name,
          email: this.email,
        }
        this.$store.dispatch('createLecturer', lecturer)
      },
      formIsValid() {
        return this.name !== '' && this.email !== '';
      },
    },
    computed: {
      lecturerUploaded(){
        return this.$store.getters.postRequest
      }
    },
    updated(){
      if(this.$store.getters.user === null){
        this.$store.commit('setError', ['Please login to add lecturer!'])
      }
    },
    watch: {
      lecturerUploaded(value){
        if(value === true){
          this.$store.commit('postRequest', null)
          this.$router.push('/lecturers');
        }else if(value === false){
          this.$store.commit('postRequest', null)
        }
      }
    }
  }
</script>

<style scoped>

</style>
