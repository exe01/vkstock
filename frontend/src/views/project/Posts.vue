<template>
  <v-container style="width: 100%">
    <v-layout
      justify-center
    >
      <v-flex xs6>
        <rendered-post />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import RenderedPost from '@/components/renderedPost.vue';

export default {
  components: {
    RenderedPost,
  },
  data() {
    return {
    };
  },
};
</script>
