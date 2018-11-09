<template>
    <v-container>
        <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
                <v-card>
                    <v-card-text>
                        <v-container>
                          <form @submit.prevent="register">

                            <!-- demo root element -->
                            <div id="demo">
                              <form id="search">
                                Search <input name="query" v-model="searchQuery">
                              </form>
                              <demo-grid
                                :data="gridData"
                                :columns="gridColumns"
                                :filter-key="searchQuery">
                              </demo-grid>
                            </div>

                            <aside>
                              <!--Search bar-->
                              <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="lecture_code"
                                                label="Lecture Code"
                                                id="lecture_code"
                                                v-model="lecture_code"
                                                type="name"
                                                required
                                        >

                                        </v-text-field>
                                    </v-flex>
                                </v-layout>



                                <v-layout row>
                                    <v-flex xs12>
                                        <v-btn type="submit" :disabled="loading" :loading="loading">
                                            Register
                                            <span slot="loader" class="custom-loader">
                                                <v-icon light>cached</v-icon>
                                            </span>
                                        </v-btn>
                                    </v-flex>
                                </v-layout>
                              </aside>
                            </form>
                        </v-container>
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<!-- component template -->
<script type="text/x-template" id="grid-template">
  <table>
    <thead>
      <tr>
        <th v-for="key in columns"
          @click="sortBy(key)"
          :class="{ active: sortKey == key }">
          {{ key | capitalize }}
          <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
          </span>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="entry in filteredData">
        <td v-for="key in columns">
          {{entry[key]}}
        </td>
      </tr>
    </tbody>
  </table>
</script>
