<template>
  <div id="app">
    <v-app
      id="inspire"
      dark
    >
      <!-- Left menu -->
      <v-navigation-drawer
        clipped
        fixed
        v-model="drawer"
        app
      >
        <v-toolbar
          flat
          class="transparent"
        >
          <!-- User info -->
          <v-list
            class="pa-0"
          >
            <v-list-tile avatar>
              <v-list-tile-avatar>
                <img src="https://randomuser.me/api/portraits/men/85.jpg">
              </v-list-tile-avatar>

              <v-list-tile-content>
                <v-list-tile-title>User name</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-toolbar>

        <!-- Menu -->
        <v-list dense>
          <v-list-group
            prepend-icon="folder"
            active-class="navigation-bar__active-tab"
            :value="false"
          >
            <template v-slot:activator>
              <v-list-tile>
                <v-list-tile-title>Projects</v-list-tile-title>
              </v-list-tile>
            </template>

            <v-list-tile
              v-for="(project, key) in projects"
              :key="key"
              class="ml-3"
              @click="goToProjectView(project)"
            >
              <v-list-tile-title>{{ project.name }}</v-list-tile-title>
            </v-list-tile>
          </v-list-group>

          <v-list-tile
            @click="$router.push('/settings')"
          >
            <v-list-tile-action>
              <v-icon>settings</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Settings</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-navigation-drawer>

      <!-- Top menu -->
      <v-toolbar
        app
        fixed
        clipped-left
      >
        <v-toolbar-side-icon @click.stop="drawer = !drawer" />
        <v-toolbar-title>Stock</v-toolbar-title>
      </v-toolbar>

      <!-- Main content -->
      <v-content>
        <router-view :key="$route.fullPath" />
      </v-content>

      <!-- Footer -->
      <v-footer
        app
        fixed
      >
        <span>&copy; 2020 exe01</span>
      </v-footer>
    </v-app>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
      projects: [],
    };
  },
  created() {
    this.setProjects();
  },
  methods: {
    async setProjects() {
      this.projects = await this.getProjects();
    },
    async getProjects() {
      const resp = await this.$axios.get('api/1.0/projects');
      const projects = resp.data.results;
      return projects;
    },
    goToProjectView(project) {
      this.$router.push({ name: 'projects', params: { id: project.id } }).catch(() => {});
    }
  }
};
</script>

<style>
.navigation-bar__active-tab {
  color: #43C1DF
}
</style>
