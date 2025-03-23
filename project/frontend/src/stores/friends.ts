import { defineStore } from "pinia";
import { reactive, ref } from "vue";
import { type User } from "./user"

export const useFriends = defineStore('friends', {
  state: () => ({
    friends: [] as User[],
  }),
  actions: {
    setFriends(friends: User[]) {
        this.friends = friends;
    }
  }
})
