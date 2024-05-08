<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar app color="primary">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>My Vuetify 3 App</v-toolbar-title>
    </v-app-bar>

    <!-- Drawer -->
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-account</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Profile</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container>
        <HelloWorld/>
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app>
      <span>&copy; 2024 My Vuetify App</span>
    </v-footer>
  </v-app>
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  components: {HelloWorld},
  data() {
    return {
      drawer: true, // Set this to true to make the drawer visible by default
    };
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
