<script setup lang="ts">
import "@/static/css/style.scss";
import _ from "lodash";
import "@ahzoo/ouo/style.css";
import "font-awesome/css/font-awesome.css";
import {scrollSetToc, setAttribute} from "@ahzoo/utils";
import {useArticleStore} from "@/store/articleStore";
import SidebarMobile from "@/components/sidebar/mobile.vue";

const {$viewport} = useNuxtApp();
const articleStore = useArticleStore();
const show = ref(false);

const latestIndex = ref(0);

// 滚动时定位Toc位置
function scrollHandlerSetToc(scrollTop: number) {
  const scrollToc = scrollSetToc(scrollTop, latestIndex.value, articleStore.tocList);
  if (!scrollToc) {
    return;
  }
  latestIndex.value = scrollToc.latestIndex;
  // 防止重复设置当前选中目录
  if (articleStore.onClick) {
    return;
  }
  articleStore.setSelectTitle(scrollToc.id);
}

function scrollHandler() {
  try {
     window!.onscroll = (_.throttle(() => {
      // 滚动条向下
      const scrollPosition = window.scrollY || document.documentElement.scrollTop;
      if (scrollPosition > 30) {
        scrollHandlerSetToc(scrollPosition);
        setAttribute("scroll", "scroll");
      } else {
        // 滚动到顶部
        setAttribute("scroll", "primary");
      }
    }, 200));
  } catch (e) {
    console.log(e);
  }
}

onMounted(() => {
  if (process.client) {
    show.value = true;
    if ($viewport.isLessThan("lg")) {
      setAttribute("scroll", "scroll");
    } else {
      scrollHandler();
    }
  }
});
</script>
<template>
  <NuxtLoadingIndicator/>
  <div v-show="show" id="basic" class="font-size-medium w-full h-full flex flex-col relative">
    <div id="ahzoo" class="relative w-full overflow-y-scroll">
      <NuxtPage/>
      <SidebarMobile/>
      <Footer/>
    </div>
    <Menu/>
  </div>
</template>
