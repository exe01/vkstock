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
          <p class="mb-0">{{ post.text }}</p>
        </div>
      </v-card-title>

      <post-images
        :links="renderImgLinks(post.images || [])"
      />

      <v-card-actions>
        <v-btn flat color="#98ee99">Accept</v-btn>
        <v-btn flat color="#ff867c">Discard</v-btn>
        <v-btn flat color="#43C1DF" @click="openSettingDialog()">Settings</v-btn>
      </v-card-actions>
    </v-card>

    <v-dialog
      v-if="settingDialog"
      v-model="settingDialog"
      max-width="600px"
    >
      <v-card
        class="px-3"
      >
        <v-card-title>
          <div>
            <p class="headline">{{ projectName }}</p>
            <p class="mb-0">{{ post.text }}</p>
          </div>
        </v-card-title>

        <v-img
          v-for="(imgLink, i) in renderImgLinks(post.images)"
          :key="i"
          :src="imgLink"
        />

        <v-card-text>
          <v-divider class="mb-3" />

          <p>{{ originalPost.text }}</p>

          <post-images
            :links="renderImgLinks(originalPost.images || [])"
            width="300"
          />

          <v-divider class="mt-3" />

          <v-checkbox
            v-for="(comment, i) in originalPost.comments"
            :key="i"
            v-model="checkboxModel"
            :label="comment.text"
          />
        </v-card-text>

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
import PostImages from './postImages.vue';

export default {
  props: {
    post: {
      type: Object,
      default() {
        return {};
      },
    },
    projectName: String,
  },
  components: {
    PostImages,
  },
  data() {
    return {
      settingDialog: false,
      originalPost: {},
      checkboxModel: false,
    };
  },
  methods: {
    async openSettingDialog() {
      this.originalPost = await this.getOriginalPost(this.post.post_id);
      this.settingDialog = true;
    },
    async getOriginalPost(postId) {
      const resp = await this.$axios.get(`api/1.0/posts/${postId}`);
      const originalPost = resp.data;
      originalPost.images = originalPost.images || [];
      return originalPost;
    },
    renderImgLinks(images) {
      const { baseURL } = this.$axios.defaults;
      const imgLinks = images.map((i) => `${baseURL}api/images/${i.path}`);
      return imgLinks;
    }
  }
};
</script>
