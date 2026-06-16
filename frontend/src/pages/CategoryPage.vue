<script setup>
import { computed, onMounted, ref } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import SiteFooter from '../components/SiteFooter.vue'
import SiteHeader from '../components/SiteHeader.vue'

const category = ref(null)
const products = ref([])
const loading = ref(true)
const searchQuery = ref('')
const statusFilter = ref('All')
const whatsappNumber = ref('60102431634')

const slug = computed(() => {
  const parts = window.location.pathname.split('/').filter(Boolean)
  return parts[1] || ''
})

const statuses = computed(() => ['All', ...new Set(products.value.map((product) => product.status))])
const filteredProducts = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  return products.value.filter((product) => {
    const matchesStatus = statusFilter.value === 'All' || product.status === statusFilter.value
    const matchesQuery =
      !query ||
      [product.title, product.summary, product.server, product.accountLevel]
        .filter(Boolean)
        .some((value) => value.toLowerCase().includes(query))
    return matchesStatus && matchesQuery
  })
})

onMounted(async () => {
  try {
    const response = await fetch(`/api/categories/${slug.value}/`)
    const data = await response.json()
    category.value = data.category
    products.value = data.products
    whatsappNumber.value = data.whatsappNumber
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="site-shell">
    <SiteHeader />

    <section v-if="category" class="category-hero">
      <div>
        <p class="eyebrow">{{ category.badge }}</p>
        <h1>{{ category.name }}</h1>
        <p>{{ category.description }}</p>
        <div class="category-meta">
          <span>{{ products.length }} active listings</span>
          <span>Order via WhatsApp</span>
        </div>
      </div>
      <div
        class="category-cover"
        :style="{
          '--accent': category.accentColor || '#ff8ebb',
          ...(category.coverImage ? { backgroundImage: `url(${category.coverImage})` } : {}),
        }"
        aria-hidden="true"
      ></div>
    </section>

    <section class="latest-section" aria-label="Category listings">
      <div class="section-heading">
        <div class="section-label-row">
          <p class="eyebrow">Category Listings</p>
          <a href="/">Back to all games</a>
        </div>
        <h2>{{ category ? category.name : 'Loading category' }}</h2>
      </div>

      <div class="listing-toolbar category-toolbar">
        <label class="search-field">
          <span>Search listings</span>
          <input v-model="searchQuery" type="search" placeholder="Search title, server, level..." />
        </label>
        <label class="filter-field">
          <span>Status</span>
          <select v-model="statusFilter">
            <option v-for="status in statuses" :key="status" :value="status">{{ status }}</option>
          </select>
        </label>
      </div>

      <p v-if="loading" class="empty-state">Loading listings...</p>
      <p v-else-if="products.length === 0" class="empty-state">No active listings in this category.</p>
      <p v-else-if="filteredProducts.length === 0" class="empty-state">
        No listings match the selected filters.
      </p>
      <div v-else class="listing-grid">
        <ProductCard
          v-for="product in filteredProducts"
          :key="product.slug"
          :product="product"
          :whatsapp-number="whatsappNumber"
        />
      </div>
    </section>

    <SiteFooter :whatsapp-number="whatsappNumber" />
  </main>
</template>
