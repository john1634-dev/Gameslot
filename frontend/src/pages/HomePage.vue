<script setup>
import { computed, onMounted, ref } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import SiteFooter from '../components/SiteFooter.vue'
import SiteHeader from '../components/SiteHeader.vue'

const site = ref({
  title: 'New Season Stock',
  headline: 'No Reroll, No Life',
  description: 'Starter accounts, VIP collections, and reroll picks refreshed for anime game players.',
  coverImage: '',
  announcement: 'Fresh accounts are reviewed and updated regularly.',
  supportHours: 'Daily support',
  whatsappNumber: '60102431634',
})
const categories = ref([])
const latestListings = ref([])
const loading = ref(true)
const searchQuery = ref('')

const filteredListings = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) return latestListings.value
  return latestListings.value.filter((listing) =>
    [listing.title, listing.category, listing.server, listing.accountLevel]
      .filter(Boolean)
      .some((value) => value.toLowerCase().includes(query)),
  )
})

const totalStock = computed(() => categories.value.reduce((sum, category) => sum + Number(category.stock || 0), 0))

onMounted(async () => {
  try {
    const response = await fetch('/api/home/')
    const data = await response.json()
    site.value = data.site
    categories.value = data.categories
    latestListings.value = data.latestListings
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="site-shell">
    <SiteHeader />
    <div class="announcement-bar">{{ site.announcement }}</div>

    <section class="hero-section">
      <aside class="hero-panel" aria-label="New season stock">
        <div
          class="banner-card"
          :class="{ 'has-cover': site.coverImage }"
          :style="{ backgroundImage: `linear-gradient(90deg, rgba(8, 9, 16, 0.86) 0%, rgba(8, 9, 16, 0.2) 65%, rgba(8, 9, 16, 0.65) 100%), url(${site.coverImage || '/static/frontend/anime-store-hero.png'})` }"
        >
          <span>{{ site.title }}</span>
          <strong>{{ site.headline }}</strong>
          <p>{{ site.description }}</p>
          <div class="hero-meta">
            <span>Verified listings</span>
            <span>Direct WhatsApp order</span>
            <span>Manual handover</span>
          </div>
        </div>
      </aside>
    </section>

    <section class="stats-strip" aria-label="Store highlights">
      <div>
        <strong>{{ categories.length }}</strong>
        <span>Game categories</span>
      </div>
      <div>
        <strong>{{ totalStock }}</strong>
        <span>Active accounts</span>
      </div>
      <div>
        <strong>{{ site.supportHours }}</strong>
        <span>Support window</span>
      </div>
    </section>

    <section class="preview-section" aria-label="Account categories">
      <div class="section-heading">
        <div class="section-label-row">
          <p class="eyebrow">Account Categories</p>
          <span>{{ categories.length }} games</span>
        </div>
        <h1>Choose your game first.</h1>
        <p>Browse each game through its dedicated storefront and compare available accounts.</p>
      </div>

      <p v-if="loading" class="empty-state">Loading store categories...</p>
      <div v-else class="category-strip">
        <a
          v-for="(category, index) in categories"
          :key="category.slug"
          :href="`/categories/${category.slug}/`"
          class="category-tile"
          :class="{ 'category-tile-featured': index === 0 }"
          :style="{
            '--accent': category.accentColor || '#ff8ebb',
            ...(category.coverImage
              ? { backgroundImage: `linear-gradient(180deg, rgba(13, 15, 25, 0.2), rgba(13, 15, 25, 0.92)), url(${category.coverImage})` }
              : {}),
          }"
        >
          <div class="category-topline">
            <span class="category-number">{{ String(index + 1).padStart(2, '0') }}</span>
            <small>{{ category.badge || 'Game Accounts' }}</small>
          </div>
          <div class="category-content">
            <p>{{ category.subtitle || 'Curated Account Collection' }}</p>
            <strong>{{ category.name }}</strong>
          </div>
          <div class="category-footer">
            <span><b>{{ category.stock }}</b> listings</span>
            <span class="category-action">Browse <b aria-hidden="true">&rarr;</b></span>
          </div>
        </a>
      </div>
    </section>

    <section class="latest-section" aria-label="Latest listings">
      <div class="section-heading">
        <div class="section-label-row">
          <p class="eyebrow">Latest Listings</p>
          <span>{{ latestListings.length }} available</span>
        </div>
        <h2>Fresh account offers</h2>
      </div>

      <div class="listing-toolbar">
        <label class="search-field">
          <span>Search</span>
          <input v-model="searchQuery" type="search" placeholder="Search game, account, server..." />
        </label>
      </div>

      <p v-if="!loading && latestListings.length === 0" class="empty-state">
        No listings are available yet.
      </p>
      <p v-else-if="!loading && filteredListings.length === 0" class="empty-state">
        No listings match your search.
      </p>
      <div v-else class="listing-grid">
        <ProductCard
          v-for="account in filteredListings"
          :key="account.slug"
          :product="account"
          link-category
          :whatsapp-number="site.whatsappNumber"
        />
      </div>
    </section>

    <SiteFooter :whatsapp-number="site.whatsappNumber" />
  </main>
</template>
