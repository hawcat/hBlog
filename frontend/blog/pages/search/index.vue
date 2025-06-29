<script setup lang="ts">
import type {PreviewArticle} from "@/types/articleInterface";
import {searchAllApi, searchArticleContentApi, searchArticleTitleApi} from "@/api/search";
import {useSearchStore} from "@/store/searchStore";
import ArticleItem from "@/components/list/HorizontalArticleItem.vue";

const searchStore = useSearchStore();

const searchList = ref<PreviewArticle[]>([] as PreviewArticle[]);
const showLoading = ref(false);

/**
 * 数据获取
 */
await searchArticleList(searchStore.keyword, 1);

async function searchArticleList(keyword: string, pagination: number) {
  if (!searchStore.keyword) {
    navigateTo("/");
    return;
  }
  const params = {
    "keyword": keyword,
    "pagination": pagination
  };
  const type = searchStore.type;
  showLoading.value = true;
  if (type === "content") {
    const newSearchList = await searchArticleContentApi(params);
    searchList.value = unref(newSearchList);
  } else if (type === "title") {
    const newSearchList = await searchArticleTitleApi(params);
    searchList.value = unref(newSearchList);
  } else {
    const newSearchList = await searchAllApi(params);
    searchList.value = unref(newSearchList);
  }
  showLoading.value = false;
}

/**
 * 监听搜索关键词变化
 */
searchStore.$subscribe((mutation, state) => {
  searchArticleList(state.marking, 1);
});

useSeoMeta({
  title: "搜索",
  description: "搜索页"
})
</script>

<template>
  <div v-show="showLoading" class="w-full h-full">
    <Loading/>
  </div>
  <div class="page-content w-full">
    <div class="search-header box flex rounded-xl">
      <span class="title tag-item">{{ searchStore.keyword }}</span>
    </div>
    <div class="mt-7">
      <div v-if="!searchList||searchList.length<=0" class="text-center">
        什么也没有搜索到（⊙ｏ⊙）
      </div>
      <div v-for="article in searchList">
        <ArticleItem :article="article"/>
      </div>
    </div>
  </div>
</template>
