<template>
  <v-container>
    <v-layout>
      <v-flex>
        <v-card>
          <v-card-title>
            <h2>Sources</h2>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :items="sources"
              :headers="sourceHeaders"
            >
              <template v-slot:items="props">
                <td>{{ props.item.name }}</td>
                <td>{{ props.item.platform_id }}</td>
                <td>{{ formatType(props.item.type_id) }}</td>
                <!-- Actions -->
                <td class="justify-center align-center layout px-0">
                  <v-btn fab small color="warning">
                    <v-icon>edit</v-icon>
                  </v-btn>
                  <v-btn fab small color="#43C1DF">
                    <v-icon>pause</v-icon>
                  </v-btn>
                  <v-btn fab small color="red">
                    <v-icon>delete</v-icon>
                  </v-btn>
                </td>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  props: {
    projectId: Number
  },
  data() {
    return {
      sources: [],
      types: [],
      project: {},

      sourceHeaders: [
        { text: 'Name', value: 'name' },
        { text: 'Platform id', value: 'platform_id', sortable: false },
        { text: 'Type of source', value: 'type_id' },
        { text: 'Actions', sortable: false, align: 'center' },
      ]
    };
  },
  created() {
    this.setTypes()
      .then(() => {
        this.setProject(this.projectId);
        this.setSources(this.projectId);
      });
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
    async setSources(projectId) {
      this.sources = await this.getSources(projectId);
    },
    async getSources(projectId) {
      const resp = await this.$axios.get('/api/1.0/sources/', {
        params: {
          project_id: projectId
        }
      });

      const sources = resp.data.results;
      return sources;
    },
    async setTypes() {
      this.types = await this.getTypes();
    },
    async getTypes() {
      const resp = await this.$axios.get('/api/1.0/types/');
      const types = resp.data.results;
      return types;
    },
    async editSource(source) {
      console.log(source);
    },
    async deleteSource(source) {
      console.log(source);
    },

    formatType(id) {
      const type = this.types.find((t) => t.id === id);
      return type.name;
    }
  },
};
</script>
