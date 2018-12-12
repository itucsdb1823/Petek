<template>
  <v-container>
  <v-layout row>
    <v-flex xs12 sm12>
      <v-btn color="success" to="notes/create">Create Note</v-btn>
    </v-flex>
  </v-layout>
    <v-layout row>
      <v-flex xs12 sm12>
        <v-data-table
          :headers="headers"
          :items="users"
          class="elevation-1"
        >
          <template slot="items" slot-scope="props">
            <td @click="user(props.item.slug)"><v-icon>visibility</v-icon></td>
            <td @click="user(props.item.slug)">{{ props.item.name }}</td>
            <td class="text-xs-left">{{ props.item.email }}</td>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    name: "Users",
    data() {
      return {
        headers: [
          {
            text: '#',
            align: 'left',
            sortable: false,
          },
          {
            text: 'Name',
            align: 'left',
            sortable: false,
            value: 'name'
          },
          { text: 'Email', value: 'email' },
        ],
      }
    },
    methods: {
      user(user_slug){
        let go = this.$router.push(`/users/${user_slug}`)
      }
    },
    computed: {
      users(){
        return this.$store.getters.getUsers;
      }
    },
    mounted(){
      this.$store.dispatch('getUsers')
    }
  }
</script>

<style scoped>

</style>
