import { defineStore } from "pinia";
import { reactive, ref } from "vue";

export type User = {
    _id?: string
    first_name: string
    last_name: string
    email: string
    password:string
    friends: String[]
    profile_pic_url: string
    spotify_id: string
    spotify_token: string
    username: string
    admin: boolean
    _id?: string,
    spotify_refresh_token: string
}

export const useUser = defineStore('user', {
  state: () => ({
    user: null as User | null,
  }),
  actions: {
    setUser(newUser: User | null) {
        this.user = newUser;
    }
  }
})
