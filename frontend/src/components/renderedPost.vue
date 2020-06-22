/* eslint-disable vue/max-attributes-per-line */
/* eslint-disable vue/singleline-html-element-content-newline */
<template>
  <div>
    <v-card
      width="500px"
    >
      <v-card-title>
        <div>
          <p class="headline">{{ projectName }}</p>
          <p class="mb-0">{{ text }}</p>
        </div>
      </v-card-title>

      <v-img
        v-for="img in images"
        :key="img"
        :src="img"
      />

      <v-card-actions>
        <v-btn flat color="#98ee99">Accept</v-btn>
        <v-btn flat color="#ff867c">Discard</v-btn>
        <v-btn flat color="#43C1DF" @click="settingDialog = true">Settings</v-btn>
      </v-card-actions>
    </v-card>

    <v-dialog
      v-model="settingDialog"
      max-width="500px"
    >
      <v-card>
        <v-card-title>
          <div>
            <p class="headline">{{ projectName }}</p>
            <p class="mb-0">{{ text }}</p>
          </div>
        </v-card-title>

        <v-img
          v-for="img in images"
          :key="img"
          :src="img"
        />

        <v-card-actions>
          <v-btn flat color="#98ee99">Accept</v-btn>
          <v-btn flat color="#ff867c">Discard</v-btn>
          <v-btn flat color="#43C1DF">Settings</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  props: {
    projectName: String,
    text: String,
    images: {
      type: Array,
      default() {
        return [];
      }
    }
  },
  data() {
    return {
      settingDialog: false,
    };
  },
};
</script>
