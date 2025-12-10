<template>
  <div
    class="relative border border-gray-300 rounded overflow-hidden bg-gray-100"
    ref="containerRef"
  >
    <img
      v-if="imageSrc"
      :src="imageSrc"
      :style="{ transform: `scale(${zoom})`, transformOrigin: 'top left' }"
      class="max-w-full h-auto block"
      @load="onImageLoad"
      crossorigin="anonymous"
    />
    <canvas
      ref="maskCanvasRef"
      :style="{ transform: `scale(${zoom})`, transformOrigin: 'top left' }"
      class="absolute top-0 left-0 pointer-events-none"
    ></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
  imageSrc?: string;
  masksB64?: string[];
  zoom?: number;
}>();

const containerRef = ref<HTMLDivElement | null>(null);
const maskCanvasRef = ref<HTMLCanvasElement | null>(null);
const maskColors = ref<string[]>([]);

// Generate distinct colors for each mask
const generateColors = (count: number) => {
  const colors = [
    "rgba(255, 99, 71, 0.5)", // Tomato
    "rgba(54, 162, 235, 0.5)", // Blue
    "rgba(75, 192, 192, 0.5)", // Teal
    "rgba(255, 206, 86, 0.5)", // Yellow
    "rgba(153, 102, 255, 0.5)", // Purple
    "rgba(255, 159, 64, 0.5)", // Orange
    "rgba(46, 204, 113, 0.5)", // Green
    "rgba(231, 76, 60, 0.5)", // Red
  ];

  maskColors.value = [];
  for (let i = 0; i < count; i++) {
    maskColors.value.push(colors[i % colors.length]);
  }
};

const onImageLoad = () => {
  drawMasks();
};

const drawMasks = () => {
  const canvas = maskCanvasRef.value;
  const container = containerRef.value;
  if (!canvas || !container || !props.masksB64 || props.masksB64.length === 0)
    return;

  const img = container.querySelector("img");
  if (!img) return;

  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;

  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  generateColors(props.masksB64.length);

  let loadedCount = 0;
  const totalMasks = props.masksB64.length;

  props.masksB64.forEach((maskB64, index) => {
    const imgEl = new Image();
    imgEl.onload = () => {
      // Apply color tint to each mask
      ctx.save();
      ctx.globalAlpha = 0.6;

      // Draw mask
      ctx.drawImage(imgEl, 0, 0, canvas.width, canvas.height);

      // Apply color overlay using composite operation
      ctx.globalCompositeOperation = "source-in";
      ctx.fillStyle = maskColors.value[index];
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.restore();
      ctx.globalCompositeOperation = "source-over";

      // Draw border around mask
      loadedCount++;
      if (loadedCount === totalMasks) {
        drawMaskBorders();
      }
    };
    imgEl.src = `data:image/png;base64,${maskB64}`;
  });
};

const drawMaskBorders = () => {
  const canvas = maskCanvasRef.value;
  const ctx = canvas?.getContext("2d");
  if (!ctx || !canvas) return;

  // Add subtle borders to masks
  ctx.strokeStyle = "rgba(255, 255, 255, 0.8)";
  ctx.lineWidth = 2;
};

watch(() => props.masksB64, drawMasks, { deep: true });
watch(
  () => props.zoom,
  () => {
    // Zoom handled by CSS transform
  }
);
</script>
