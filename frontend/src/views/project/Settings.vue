<template>
  <v-container>
    <v-layout>
      <v-flex>
        <v-card>
          <v-card-title>
            <h2>Sources</h2>
            <v-spacer />
            <v-btn
              color="#43C1DF"
              dark
              @click="addSourceDialog = true"
            >
              Add new source
            </v-btn>
            <v-btn
              color="#43C1DF"
              dark
              @click="addSourceByURLDialog = true"
            >
              Add new source by url
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :items="sources"
              :headers="sourceHeaders"
              :pagination.sync="sourcePagination"
              :total-items="totalSources"
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
                  <v-btn fab small color="red" @click="deleteSource(props.item)">
                    <v-icon>delete</v-icon>
                  </v-btn>
                </td>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <v-layout
      class="mt-4"
    >
      <v-flex>
        <v-card>
          <v-card-title>
            <h2>Token</h2>
            <v-spacer />
            <v-btn
              color="#43C1DF"
              dark
              @click="editTokenDialog = true"
            >
              Edit token
            </v-btn>
          </v-card-title>
          <v-card-text class="text-hidden">
            {{ project.token }}
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <v-layout class="mt-4">
      <v-flex>
        <v-card>
          <v-card-title>
            <h2>Platform Id</h2>
            <v-spacer />
            <v-btn
              color="#43C1DF"
              dark
              @click="editPlatformIdDialog = true"
            >
              Edit Platform Id
            </v-btn>
          </v-card-title>
          <v-card-text>
            {{ project.platform_id }}
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <!-- Edit Platform Id form -->
    <v-dialog
      v-model="editPlatformIdDialog"
      max-width="600px"
    >
      <v-card
        class="px-3"
      >
        <v-card-title>
          <h2>Edit Platform Id</h2>
        </v-card-title>

        <v-card-text>
          <v-layout>
            <v-flex xs12>
              <v-text-field
                label="Platform Id"
                v-model="newPlatformId"
              />
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-actions>
          <v-btn flat color="#98ee99" @click="editPlatformId()">Edit</v-btn>
          <v-btn flat color="#ff867c" @click="newPlatformId='';editPlatformIdDialog=false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Edit token form -->
    <v-dialog
      v-model="editTokenDialog"
      max-width="600px"
    >
      <v-card
        class="px-3"
      >
        <v-card-title>
          <h2>Edit token</h2>
        </v-card-title>

        <v-card-text>
          <v-layout>
            <v-flex xs12>
              <v-text-field
                label="Token"
                v-model="newToken"
              />
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-actions>
          <v-btn flat color="#98ee99" @click="editToken()">Edit</v-btn>
          <v-btn flat color="#ff867c" @click="newToken='';editTokenDialog=false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Create source form -->
    <v-dialog
      v-model="addSourceDialog"
      max-width="600px"
    >
      <v-card
        class="px-3"
      >
        <v-card-title>
          <h2>Add new source</h2>
        </v-card-title>

        <v-card-text>
          <v-layout>
            <v-flex xs12>
              <v-text-field
                label="Source name"
                v-model="newSource.name"
              />
            </v-flex>
          </v-layout>
          <v-layout>
            <v-flex xs12>
              <v-text-field
                label="Platform id"
                v-model="newSource.platform_id"
              />
            </v-flex>
          </v-layout>
          <v-layout>
            <v-flex xs12>
              <v-select
                :items="types"
                v-model="newSource.type_id"

                label="Type of source"
                item-text="name"
                item-value="id"
              />
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-actions>
          <v-btn flat color="#98ee99" @click="addSource()">Add</v-btn>
          <v-btn flat color="#ff867c" @click="clearNewSource()">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="addSourceByURLDialog"
      max-width="600px"
    >
      <v-card
        class="px-3"
      >
        <v-card-title>
          <h2>Add new source by url</h2>
        </v-card-title>

        <v-card-text>
          <v-layout>
            <v-flex xs12>
              <v-text-field
                label="Source url"
                v-model="newSourceByURL.url"
              />
            </v-flex>
          </v-layout>
          <v-layout>
            <v-flex xs12>
              <v-select
                :items="types"
                v-model="newSourceByURL.type_id"

                label="Type of source"
                item-text="name"
                item-value="id"
              />
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-actions>
          <v-btn flat color="#98ee99" @click="addSourceByURL()">Add</v-btn>
          <v-btn flat color="#ff867c" @click="clearNewSourceByURL()">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
      totalSources: 0,
      sourcePagination: {},
      newSource: {
        name: '',
        type_id: undefined,
        platform_id: '',
        project_id: undefined,
      },
      newSourceByURL: {
        url: '',
        type_id: undefined,
        project_id: undefined,
      },

      types: [],
      project: {},

      sourceHeaders: [
        { text: 'Name', value: 'name' },
        { text: 'Platform id', value: 'platform_id', sortable: false },
        { text: 'Type of source', value: 'type_id' },
        { text: 'Actions', sortable: false, align: 'center' },
      ],
      addSourceDialog: false,
      addSourceByURLDialog: false,

      newPlatformId: '',
      editPlatformIdDialog: false,

      newToken: '',
      editTokenDialog: false,
    };
  },
  watch: {
    sourcePagination: {
      handler() {
        this.setSources();
      },
      deep: true,
    },
  },
  created() {
    this.setTypes()
      .then(() => {
        this.setProject();
        this.setSources();
      });
  },
  methods: {
    async setProject() {
      this.project = await this.getProjectById(this.projectId);
    },
    async getProjectById(projectId) {
      const resp = await this.$axios.get(`/api/1.0/projects/${projectId}`);
      const project = resp.data;
      return project;
    },
    async setSources() {
      const [sources, totalSources] = await this.getSources(this.projectId, this.sourcePagination);

      this.sources = sources;
      this.totalSources = totalSources;
    },
    async getSources(projectId, pagination) {
      const resp = await this.$axios.get('/api/1.0/sources/', {
        params: {
          project_id: projectId,
          page: pagination.page,
          count: pagination.rowsPerPage,
        }
      });

      const sources = resp.data.results;
      const totalSources = resp.data.meta.total;
      return [sources, totalSources];
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
      const resp = await this.$axios.delete(`/api/1.0/sources/${source.id}/`);

      if (resp.status === 204) {
        console.log('Source deleted');
        this.setSources();
      }
      console.log(resp);
    },
    async addSource() {
      this.newSource.project_id = this.projectId;

      const resp = await this.$axios.post('/api/1.0/sources/', this.newSource);

      if (resp.status === 201) {
        console.log('Source added');
        this.clearNewSource();
        this.addSourceDialog = false;
        this.setSources();
      }
    },
    async addSourceByURL() {
      this.newSourceByURL.project_id = this.projectId;

      const resp = await this.$axios.post('/api/1.0/sources/', this.newSourceByURL);

      if (resp.status === 201) {
        console.log('Source added');
        this.clearNewSourceByURL();
        this.addSourceByURLDialog = false;
        this.setSources();
      }
    },
    clearNewSource() {
      this.newSource = {
        name: '',
        type_id: undefined,
        platform_id: '',
        project_id: undefined,
      };
    },
    clearNewSourceByURL() {
      this.newSourceByURL = {
        url: '',
        type_id: undefined,
        project_id: undefined,
      };
    },
    async editToken() {
      const resp = await this.$axios.patch(`/api/1.0/projects/${this.project.id}/`,
        {
          token: this.newToken,
        });

      if (resp.status === 200) {
        console.log('Token was updated');
        this.newToken = '';
        this.editTokenDialog = false;
        this.setProject();
      }
    },
    async editPlatformId() {
      const resp = await this.$axios.patch(`/api/1.0/projects/${this.project.id}/`,
        {
          platform_id: this.newPlatformId
        });

      if (resp.status === 200) {
        console.log('Platform id was updated');
        this.newPlatformId = '';
        this.editPlatformIdDialog = false;
        this.setProject();
      }
    },

    formatType(id) {
      const type = this.types.find((t) => t.id === id);
      return type.name;
    }
  },
};
</script>

<style scope>
.text-hidden {
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
