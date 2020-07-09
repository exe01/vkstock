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
              <v-list-tile-action>
                <v-icon />
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>{{ project.name }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile
              @click="createNewProjectDialog=true; drawer=false"
              class="ml-3"
            >
              <v-list-tile-action>
                <v-icon>add_circle</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>Create new project</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list-group>

          <v-list-tile
            @click="$router.push({ name: 'settings' })"
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

      <v-dialog
        v-model="createNewProjectDialog"
        max-width="600px"
      >
        <v-card
          class="px-3"
        >
          <v-card-title>
            <h2>Create new project</h2>
          </v-card-title>

          <v-card-text>
            <v-layout>
              <v-flex xs12>
                <v-text-field
                  label="Project name"
                  v-model="newProject.name"
                />
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex xs12>
                <v-text-field
                  label="Token"
                  v-model="newProject.token"
                />
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex xs12>
                <v-select
                  :items="types"
                  v-model="newProject.type_id"

                  label="Type of project"
                  item-text="name"
                  item-value="id"
                />
              </v-flex>
            </v-layout>
          </v-card-text>

          <v-card-actions>
            <v-btn flat color="#98ee99" @click="createProject()">Add</v-btn>
            <v-btn flat color="#ff867c" @click="clearNewProject(); createNewProjectDialog=false">Cancel</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-app>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
      createNewProjectDialog: false,
      projects: [],

      types: [],
      newProject: {
        name: '',
        token: '',
        type_id: ''
      },
    };
  },
  created() {
    this.setProjects();
    this.setTypes();
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
    },
    async setTypes() {
      this.types = await this.getTypes();
    },
    async getTypes() {
      const resp = await this.$axios.get('/api/1.0/types/');
      const types = resp.data.results;
      return types;
    },

    async createProject() {
      const resp = await this.$axios.post('/api/1.0/projects/', this.newProject);

      if (resp.status === 201) {
        console.log('Project added');
        this.clearNewProject();
        this.createNewProjectDialog = false;
        this.setProjects();
      }
    },
    clearNewProject() {
      this.newProject = {
        name: '',
        token: '',
        type_id: ''
      };
    }
  }
};
</script>

<style>
.navigation-bar__active-tab {
  color: #43C1DF
}
</style>
