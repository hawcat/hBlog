import {useDefaultRequest} from "@/api/request";
import type {CategoryMap} from "@/types/categoryInterface";

const BASE_URL = "/v1/categories";

export function listCategoryApi(): Promise<CategoryMap[]>  {
    return useDefaultRequest.get<CategoryMap[]>(BASE_URL);
}
