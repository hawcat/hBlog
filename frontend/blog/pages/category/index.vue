<script setup lang="ts">
import type {CategoryMap} from "@/types/categoryInterface";
import type {PreviewColumn} from "@/types/columnInterface";
import {listCategoryApi} from "@/api/category";
import {listAllColumnApi, listColumnByCategoryIdApi} from "@/api/column";
import {OuOTag} from "@ahzoo/ouo";
import ColumnItem from "@/components/list/ColumnItem.vue";

const categoryList = ref<CategoryMap[]>([]);
const columnList = ref<PreviewColumn[]>([]);

getCategoryList();
getAllColumnList();

async function getCategoryList() {
  const newCategoryList = await listCategoryApi();
  categoryList.value = unref(newCategoryList);
}

async function getAllColumnList() {
  const newColumnList = await listAllColumnApi();
  columnList.value = unref(newColumnList);
}
async function getColumnListByCategoryId(categoryId: string, pagination: number) {
  const newColumnList = await listColumnByCategoryIdApi(categoryId, pagination);
  columnList.value = unref(newColumnList);
}

useSeoMeta({
  title: "分类",
  description: "分类页"
})
</script>

<template>
  <div class="page-content w-full">
    <div v-if="categoryList.length>0" class="box-header">
      <OuOTag class="mr-2" :size="'small'" @click="getAllColumnList" :checked="'true'">
        全部专栏
      </OuOTag>
      <OuOTag class="mr-2" :size="'small'" v-for="category in categoryList"
              @click="getColumnListByCategoryId(category.id, 1)">
        {{ category.name }}
      </OuOTag>
    </div>
    <div class="category-column grid column-grid gap-7 gap-y-5 pc:gap-5 mt-6">
      <ColumnItem v-for="column in columnList" :column="column"/>
    </div>
  </div>
</template>
