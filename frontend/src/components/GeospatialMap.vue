<template>
  <div ref="mapRef" class="geospatial-map"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts/core'
import { 
  GeoComponent, 
  TooltipComponent, 
  VisualMapComponent 
} from 'echarts/components'
import { MapChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([GeoComponent, TooltipComponent, VisualMapComponent, MapChart, CanvasRenderer])

const props = defineProps<{
  annotations: any[]
}>()

const mapRef = ref<HTMLDivElement>()

onMounted(() => {
  const chart = echarts.init(mapRef.value!)
  
  const option = {
    geo: {
      map: 'world',
      roam: true,
      itemStyle: {
        areaColor: '#f0f0f0',
        borderColor: '#ccc'
      }
    },
    series: [
      {
        type: 'scatter',
        coordinateSystem: 'geo',
         props.annotations.map(ann => ({
          name: ann.label,
          value: [ann.longitude, ann.latitude, ann.confidence]
        })),
        symbolSize: 10,
        itemStyle: {
          color: '#ff4757'
        }
      }
    ],
    tooltip: {
      trigger: 'item'
    }
  }
  
  chart.setOption(option)
  
  const resizeHandler = () => chart.resize()
  window.addEventListener('resize', resizeHandler)
  
  onUnmounted(() => {
    chart.dispose()
    window.removeEventListener('resize', resizeHandler)
  })
})
</script>

<style scoped>
.geospatial-map {
  @apply w-full h-96;
}
</style>