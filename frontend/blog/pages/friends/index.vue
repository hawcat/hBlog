<script setup lang="ts">
import type {FriendInterface} from "@/types/friendInterface";
import {listFriendApi} from "@/api/friend";
import {useGlobalStore} from "@/store/globalStore";

const globalStore = useGlobalStore();
const friendList = ref<FriendInterface[]>([]);

/**
 * 数据获取
 */
await getFriendList();

function showFriendForm() {
  globalStore.setShowFriendForm(true);
}

async function getFriendList() {
  friendList.value = await listFriendApi();
}

useSeoMeta({
  title: "友链",
  description: "友链页"
})
</script>

<template>
  <Friend/>
  <div class="friend-content relative w-full h-full mobile:px-5 px-8 pt-8 mt-5 rounded-lg">
    <div class="box-header flex justify-end">
      <div class="right cursor-pointer">
            <span class="stress mx-2"
                  @click="showFriendForm">
              交换友链
             </span>
        <i class="fa fa-send"/>
      </div>
    </div>
    <div class="friend-list grid gap-7 my-7">
      <FriendItem v-for="(item, index) in friendList" :key="index" :friend="item"/>
    </div>
  </div>
</template>
<style scoped lang="scss">
.friend {
  &-content {
    background: rgba(var(--z-common-bg), .6);
  }

  &-list {
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  }
}
</style>
