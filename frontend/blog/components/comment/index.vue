<script setup lang="ts">
import type {Comment, CommentItem} from "@/types/commentInterface";
import {listFriendApi, saveCommentApi} from "@/api/comment";
import {useGlobalStore} from "@/store/globalStore";
import {SuSComment, SuSList} from "@ahzoo/sus";
import {OuOMessage} from "@ahzoo/ouo";
import emoji from "@/static/json/emoji.json";

const {path} = useRoute();
const articlePath = <string>path.split("/").pop();
const globalStore = useGlobalStore();
const commentList = ref<CommentItem[]>([] as CommentItem[]);
const replyComment = ref<CommentItem>({} as CommentItem);
const showLoading = ref(false);

/**
 * 数据获取
 */
await getCommentList(1);

/**
 * 正常评论弹窗
 */
function toShowComment() {
  replyComment.value = {} as CommentItem;
  globalStore.setShowComment(true);
}

/**
 * 回复评论弹窗
 * @param comment
 */
function toReplyComment(comment: CommentItem) {
  replyComment.value = unref(comment);
  globalStore.setShowComment(true);
}

function toCancelComment() {
  globalStore.setShowComment(false);
}

/**
 * 保存评论
 * @param comment
 */
async function toSaveComment(comment: Comment) {
  const beforeContent = localStorage.getItem("content");
  comment.articleId = articlePath;
  const contentLength = comment.contentMD.length;
  if (!comment) {
    return;
  }
  if (beforeContent === comment.contentMD) {
    OuOMessage.warning("请勿发送重复内容");
    return;
  }
  if (!comment.userName) {
    OuOMessage.warning("请先填写昵称");
    return;
  }
  if (contentLength < 3) {
    OuOMessage.warning("字数过少");
    return;
  }
  if (contentLength > 800) {
    OuOMessage.warning("字数超出限制");
    return;
  }
  showLoading.value = true;
  comment.website = window.location.href;
  const res = await saveCommentApi(comment);
  showLoading.value = false;
  if (!!res) {
    localStorage.setItem("content", comment.contentMD);
    OuOMessage.success("评论成功");
    globalStore.setShowComment(false);
    await getCommentList(1);
  }
}

async function getCommentList(pagination: number) {
  commentList.value = await listFriendApi(articlePath, pagination);
}
</script>

<template>
  <Teleport to="body">
    <div class="comment-mask flex flex-col items-center justify-center absolute top-0 left-0 w-full h-full"
         v-show="globalStore.showComment">
      <div class="comment-sus flex flex-col">
        <div v-show="showLoading" class="w-full h-full">
          <Loading/>
        </div>
        <div class="stress my-3" v-show="replyComment?.userName">回复@{{ replyComment?.userName }}：</div>
        <SuSComment class="w-full h-auto" :cache="true" :reply="replyComment" :emoji="emoji"
                    @on-cancel="toCancelComment" @on-save="toSaveComment"/>
      </div>
    </div>
  </Teleport>
  <div id="comment" class="relative h-full">
    <div class="box-header flex justify-end">
      <div class="right cursor-pointer">
        <span class="stress mx-2"
              @click="toShowComment">
          发表评论
        </span>
        <i class="fa fa-send"/>
      </div>
    </div>
    <div class="comment-list">
      <SuSList v-for="commentItem in commentList" :comment="commentItem" @on-reply="toReplyComment"/>
    </div>
  </div>
</template>

<style scoped lang="scss">
.comment {

  &-mask {
    z-index: 11;
    background-color: rgba(var(--z-global-bg), .9);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-transition: all .25s ease;
    transition: all .25s ease;
  }

  &-sus {
    margin: 30px 15vw;
    max-width: 700px;
    min-width: 300px;
  }
}
</style>
