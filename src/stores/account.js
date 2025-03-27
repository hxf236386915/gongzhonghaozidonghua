import { defineStore } from 'pinia'

export const useAccountStore = defineStore('account', {
  state: () => ({
    token: null,
    userInfo: null
  }),
  actions: {
    setToken(token) {
      this.token = token
    },
    setUserInfo(userInfo) {
      this.userInfo = userInfo
    },
    clearAccount() {
      this.token = null
      this.userInfo = null
    }
  },
  persist: true
})