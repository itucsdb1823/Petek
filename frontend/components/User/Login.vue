<template>
    <v-container>
        <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
                <v-card>
                    <v-card-text>
                        <v-container>
                            <form @submit.prevent="login">
                                <!--EMAIL INPUT FIELD-->
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="email"
                                                label="Mail"
                                                id="email"
                                                v-model="email"
                                                type="email"
                                                required
                                        >

                                        </v-text-field>
                                    </v-flex>
                                </v-layout>

                                <!--PASSWORD INPUT FIELD-->
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="password"
                                                label="Password"
                                                id="password"
                                                v-model="password"
                                                type="password"
                                                required
                                        >

                                        </v-text-field>
                                    </v-flex>
                                </v-layout>

                                <v-layout row>
                                    <v-flex xs12>
                                        <v-btn type="submit">
                                            Login
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
                email: '',
                password: ''
            }
        },
        methods: {
            login(){
                // Vuex
                this.$store.dispatch('login', {email: this.email, password: this.password});
                if(this.user !== null && this.user !== undefined){
                    this.$router.push('/');
                }
            }
        },
        computed: {
            user(){
                return this.$store.getters.user;
            }
        },
        watch: {
            user(value){
                if(value !== null && value !== undefined){
                    this.$router.push('/');
                }
            }
        }
    }
</script>

<style>

</style>
