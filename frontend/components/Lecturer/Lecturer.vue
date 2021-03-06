<template v-if="lecturer">
    <v-container>
      <v-layout>
        <v-flex xs12 sm10 offset-sm1>
          <v-card>
            <v-container>
              <v-layout row fill-height>
                <v-flex xs9 class="lecturer-title">
                  <v-layout row>
                    <v-flex xs2>
                    {{ lecturer.name }}
                  </v-flex>
                  <v-flex xs5>
                    <add-grade-distribution-dialog
                    :lecturer="lecturer"
                    v-if="userIsAuthenticated"
                  ></add-grade-distribution-dialog>
                  </v-flex>
                  <v-flex xs5>
                    <add-comment-dialog
                    :lecturer="lecturer"
                    :disabled="!userIsAuthenticated"
                  ></add-comment-dialog>
                  </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex xs3 class="grey--text text-xs-right">
                  {{ lecturer.email }}
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs4>
                  <v-list two-line>
                    <template v-for="(item, index) in lecturer.comments.slice(0, commentLimit)">
                      <v-list-tile :key="index" avatar ripple>
                        <v-list-tile-content>
                          <v-list-tile-title>{{ (item.comment.comment === undefined || item.comment.comment === null) ? item.comment : item.comment.comment  }}</v-list-tile-title>
                        </v-list-tile-content>
                        <v-list-tile-action v-if="(userIsAuthenticated && user.id === item.user_id) || userIsAdmin">
                          <v-icon color="red lighten-1" @click="deleteComment(item.id, index)">delete</v-icon>
                        </v-list-tile-action>
                      </v-list-tile>
                      <v-divider v-if="index + 1 < lecturer.comments.length" :key="`divider-${index}`"></v-divider>
                    </template>
                  </v-list>
                  <v-layout row justify-center v-if="commentLimit < lecturer.comments.length">
                    <v-flex xs6 offset-xs3>
                      <v-btn color="orange" @click="commentLimit += 3">Load More</v-btn>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-spacer></v-spacer>
                <v-flex xs6>
                  <v-container grid-list-sm fluid>
                    <v-layout row wrap>
                      <v-flex
                        v-for="(n, i) in lecturer.grade_distributions.slice(0,gradeDistributionLimit)"
                        :key="i"
                        xs12
                        d-flex
                      >
                        <v-card flat tile class="d-flex">
                          <grade-distribution-dialog
                            :n="n"
                            :index="i"
                          ></grade-distribution-dialog>
                        </v-card>
                      </v-flex>
                    </v-layout>
                    </v-container>
                  <v-layout row justify-center v-if="gradeDistributionLimit < lecturer.grade_distributions.length">
                    <v-flex xs6 offset-xs3>
                      <v-btn color="orange" @click="gradeDistributionLimit += 2">Load More</v-btn>
                    </v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-container>
            <v-card-actions>
              <v-btn flat color="red">Report</v-btn>
              <v-divider></v-divider>
              <edit-lecturer-dialog
                :lecturer="lecturer"
              ></edit-lecturer-dialog>
              <delete-lecturer-dialog
                :lecturer="lecturer"
              ></delete-lecturer-dialog>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
  import AddGradeDistributionDialog from "../GradeDistribution/Create";
  import AddCommentDialog from "../Comment/LecturerComment";
  import GradeDistributionDialog from '../Dialogs/GradeDistribution'
  import EditLecturerDialog from './EditLecturerDialog'
  import DeleteLecturerDialog from './DeleteLecturerDialog'

  export default {
    name: "Lecturer",
    components: {
      DeleteLecturerDialog,
      AddGradeDistributionDialog, AddCommentDialog, GradeDistributionDialog, EditLecturerDialog},
    metaInfo: {
      // title will be injected into parent titleTemplate
      title: "Lecturer"
    },
    data() {
      return {
        commentLimit: 3,
        gradeDistributionLimit: 2,
      }
    },
    beforeCreate(){
      let lecturer_slug = this.$route.params.lecturer_slug
      this.$store.dispatch('getLecturer', lecturer_slug)
    },
    computed: {
      lecturer(){
        return this.$store.getters.lecturer
      },
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      user(){
        return this.$store.getters.user
      },
      userIsAdmin(){
        return this.userIsAuthenticated && this.user.admin === true;
      }
    },
    methods: {
      deleteComment(comment_id, index){
        const deleteComment = {
          comment_id: comment_id,
          lecturer_id: this.lecturer.id,
          comment_index: index
        }

        console.log(deleteComment)

        if(this.userIsAdmin){
          this.$store.dispatch('adminDeleteLecturerComment', deleteComment)
        }else{
          this.$store.dispatch('deleteLecturerComment', deleteComment)
        }
      }
    }
  }
</script>

<style scoped>
  .lecturer-title{
    font-size: 23px;
  }
</style>
