<script setup lang="ts">
import "@/static/css/style.scss";
import _ from "lodash";
import "@ahzoo/ouo/style.css";
import "font-awesome/css/font-awesome.css";
import {setAttribute} from "@ahzoo/utils";
import SidebarMobile from "@/components/sidebar/mobile.vue";

const {$viewport} = useNuxtApp();
const show = ref(false);

function scrollHandler() {
  try {
     window!.onscroll = (_.throttle(() => {
      // 滚动条向下
      if (window.scrollY > 30 || document.documentElement.scrollTop > 30) {
        setAttribute("scroll", "scroll");
      } else {
        // 滚动到顶部
        setAttribute("scroll", "top");
      }
    }, 200));
  } catch (e) {
    console.log(e);
  }
}

onMounted(() => {
  const primary = document.getElementById("ahzoo");
  primary!.scrollTop = 0;
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
      <div class="w-full">
        <Header/>
      </div>
      <div id="main" class="page flex" :class="$viewport.isLessThan('lg') ? 'mobile' : 'pc'">
        <NuxtPage/>
        <Sidebar class="w-1/3 mt-5"
                 v-if="!$viewport.isLessThan('lg')"/>
      </div>
      <SidebarMobile/>
      <Footer/>
    </div>
    <Menu/>
  </div>
</template>

<style lang="scss">
#basic {
  color: rgb(var(--z-fontcolor));
  transition: all .3s;
  background-image: url("/basic-bg.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
