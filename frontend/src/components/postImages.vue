<template>
  <div>
    <v-img
      v-if="links.length === 1"
      :src="links[0]"
      :max-width="`${width}px`"
    />

    <v-carousel
      v-else-if="links.length > 1"
      :max="width"
      :cycle="false"
    >
      <v-carousel-item
        v-for="(link, i) in links"
        :key="i"
        :src="link"
      />
    </v-carousel>
  </div>
</template>

<script>
export default {
  props: {
    width: {
      type: String,
      default: '500',
    },
    links: {
      type: Array,
      default() {
        return [];
      }
    }
  },
  data() {
    return {
    };
  },
};
</script>
