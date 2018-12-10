<template>
  <v-app dark>
    <v-navigation-drawer
      :mini-variant="miniVariant"
      :clipped="clipped"
      v-model="drawer"
      fixed
      app
    >
      <v-list>
        <v-list-tile
          router
          :to="item.to"
          :key="i"
          v-for="(item, i) in menuItems"
          exact
        >
          <v-list-tile-action>
            <v-icon v-html="item.icon"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="item.title"></v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile
          router
          exact
          @click="logout"
          v-if="userIsAuthenticated"
        >
          <v-list-tile-action>
            <v-icon>exit_to_app</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Logout</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar fixed>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
    </v-toolbar>
    <v-toolbar fixed app :clipped-left="clipped">
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-btn
        icon
        @click.native.stop="miniVariant = !miniVariant"
      >
        <v-icon v-html="miniVariant ? 'chevron_right' : 'chevron_left'"></v-icon>
      </v-btn>
      <v-btn
        icon
        @click.native.stop="clipped = !clipped"
      >
        <v-icon>web</v-icon>
      </v-btn>
      <v-btn
        icon
        @click.native.stop="fixed = !fixed"
      >
        <v-icon>remove</v-icon>
      </v-btn>
      <v-toolbar-title v-text="title"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        icon
        @click.native.stop="rightDrawer = !rightDrawer"
        v-if="userIsAuthenticated && user.admin === true"
      >
        <v-icon>menu</v-icon>
      </v-btn>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <v-layout row v-if="errors">
          <v-flex xs12 sm6 offset-sm3>
            <app-alert v-for="(err, index) in errors" :data="err" :key="index" @dismissed="onDismissed" :text="err"></app-alert>
          </v-flex>
          </v-layout>
        <v-slide-y-transition mode="out-in">
          <router-view></router-view>
        </v-slide-y-transition>
      </v-container>
    </v-content>
    <v-navigation-drawer
      temporary
      :right="right"
      v-model="rightDrawer"
      fixed
      v-if="userIsAuthenticated && user.admin === true"
    >
      <v-list>
        <v-list-tile v-for="(item, i) in adminItems" :to="item.to" :data="item" :key="i">
          <v-list-tile-action>
            <v-icon light>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-footer :fixed="fixed" app>
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>
  import Meta from 'mixins/meta'

  export default {
    components: {},
    mixins: [Meta],
    metaInfo: {
      // if no subcomponents specify a metaInfo.title, this title will be used
      title: 'Notes',
      // all titles will be injected into this template
      titleTemplate: '%s | Petek'
    },
    data () {
      return {
        clipped: false,
        drawer: true,
        fixed: false,
        miniVariant: false,
        right: true,
        rightDrawer: false,
        title: 'Vuetify.js'
      }
    },
    computed: {
      userIsAuthenticated(){
        return this.user !== null && this.user !== undefined;
      },
      user(){
        return this.$store.getters.user;
      },
      adminItems(){
        return [
          { icon: 'reorder', title: 'Notes', to:'/admin/notes' },
          { icon: 'face', title: 'Users', to:'/admin/users' },
        ]
      },
      menuItems(){
        let menuItems = [
          { icon: 'apps', title: 'Home', to: '/' },
          { icon: 'reorder', title: 'Notes', to: '/notes' },
          { icon: 'portrait', title: 'Lecturers', to: '/lecturers' },
          { icon: 'face', title: 'Register', to: '/register' },
          { icon: 'lock_open', title: 'Login', to: '/login' },
        ];
        if(this.userIsAuthenticated){
            menuItems = [
                { icon: 'apps', title: 'Home', to: '/' },
                { icon: 'reorder', title: 'Notes', to: '/notes' },
              { icon: 'portrait', title: 'Lecturers', to: '/lecturers' },
              { icon: 'person', title: 'Profile', to: `/users/${this.user.slug}`},
            ]
        }
        return menuItems;
      },
      errors () {
        return this.$store.getters.error
      },
    },
    methods: {
      logout() {
        this.$store.dispatch('logout')
      },
      onDismissed () {
        this.$store.dispatch('clearError');
      }
    }
  }
</script>
