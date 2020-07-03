<template>
  <v-container
    style="width: 100%"
    grid-list-xl
  >
    <!-- Sorting card -->
    <v-layout>
      <v-flex>
        <v-card>
          <v-card-text>
            <v-layout>
              <v-flex xs4>
                <v-select
                  v-model="status"
                  :items="statuses"
                  item-text="name"
                  item-value="value"

                  return-object

                  label="Statuses"
                  box
                  hide-details
                  color="#43C1DF"
                />
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <v-layout justify-center>
      <v-flex>
        <div class="text-xs-center">
          <v-pagination
            v-model="currentPage"
            :length="totalPages"

            color="#43C1DF"
          />
        </div>
      </v-flex>
    </v-layout>

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
          :post="post"
          :project-name="project.name"
        />
      </v-flex>
    </v-layout>

    <v-layout justify-center>
      <v-flex>
        <div class="text-xs-center">
          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            color="#43C1DF"
          />
        </div>
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
      currentPage: 1,
      totalPages: 1,

      status: { value: 'UN', name: 'Unaccepted' },
      statuses: [
        { value: 'UN', name: 'Unaccepted' },
        { value: 'AC', name: 'Accepted' },
        { value: 'RE', name: 'Rejected' },
        { value: 'PO', name: 'Posted' },
      ],

      project: {},
      renderedPosts: [],
    };
  },
  created() {
    this.setProject(this.projectId)
      .then(() => { this.setRenderedPosts(); });
  },
  watch: {
    currentPage() {
      this.setRenderedPosts();
    },
    status() {
      this.setRenderedPosts();
    }
  },
  methods: {
    async setProject(projectId) {
      this.project = await this.getProjectById(projectId);
    },
    async setRenderedPosts() {
      const { projectId, status } = this;

      this.renderedPosts = await this.getRenderedPosts(projectId, status.value);
    },
    async getProjectById(projectId) {
      const resp = await this.$axios.get(`api/1.0/projects/${projectId}`);
      const project = resp.data;
      return project;
    },
    async getRenderedPosts(projectId, status) {
      const resp = await this.$axios.get('api/1.0/rendered_posts', {
        params: {
          project_id: projectId,
          page: this.currentPage,
          status,
        },
      });

      this.totalPages = resp.data.meta.all_pages;

      const renderedPosts = resp.data.results;
      return renderedPosts;
    },
  }
};
</script>
