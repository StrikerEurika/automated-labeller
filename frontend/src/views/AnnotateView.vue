<template>
  <div class="p-6 max-w-6xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">AutoAnnotate</h1>

    <div class="mb-4">
      <label class="block mb-2">Prompt (e.g., "solar panel, roof")</label>
      <input
        v-model="prompt"
        type="text"
        class="w-full p-2 border rounded"
        placeholder="Enter comma-separated object names"
      />
    </div>

    <div class="mb-4">
      <input type="file" @change="onFileSelect" accept="image/*" />
    </div>

    <button
      @click="runAutoAnnotate"
      :disabled="!selectedFile"
      class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
    >
      Auto-Annotate
    </button>

    <div v-if="imagePreview" class="mt-6">
      <Canvas :image-src="imagePreview" :masks-b64="masksB64" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import api from "@/api/client";
import Canvas from "@/components/Canvas.vue";

const prompt = ref("car, tree");
const selectedFile = ref<File | null>(null);
const imagePreview = ref<string | null>(null);
const masksB64 = ref<string[]>([]);

const onFileSelect = (e: Event) => {
  const input = e.target as HTMLInputElement;
  if (input.files?.[0]) {
    selectedFile.value = input.files[0];
    imagePreview.value = URL.createObjectURL(input.files[0]);
    masksB64.value = [];
  }
};

const runAutoAnnotate = async () => {
  if (!selectedFile.value) return;

  const formData = new FormData();
  formData.append("image", selectedFile.value);
  formData.append("prompts", prompt.value);

  try {
    const res = await api.post("/annotate", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    masksB64.value = res.data.masks_b64;
  } catch (err) {
    console.error("Annotation failed", err);
    alert(
      `Failed to generate annotations: ${
        err instanceof Error ? err.message : "Unknown error"
      }`
    );
  }
};
</script>
