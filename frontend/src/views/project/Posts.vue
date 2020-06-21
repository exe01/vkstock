<template>
  <v-container
    style="width: 100%"
    grid-list-xl
  >
    <v-layout
      column
      align-center
      justify-start
      fill-height
    >
      <v-flex
        v-for="(post, index) in renderedPosts"
        :key="index"
      >
        <rendered-post
          :project-name="project.name"
          :img="'http://localhost:8000/api/images/123'"
          :text="post.text"
        />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import RenderedPost from '@/components/renderedPost.vue';

export default {
  props: {
    projectId: Number
  },
  components: {
    RenderedPost,
  },
  data() {
    return {
      project: {},
      renderedPosts: [],
    };
  },
  created() {
    this.setProject(this.projectId)
      .then(() => { this.setRenderedPosts(this.projectId); });
  },
  methods: {
    async setProject(projectId) {
      this.project = await this.getProjectById(projectId);
    },
    async setRenderedPosts(projectId) {
      this.renderedPosts = await this.getRenderedPosts(projectId);
    },
    async getProjectById(projectId) {
      const resp = await this.$axios.get(`api/1.0/projects/${projectId}`);
      const project = resp.data;
      return project;
    },
    async getRenderedPosts(projectId) {
      const resp = await this.$axios.get('api/1.0/rendered_posts', {
        params: {
          project_id: projectId,
        },
      });
      const renderedPosts = resp.data.results;
      return renderedPosts;
    },
  }
};
</script>
