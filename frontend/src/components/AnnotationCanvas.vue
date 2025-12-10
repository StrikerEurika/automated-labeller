<template>
  <div class="annotation-container">
    <!-- Image display with overlay -->
    <div class="image-canvas" ref="canvasRef">
      <img 
        :src="imageUrl" 
        @load="onImageLoad"
        @click="onCanvasClick"
        class="annotation-image"
      />
      
      <!-- SVG overlay for annotations -->
      <svg class="annotation-overlay" ref="svgRef">
        <g v-for="(detection, index) in detections" :key="index">
          <rect
            :x="detection.bbox[0]"
            :y="detection.bbox[1]"
            :width="detection.bbox[2] - detection.bbox[0]"
            :height="detection.bbox[3] - detection.bbox[1]"
            class="detection-rect"
            @click="selectDetection(index)"
          />
          <polygon
            v-if="detection.mask"
            :points="formatMaskPoints(detection.mask)"
            class="mask-polygon"
          />
        </g>
      </svg>
    </div>
    
    <!-- Control panel -->
    <div class="control-panel">
      <v-text-field
        v-model="prompt"
        label="Annotation Prompt"
        placeholder="Describe objects to detect..."
        @keyup.enter="runAutoAnnotation"
      />
      <v-btn @click="runAutoAnnotation" :loading="isProcessing">
        Auto-annotate
      </v-btn>
      <v-btn @click="saveAnnotations" color="primary">
        Save Annotations
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { AnnotationRequest, AnnotationResult } from '@/types/annotation'

const canvasRef = ref<HTMLDivElement>()
const svgRef = ref<SVGSVGElement>()
const imageUrl = ref('')
const prompt = ref('')
const detections = ref<any[]>([])
const isProcessing = ref(false)

const runAutoAnnotation = async () => {
  isProcessing.value = true
  try {
    const response = await fetch('/api/annotate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_id: 'current_image',
        prompt: prompt.value
      } as AnnotationRequest)
    })
    
    const result = await response.json() as AnnotationResult
    detections.value = result.detections
  } catch (error) {
    console.error('Annotation failed:', error)
  } finally {
    isProcessing.value = false
  }
}

const formatMaskPoints = (mask: number[][]) => {
  return mask.map(([x, y]) => `${x},${y}`).join(' ')
}

const selectDetection = (index: number) => {
  // Handle detection selection for manual refinement
}
</script>

<style scoped>
.annotation-container {
  @apply flex flex-col h-screen bg-gray-50;
}

.image-canvas {
  @apply relative flex-1 overflow-auto;
}

.annotation-image {
  @apply max-w-full max-h-full object-contain;
}

.annotation-overlay {
  @apply absolute top-0 left-0 w-full h-full pointer-events-none;
}

.detection-rect {
  @apply fill-none stroke-blue-500 stroke-2;
}

.mask-polygon {
  @apply fill-blue-500 fill-opacity-20 stroke-blue-500 stroke-1;
}

.control-panel {
  @apply p-4 bg-white border-t;
}
</style>