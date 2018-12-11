<template>
  <v-container>
    <v-layout row>
      <v-flex xs12 sm9>
        <add-course-dialog
        ></add-course-dialog>
      </v-flex>
      <v-flex xs12 sm3>
        <v-text-field
          v-model="search"
          label="Search:"
        ></v-text-field>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex xs12 sm12>
        <v-list two-line>
          <template v-for="(item, index) in filteredCourses.slice(0, limit)">
            <v-list-tile :key="index" avatar ripple>
              <v-list-tile-content>
                <v-list-tile-title>{{ item.name === null || item.name === undefined ? (item === null || item === undefined ? '' : '') : item.name  }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-layout>
                  <v-flex xs12>
                    <delete-course-dialog
                      :course="item"
                    ></delete-course-dialog>
                  </v-flex>
                  <v-flex xs12>
                    <edit-course-dialog
                      :course="item"
                    ></edit-course-dialog>
                  </v-flex>
                </v-layout>
              </v-list-tile-action>
            </v-list-tile>
            <v-divider v-if="index + 1 < courses.length" :key="`divider-${index}`"></v-divider>
          </template>
        </v-list>
      </v-flex>
    </v-layout>
    <v-layout row justify-center v-if="limit < courses.length">
      <v-flex xs6 offset-xs3>
        <v-btn color="orange" @click="limit += 5">Load More</v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import AddCourseDialog from './AddCourseDialog'
  import EditCourseDialog from './EditCourseDialog'
  import DeleteCourseDialog from "./DeleteCourseDialog";

  export default {
    components: {DeleteCourseDialog, AddCourseDialog, EditCourseDialog},
    name: "Courses",
    data(){
      return {
        search: '',
        limit: 5
      }
    },
    computed: {
      courses(){
        return this.$store.getters.courses
      },
      filteredCourses(){
        return this.courses.filter(course => {
          if(course.name !== null && course.name !== undefined){
            return course.name.toLowerCase().includes(this.search.toLowerCase())
          }else{
            // return course.toLowerCase().includes(this.search.toLowerCase())
          }
        })
      }
    },
    beforeCreate(){
      this.$store.dispatch('getCourses')
    }
  }
</script>

<style scoped>

</style>
