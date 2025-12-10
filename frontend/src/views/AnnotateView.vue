<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="p-6 max-w-7xl mx-auto">
      <div class="bg-white rounded-lg shadow-xl p-6 mb-6">
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-3xl font-bold text-gray-800 flex items-center">
            <svg
              class="w-8 h-8 mr-3 text-indigo-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            SAM DA - Automated Labeller
          </h1>
          <div v-if="masksB64.length > 0" class="text-sm text-gray-600">
            <span class="font-semibold">{{ masksB64.length }}</span> object(s)
            detected
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Detection Prompts
          </label>
          <input
            v-model="prompt"
            type="text"
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
            placeholder="e.g., solar panel, roof, window"
          />
          <p class="mt-1 text-xs text-gray-500">
            Enter comma-separated object names to detect
          </p>
        </div>

        <!-- Drag and Drop Area -->
        <div
          @drop.prevent="onDrop"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          :class="[
            'mb-4 p-8 border-2 border-dashed rounded-lg transition-all cursor-pointer',
            isDragging
              ? 'border-indigo-500 bg-indigo-50'
              : 'border-gray-300 bg-gray-50 hover:bg-gray-100',
          ]"
          @click="triggerFileInput"
        >
          <input
            ref="fileInputRef"
            type="file"
            @change="onFileSelect"
            accept="image/*"
            class="hidden"
          />
          <div class="text-center">
            <svg
              class="mx-auto h-12 w-12 text-gray-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            <p class="mt-2 text-sm text-gray-600">
              <span class="font-semibold text-indigo-600">Click to upload</span>
              or drag and drop
            </p>
            <p class="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
            <p
              v-if="selectedFile"
              class="mt-2 text-sm font-medium text-green-600"
            >
              ✓ {{ selectedFile.name }}
            </p>
          </div>
        </div>

        <div class="flex gap-3">
          <button
            @click="runAutoAnnotate"
            :disabled="!selectedFile || isLoading"
            class="flex-1 bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95 shadow-md"
          >
            <span v-if="!isLoading" class="flex items-center justify-center">
              <svg
                class="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              Auto-Annotate
            </span>
            <span v-else class="flex items-center justify-center">
              <svg
                class="animate-spin h-5 w-5 mr-2"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Processing...
            </span>
          </button>

          <button
            v-if="masksB64.length > 0"
            @click="downloadAnnotations"
            class="bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 transition-all transform hover:scale-105 active:scale-95 shadow-md"
          >
            <svg
              class="w-5 h-5 inline mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
              />
            </svg>
            Download
          </button>

          <button
            v-if="imagePreview"
            @click="clearImage"
            class="bg-gray-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-700 transition-all transform hover:scale-105 active:scale-95 shadow-md"
          >
            <svg
              class="w-5 h-5 inline mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            Clear
          </button>
        </div>

        <!-- Error Message -->
        <div
          v-if="errorMessage"
          class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg"
        >
          <div class="flex">
            <svg
              class="h-5 w-5 text-red-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Error</h3>
              <p class="text-sm text-red-700 mt-1">{{ errorMessage }}</p>
            </div>
            <button @click="errorMessage = ''" class="ml-auto">
              <svg
                class="h-5 w-5 text-red-400 hover:text-red-600"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Success Message -->
        <div
          v-if="successMessage"
          class="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg"
        >
          <div class="flex">
            <svg
              class="h-5 w-5 text-green-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
            <p class="ml-3 text-sm text-green-700">{{ successMessage }}</p>
            <button @click="successMessage = ''" class="ml-auto">
              <svg
                class="h-5 w-5 text-green-400 hover:text-green-600"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Canvas with zoom controls -->
      <div v-if="imagePreview" class="bg-white rounded-lg shadow-xl p-4">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-gray-800">
            Annotation Results
          </h2>
          <div class="flex gap-2">
            <button
              @click="zoomOut"
              class="p-2 bg-gray-200 hover:bg-gray-300 rounded transition"
              title="Zoom Out"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7"
                />
              </svg>
            </button>
            <button
              @click="resetZoom"
              class="px-3 py-2 bg-gray-200 hover:bg-gray-300 rounded transition text-sm font-medium"
            >
              {{ Math.round(zoomLevel * 100) }}%
            </button>
            <button
              @click="zoomIn"
              class="p-2 bg-gray-200 hover:bg-gray-300 rounded transition"
              title="Zoom In"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"
                />
              </svg>
            </button>
          </div>
        </div>
        <div class="overflow-auto max-h-[70vh] border rounded-lg">
          <Canvas
            :image-src="imagePreview"
            :masks-b64="masksB64"
            :zoom="zoomLevel"
          />
        </div>
      </div>
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
const isLoading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const isDragging = ref(false);
const fileInputRef = ref<HTMLInputElement | null>(null);
const zoomLevel = ref(1);

const triggerFileInput = () => {
  fileInputRef.value?.click();
};

const onFileSelect = (e: Event) => {
  const input = e.target as HTMLInputElement;
  if (input.files?.[0]) {
    processFile(input.files[0]);
  }
};

const onDrop = (e: DragEvent) => {
  isDragging.value = false;
  const files = e.dataTransfer?.files;
  if (files?.[0]) {
    processFile(files[0]);
  }
};

const processFile = (file: File) => {
  errorMessage.value = "";
  successMessage.value = "";

  // Validate file type
  if (!file.type.startsWith("image/")) {
    errorMessage.value = "Please select a valid image file";
    return;
  }

  // Validate file size (10MB)
  if (file.size > 10 * 1024 * 1024) {
    errorMessage.value = "Image size must be less than 10MB";
    return;
  }

  selectedFile.value = file;
  imagePreview.value = URL.createObjectURL(file);
  masksB64.value = [];
  zoomLevel.value = 1;
  successMessage.value = `Image "${file.name}" loaded successfully`;
  setTimeout(() => (successMessage.value = ""), 3000);
};

const runAutoAnnotate = async () => {
  if (!selectedFile.value) return;

  isLoading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  const formData = new FormData();
  formData.append("image", selectedFile.value);
  formData.append("prompts", prompt.value);

  try {
    const res = await api.post("/annotate", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    masksB64.value = res.data.masks_b64;

    if (masksB64.value.length === 0) {
      errorMessage.value =
        "No objects detected. Try different prompts or another image.";
    } else {
      successMessage.value = `Successfully detected ${masksB64.value.length} object(s)!`;
      setTimeout(() => (successMessage.value = ""), 3000);
    }
  } catch (err: any) {
    console.error("Annotation failed", err);
    errorMessage.value =
      err.response?.data?.detail ||
      err.message ||
      "Failed to generate annotations. Please try again.";
  } finally {
    isLoading.value = false;
  }
};

const downloadAnnotations = () => {
  if (!imagePreview.value || masksB64.value.length === 0) return;

  // Create a canvas to combine image and masks
  const canvas = document.createElement("canvas");
  const img = new Image();

  img.onload = () => {
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Draw original image
    ctx.drawImage(img, 0, 0);

    // Draw masks
    masksB64.value.forEach((maskB64, index) => {
      const maskImg = new Image();
      maskImg.src = `data:image/png;base64,${maskB64}`;
      maskImg.onload = () => {
        ctx.globalAlpha = 0.5;
        ctx.drawImage(maskImg, 0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 1.0;

        // Download when last mask is drawn
        if (index === masksB64.value.length - 1) {
          canvas.toBlob((blob) => {
            if (!blob) return;
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `annotated_${selectedFile.value?.name || "image.png"}`;
            a.click();
            URL.revokeObjectURL(url);
            successMessage.value = "Annotations downloaded successfully!";
            setTimeout(() => (successMessage.value = ""), 3000);
          });
        }
      };
    });
  };

  img.src = imagePreview.value;
};

const clearImage = () => {
  selectedFile.value = null;
  imagePreview.value = null;
  masksB64.value = [];
  errorMessage.value = "";
  successMessage.value = "";
  zoomLevel.value = 1;
};

const zoomIn = () => {
  zoomLevel.value = Math.min(zoomLevel.value + 0.25, 3);
};

const zoomOut = () => {
  zoomLevel.value = Math.max(zoomLevel.value - 0.25, 0.25);
};

const resetZoom = () => {
  zoomLevel.value = 1;
};
</script>
