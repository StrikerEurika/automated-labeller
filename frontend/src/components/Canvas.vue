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
      class="absolute top-0 left-0 cursor-pointer"
      @click="onCanvasClick"
      @mousemove="onCanvasHover"
      @mouseleave="hoveredDetectionId = null"
    ></canvas>

    <!-- Hover Tooltip -->
    <div
      v-if="hoveredDetectionId !== null && hoveredDetection"
      :style="{ left: tooltipX + 'px', top: tooltipY + 'px' }"
      class="absolute bg-gray-900 text-white text-xs rounded py-2 px-3 pointer-events-none z-10 shadow-lg"
    >
      <p class="font-semibold">{{ hoveredDetection.label }}</p>
      <p class="text-gray-300">
        {{ Math.round(hoveredDetection.confidence * 100) }}% confidence
      </p>
      <p class="text-gray-400 text-[10px] mt-1">Click to select</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";

interface Detection {
  id: number;
  label: string;
  confidence: number;
  bbox: number[];
  mask_b64: string;
  visible?: boolean;
}

const props = defineProps<{
  imageSrc?: string;
  detections?: Detection[];
  zoom?: number;
  selectedDetectionId?: number | null;
}>();

const emit = defineEmits<{
  (e: "select-detection", id: number): void;
}>();

const containerRef = ref<HTMLDivElement | null>(null);
const maskCanvasRef = ref<HTMLCanvasElement | null>(null);
const maskColors = ref<string[]>([]);
const maskImageElements = ref<Map<number, HTMLImageElement>>(new Map());
const hoveredDetectionId = ref<number | null>(null);
const tooltipX = ref(0);
const tooltipY = ref(0);

const hoveredDetection = computed(() => {
  if (hoveredDetectionId.value === null) return null;
  return props.detections?.find((d) => d.id === hoveredDetectionId.value);
});

// Generate distinct colors for each mask
const generateColors = (count: number) => {
  const colors = [
    "rgba(255, 99, 71, 0.6)", // Tomato
    "rgba(54, 162, 235, 0.6)", // Blue
    "rgba(75, 192, 192, 0.6)", // Teal
    "rgba(255, 206, 86, 0.6)", // Yellow
    "rgba(153, 102, 255, 0.6)", // Purple
    "rgba(255, 159, 64, 0.6)", // Orange
    "rgba(46, 204, 113, 0.6)", // Green
    "rgba(231, 76, 60, 0.6)", // Red
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
  if (
    !canvas ||
    !container ||
    !props.detections ||
    props.detections.length === 0
  )
    return;

  const img = container.querySelector("img");
  if (!img) return;

  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;

  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  generateColors(props.detections.length);
  maskImageElements.value.clear();

  let loadedCount = 0;
  const totalMasks = props.detections.filter((d) => d.visible !== false).length;

  props.detections.forEach((detection) => {
    if (detection.visible === false) return;

    const imgEl = new Image();
    imgEl.onload = () => {
      maskImageElements.value.set(detection.id, imgEl);
      loadedCount++;
      if (loadedCount === totalMasks) {
        redrawMasks();
      }
    };
    imgEl.src = `data:image/png;base64,${detection.mask_b64}`;
  });
};

const redrawMasks = () => {
  const canvas = maskCanvasRef.value;
  const ctx = canvas?.getContext("2d");
  if (!ctx || !canvas || !props.detections) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw all masks
  props.detections.forEach((detection) => {
    if (detection.visible === false) return;

    const imgEl = maskImageElements.value.get(detection.id);
    if (!imgEl) return;

    const isSelected = props.selectedDetectionId === detection.id;
    const isHovered = hoveredDetectionId.value === detection.id;

    ctx.save();

    // Adjust opacity based on state
    if (isSelected || isHovered) {
      ctx.globalAlpha = 0.8;
    } else if (
      props.selectedDetectionId !== null ||
      hoveredDetectionId.value !== null
    ) {
      ctx.globalAlpha = 0.3;
    } else {
      ctx.globalAlpha = 0.6;
    }

    // Draw mask
    ctx.drawImage(imgEl, 0, 0, canvas.width, canvas.height);

    // Apply color overlay
    ctx.globalCompositeOperation = "source-in";
    ctx.fillStyle = maskColors.value[detection.id % maskColors.value.length];
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.restore();
    ctx.globalCompositeOperation = "source-over";

    // Draw border for selected or hovered
    if (isSelected || isHovered) {
      ctx.strokeStyle = isSelected
        ? "rgba(79, 70, 229, 1)"
        : "rgba(255, 255, 255, 0.9)";
      ctx.lineWidth = isSelected ? 4 : 3;
      ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
      ctx.shadowBlur = 10;

      // Draw bounding box
      const [x1, y1, x2, y2] = detection.bbox;
      ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

      ctx.shadowBlur = 0;
    }
  });
};

const onCanvasClick = (e: MouseEvent) => {
  const detection = getDetectionAtPoint(e);
  if (detection) {
    emit("select-detection", detection.id);
  }
};

const onCanvasHover = (e: MouseEvent) => {
  const detection = getDetectionAtPoint(e);
  hoveredDetectionId.value = detection ? detection.id : null;

  if (detection) {
    tooltipX.value = e.offsetX + 15;
    tooltipY.value = e.offsetY + 15;
  }
};

const getDetectionAtPoint = (e: MouseEvent): Detection | null => {
  const canvas = maskCanvasRef.value;
  const container = containerRef.value;
  if (!canvas || !container || !props.detections) return null;

  const img = container.querySelector("img");
  if (!img) return null;

  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  const x = ((e.clientX - rect.left) * scaleX) / (props.zoom || 1);
  const y = ((e.clientY - rect.top) * scaleY) / (props.zoom || 1);

  // Check detections in reverse order (top to bottom)
  for (let i = props.detections.length - 1; i >= 0; i--) {
    const detection = props.detections[i];
    if (detection.visible === false) continue;

    const [x1, y1, x2, y2] = detection.bbox;
    if (x >= x1 && x <= x2 && y >= y1 && y <= y2) {
      return detection;
    }
  }

  return null;
};

watch(() => props.detections, drawMasks, { deep: true });
watch(() => props.selectedDetectionId, redrawMasks);
watch(() => hoveredDetectionId.value, redrawMasks);
</script>
