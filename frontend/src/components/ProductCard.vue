<script setup>
const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
  linkCategory: {
    type: Boolean,
    default: false,
  },
  whatsappNumber: {
    type: String,
    default: '60102431634',
  },
})

const message = encodeURIComponent(
  `Hi Gameslot, I would like to buy "${props.product.title}" (${props.product.price}). Is it still available?`,
)
const whatsappUrl = `https://wa.me/${props.whatsappNumber}?text=${message}`
</script>

<template>
  <article class="listing-card">
    <div
      class="listing-art"
      :style="product.coverImage ? { backgroundImage: `url(${product.coverImage})` } : undefined"
      aria-hidden="true"
    >
      <span class="availability-dot">{{ product.status }}</span>
      <div v-if="product.isHot || product.isNew" class="product-badges">
        <span v-if="product.isHot">Hot</span>
        <span v-if="product.isNew">New</span>
      </div>
    </div>

    <a
      v-if="linkCategory"
      class="listing-category"
      :href="`/categories/${product.categorySlug}/`"
    >
      {{ product.category }}
    </a>
    <small v-else class="listing-category">{{ product.category }}</small>

    <h3>{{ product.title }}</h3>
    <p>{{ product.summary }}</p>

    <div v-if="product.server || product.accountLevel" class="product-facts">
      <span v-if="product.server">
        <small>Server</small>
        {{ product.server }}
      </span>
      <span v-if="product.accountLevel">
        <small>Level</small>
        {{ product.accountLevel }}
      </span>
    </div>

    <div class="listing-price">
      <span>{{ product.stockNote || 'Ready stock' }}</span>
      <strong>{{ product.price }}</strong>
    </div>

    <a class="buy-button" :href="whatsappUrl" target="_blank" rel="noopener noreferrer">
      <span class="whatsapp-mark" aria-hidden="true">W</span>
      Buy on WhatsApp
    </a>
    <small v-if="product.deliveryNote" class="delivery-note">{{ product.deliveryNote }}</small>
  </article>
</template>
