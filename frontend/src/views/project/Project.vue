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
          <v-tab-item
            v-for="header in tabHeaders"
            :key="header"
          >
            <posts />
          </v-tab-item>
        </v-tabs-items>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Posts from './Posts.vue';

export default {
  components: {
    Posts
  },
  data() {
    return {
      project: {},
      tabIndex: null,
      tabHeaders: [
        'Posts', 'Settings', 'Statistics'
      ],
    };
  },
  created() {
    const projectId = this.$route.params.id;
    this.project = this.getProjectById(projectId);
  },
  methods: {
    getProjectById(id) {
      return {
        name: 'Project name',
        id
      };
    }
  }
};
</script>

<style scoped>
  .dark-background {
    background-color: #424242;
  }
</style>
