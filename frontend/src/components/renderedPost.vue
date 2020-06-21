<template>
  <v-card
    width="500px"
  >
    <v-card-title>
      <div>
        <p class="headline">
          {{ projectName }}
        </p>
        <p class="mb-0">
          {{ text }}
        </p>
      </div>
    </v-card-title>

    <v-img
      v-if="img"
      :src="img"
    />

    <v-card-actions>
      <v-btn
        flat
        color="#98ee99"
      >
        Accept
      </v-btn>
      <v-btn
        flat
        color="#ff867c"
      >
        Discard
      </v-btn>
      <v-btn
        flat
        color="#43C1DF"
      >
        Settings
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    projectName: String,
    text: String,
    img: String
  },
  data() {
    return {
    };
  },
};
</script>
