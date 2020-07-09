<template>
  <v-container>
    <v-layout>
      <v-flex>
        <v-card>
          <v-card-title>
            <h2>Types</h2>
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
      ]
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
  },
};
</script>
