<template>
  <div class="relative border" ref="containerRef">
    <img
      v-if="imageSrc"
      :src="imageSrc"
      class="max-w-full h-auto"
      @load="onImageLoad"
      crossorigin="anonymous"
    />
    <canvas
      ref="maskCanvasRef"
      class="absolute top-0 left-0 pointer-events-none"
    ></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'

const props = defineProps<{
  imageSrc?: string
  masksB64?: string[]
}>()

const containerRef = ref<HTMLDivElement | null>(null)
const maskCanvasRef = ref<HTMLCanvasElement | null>(null)

const onImageLoad = () => {
  drawMasks()
}

const drawMasks = () => {
  const canvas = maskCanvasRef.value
  const container = containerRef.value
  if (!canvas || !container || !props.masksB64) return

  const img = container.querySelector('img')
  if (!img) return

  canvas.width = img.naturalWidth
  canvas.height = img.naturalHeight

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  props.masksB64.forEach(maskB64 => {
    const imgEl = new Image()
    imgEl.onload = () => {
      ctx.globalAlpha = 0.5
      ctx.drawImage(imgEl, 0, 0, canvas.width, canvas.height)
      ctx.globalAlpha = 1.0
    }
    imgEl.src = `data:image/png;base64,${maskB64}`
  })
}

watch(() => props.masksB64, drawMasks, { deep: true })
</script>