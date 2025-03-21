import { defineStore } from "pinia";
import { reactive, ref } from "vue";

export type User = {
    first_name: string
    last_name: string
    email: string
    password:string
    friends: String[]
    profile_pic_url: string
    spotify_id: string
    spotify_token: string
    username: string
}

export const useUser = defineStore('user', {
  state: () => ({
    user: null as User | null,  // Define the state object with `user` initialized to `null`
  }),
  actions: {
    setUser(newUser: User | null) {
        this.user = newUser;
    }
  }
})
