<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-xs-center">
        <img src="/static/v.png" alt="Vuetify.js" class="mb-5" />
      </div>
      <v-card>
        <v-card-text>
          <p>Welcome to the Petek Project.</p>
          <p>Not Kutusu has been built for ITU students to find the desired course notes easily. Before sharing a course note, you need to fill the inputs such as drive/cloud link, lecturer and course code informations. In that way, another student can search any course note easily by entering its code or lecturer. </p>
          <p>Thank you for using Petek and I look forward to bringing more exciting features in the future.</p>
          <div class="text-xs-right">
            <em><small>&mdash; Ali Tolga Dinçer & Yavuz Koca</small></em>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" flat router to="/inspire">Continue</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>
