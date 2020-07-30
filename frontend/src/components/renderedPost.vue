/* eslint-disable no-restricted-syntax */
/* eslint-disable vue/max-attributes-per-line */
/* eslint-disable vue/singleline-html-element-content-newline */
<template>
  <v-flex style="width: 500px">
    <v-card
      max-width="500px"
      md12
      xs12
      lg12
      xl12
    >
      <v-card-title>
        <div>
          <p class="headline">{{ projectName }}</p>
          <p class="mb-0">{{ post.text }}</p>
        </div>
      </v-card-title>

      <post-images
        :links="formatImgLinks(post.images || [])"
      />

      <v-card-actions>
        <v-btn :flat="post.status!='AC'" color="#98ee99" @click="updateStatus('AC')">Accept</v-btn>
        <v-btn :flat="post.status!='RE'" color="#ff867c" @click="updateStatus('RE')">Reject</v-btn>
        <v-btn flat color="#43C1DF" @click="openSettingDialog()">Settings</v-btn>
      </v-card-actions>

      <v-divider />

      <div>
        <span class="grey--text caption ma-2 font-italic">id: {{ post.id }}</span>
      </div>
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
          v-for="(imgLink, i) in formatImgLinks(post.images)"
          :key="i"
          :src="imgLink"
        />

        <v-card-text>
          <v-divider class="mb-3" />

          <v-layout
            align-center
          >
            <v-flex xs1>
              <v-checkbox
                v-model="selectedOriginalText"
              />
            </v-flex>
            <v-flex xs11>
              <v-textarea
                auto-grow
                rows="1"
                v-model="originalPost.text"
                @change="originalPostTextChanged = true"
              />
            </v-flex>
          </v-layout>

          <v-layout
            align-center
          >
            <v-flex xs1>
              <v-checkbox
                v-model="selectedOriginalImage"
              />
            </v-flex>
            <v-flex xs11>
              <post-images
                :links="formatImgLinks(originalPost.images || [])"
                width="300"
              />
            </v-flex>
          </v-layout>

          <v-divider class="mt-3" />

          <v-layout
            v-for="comment in originalPost.comments"
            :key="comment.id"
            align-center
          >
            <v-flex xs1>
              <v-checkbox
                v-model="selectedComments[comment.id]"
                @change="selectComment(comment.id)"
              />
            </v-flex>
            <v-flex xs11>
              <v-textarea
                v-if="comment.ref_text != ''"
                auto-grow
                rows="1"
                v-model="comment.ref_text"
                @change="changedComments[comment.id] = true"
              />
              <v-textarea
                auto-grow
                rows="1"
                v-model="comment.text"
                @change="changedComments[comment.id] = true"
              />
              <v-img
                max-width="300"
                v-if="comment.image"
                :src="'/media/'+comment.image"
              />
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-actions>
          <v-btn flat color="#98ee99" @click="rerendPost()">Rerend</v-btn>
          <v-btn flat color="#43C1DF" @click="rerendAsOriginal()">Rend as original</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-flex>
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
      originalPostTextChanged: false,

      changedComments: {},

      selectedComments: {},
      selectedOriginalText: true,
      selectedOriginalImage: true,
    };
  },
  methods: {
    async openSettingDialog() {
      this.originalPost = await this.getOriginalPost(this.post.post_id);
      this.settingDialog = true;
    },
    async getOriginalPost(postId) {
      const resp = await this.$axios.get(`/api/1.0/posts/${postId}`);
      const originalPost = resp.data;
      originalPost.images = originalPost.images || [];
      return originalPost;
    },
    async updateOriginalPost() {
      const { id } = this.originalPost;

      const resp = await this.$axios.patch(`/api/1.0/posts/${id}/`, {
        text: this.originalPost.text,
      });

      if (resp.status === 200) {
        console.log('Original post was updated');
      }
    },
    async updateComment(comment) {
      const { id } = comment;

      const resp = await this.$axios.patch(`/api/1.0/comments/${id}/`, {
        text: comment.text,
        ref_text: comment.ref_text
      });

      if (resp.status === 200) {
        console.log(`Comment ${id} was updated`);
      }
    },
    async getRenderedPost(postId) {
      const resp = await this.$axios.get(`/api/1.0/rendered_posts/${postId}`);
      const renderedPosts = resp.data;
      renderedPosts.images = renderedPosts.images || [];
      return renderedPosts;
    },
    formatImgLinks(images) {
      const links = images.map((i) => `/media/${i.image}`);
      return links;
    },
    async updateStatus(status) {
      const { id } = this.post;

      const resp = await this.$axios.patch(`/api/1.0/rendered_posts/${id}/`, {
        status
      });

      this.post.status = resp.data.status;
    },
    selectComment(commentId) {
      if (this.selectedComments[commentId]) {
        this.selectedComments = [];
        this.selectedComments[commentId] = true;
      }
    },
    formatCommentText(comment) {
      if (comment.ref_text.length > 0) {
        return `*${comment.ref_text}*\n*${comment.text}*`;
      }

      return comment.text;
    },
    async rerendAsOriginal() {
      const config = {
        rendered_post_id: this.post.id,
        replace: 1,
        as_original: 1,
      };

      const resp = await this.$axios.post('/api/1.0/render_post', config);
      this.post = await this.getRenderedPost(resp.data.id);
    },
    async rerendPost() {
      if (this.originalPostTextChanged) {
        await this.updateOriginalPost();
        this.originalPostTextChanged = false;
      }
      // eslint-disable-next-line no-restricted-syntax
      for (let commentId in this.changedComments) {
        if (this.changedComments[commentId] === true) {
          this.changedComments[commentId] = false;
          commentId = Number(commentId);
          const comment = this.originalPost.comments.find((c) => c.id === commentId);
          // eslint-disable-next-line no-await-in-loop
          await this.updateComment(comment);
        }
      }

      const config = {
        rendered_post_id: this.post.id,
        replace: 1,
      };

      if (this.selectedOriginalText) {
        config.img_text_with_original_text = 1;
      } else {
        config.img_text_with_original_text = 0;
      }

      if (this.selectedOriginalImage) {
        config.img_with_post_img = 1;
      } else {
        config.img_with_post_img = 0;
      }

      let commentIsSelected = false;
      // eslint-disable-next-line no-restricted-syntax
      for (const commentId in this.selectedComments) {
        if (this.selectedComments[commentId] === true) {
          config.img_comment_id = Number(commentId);
          commentIsSelected = true;
          break;
        }
      }

      if (commentIsSelected === false) {
        config.img_with_comment = 0;
      }

      const resp = await this.$axios.post('/api/1.0/render_post', config);
      this.post = await this.getRenderedPost(resp.data.id);
    },
  }
};
</script>
