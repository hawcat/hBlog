import {useDefaultRequest} from "@/api/request";
import type {Result} from "@/types/resultInterface";
import type {Friend} from "@/types/friendInterface";

const BASE_URL = "/v1/friends";

export function saveFriendApi(friend: Friend, isUpdate: boolean): Promise<Result<any>> {
    const params = {
        u: isUpdate
    };
    return useDefaultRequest.post<Result<any>>(BASE_URL, friend, params);
}

export function listFriendApi(): Promise<Friend[]> {
    return useDefaultRequest.get<Friend[]>(BASE_URL);
}
