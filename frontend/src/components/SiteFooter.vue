<script setup>
defineProps({
  whatsappNumber: {
    type: String,
    default: '60102431634',
  },
})

const displayNumber = (number) => (number === '60102431634' ? '+60 10-243 1634' : `+${number}`)
</script>

<template>
  <footer class="site-footer">
    <div>
      <a class="brand footer-brand" href="/" aria-label="Gameslot home">
        <span class="brand-mark">GS</span>
        <span>
          Gameslot
          <small>Curated game accounts</small>
        </span>
      </a>
      <p>Clear listings, direct WhatsApp ordering, and friendly account handover.</p>
    </div>

    <div class="footer-contact">
      <span>WhatsApp support</span>
      <a :href="`https://wa.me/${whatsappNumber}`" target="_blank" rel="noopener noreferrer">
        {{ displayNumber(whatsappNumber) }}
      </a>
    </div>
  </footer>
</template>
