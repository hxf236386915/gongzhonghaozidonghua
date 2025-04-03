import type { Component } from 'vue'

export interface BaseMenuItem {
  id: number
  name: string
  path: string
  component: string
  type: 'menu' | 'directory'
  permission: string
  parent_id?: number
  level: number
  sort: number
  status: boolean
}

export interface MenuItem extends BaseMenuItem {
  icon?: string
  children?: MenuItem[]
}

export interface ProcessedMenuItem extends BaseMenuItem {
  icon: Component | null
  children?: ProcessedMenuItem[]
} 