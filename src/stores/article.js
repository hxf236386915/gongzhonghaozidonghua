import { defineStore } from 'pinia'

export const useArticleStore = defineStore('article', {
  state: () => ({
    articles: [],
    currentArticle: null
  }),
  actions: {
    setArticles(articles) {
      this.articles = articles
    },
    setCurrentArticle(article) {
      this.currentArticle = article
    },
    clearArticles() {
      this.articles = []
      this.currentArticle = null
    }
  },
  persist: true
})