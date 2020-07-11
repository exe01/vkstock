<template>
  <v-container>
    <v-layout>
      <v-flex>
        <v-card>
          <v-card-title>
            <h2>Types</h2>
            <v-spacer />
            <v-btn
              color="#43C1DF"
              dark
              @click="createTypeDialog = true"
            >
              Create new type
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :items="types"
              :headers="typeHeaders"
              :total-items="totalTypes"
            >
              <template v-slot:items="props">
                <td>{{ props.item.name }}</td>
                <td>{{ props.item.token }}</td>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <!-- Create type form -->
    <v-dialog
      v-model="createTypeDialog"
      max-width="600px"
    >
      <v-card
        class="px-3"
      >
        <v-card-title>
          <h2>Create new type</h2>
        </v-card-title>

        <v-card-text>
          <v-layout>
            <v-flex xs12>
              <v-text-field
                label="Type name"
                v-model="newType.name"
              />
            </v-flex>
          </v-layout>
          <v-layout>
            <v-flex xs12>
              <v-text-field
                label="Token"
                v-model="newType.token"
              />
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-actions>
          <v-btn flat color="#98ee99" @click="createType()">Add</v-btn>
          <v-btn flat color="#ff867c" @click="clearNewType()">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      types: [],
      totalTypes: 0,
      typeHeaders: [
        { text: 'Name', value: 'name' },
        { text: 'Token', value: 'token', sortable: false },
      ],

      newType: {
        name: '',
        token: '',
      },
      createTypeDialog: false,
    };
  },
  created() {
    this.setTypes();
  },
  methods: {
    async setTypes() {
      const [types, totalTypes] = await this.getTypes();

      this.types = types;
      this.totalTypes = totalTypes;
    },
    async getTypes() {
      const resp = await this.$axios.get('/api/1.0/types/');

      const totalTypes = resp.data.meta.total;
      const types = resp.data.results;
      return [types, totalTypes];
    },
    async createType() {
      const resp = await this.$axios.post('/api/1.0/types/', this.newType);

      if (resp.status === 201) {
        console.log('Type created');
        this.clearNewType();
        this.createTypeDialog = false;
        this.setTypes();
      }
    },

    clearNewType() {
      this.newType = {
        name: '',
        token: '',
      };
    }
  },
};
</script>
