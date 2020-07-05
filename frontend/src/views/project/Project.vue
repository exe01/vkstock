<template>
  <v-container
    class="pa-0"
    fluid
  >
    <!-- Project header -->
    <v-layout
      class="dark-background"
    >
      <v-flex>
        <p
          class="display-2 ma-3"
        >
          {{ project.name }}
        </p>
      </v-flex>
    </v-layout>

    <!-- Tab headers -->
    <v-layout>
      <v-flex>
        <v-tabs
          v-model="tabIndex"
          grow
        >
          <v-tabs-slider color="white" />

          <v-tab
            v-for="header in tabHeaders"
            :key="header"
          >
            {{ header }}
          </v-tab>
        </v-tabs>
      </v-flex>
    </v-layout>

    <!-- Tab content -->
    <v-layout>
      <v-flex>
        <v-tabs-items v-model="tabIndex">
          <v-tab-item>
            <posts
              :project-id="projectId"
            />
          </v-tab-item>
          <v-tab-item>
            <settings
              :project-id="projectId"
            />
          </v-tab-item>
          <v-tab-item>
            <statistics />
          </v-tab-item>
        </v-tabs-items>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Posts from './Posts.vue';
import Settings from './Settings.vue';
import Statistics from './Statistics.vue';

export default {
  components: {
    Posts,
    Settings,
    Statistics
  },
  data() {
    return {
      projectId: null,
      project: {},
      tabIndex: null,
      tabHeaders: [
        'Posts', 'Settings', 'Statistics'
      ],
    };
  },
  created() {
    // eslint-disable-next-line radix
    this.projectId = parseInt(this.$route.params.id);
    this.setProject(this.projectId);
  },
  methods: {
    async setProject(projectId) {
      this.project = await this.getProjectById(projectId);
    },
    async getProjectById(projectId) {
      const resp = await this.$axios.get(`api/1.0/projects/${projectId}`);
      const project = resp.data;
      return project;
    },
  }
};
</script>

<style scoped>
  .dark-background {
    background-color: #424242;
  }
</style>
