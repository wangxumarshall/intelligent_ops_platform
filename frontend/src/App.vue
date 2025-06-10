<!-- frontend/src/App.vue -->
<template>
  <div id="app-container">
    <!-- Router view will render here if Vue Router is used -->
    <!-- <router-view /> -->

    <!-- Placeholder for content from the old index.html -->
    <!-- You would typically move the body content of public/index.html here -->
    <!-- or into specific views/components -->
    <header class="text-center mb-12 md:mb-16 py-8 bg-slate-200">
      <h1 class="text-4xl md:text-5xl font-bold text-slate-900">
        <span class="text-indigo-600">RTOS V2X</span> 智能运维平台<span class="text-indigo-600">原子能力验证平台</span>
      </h1>
      <p class="mt-4 text-lg md:text-xl text-slate-600 max-w-3xl mx-auto">
        仅用于内部运维功能穿刺预研，正式平台为<a href="https://fireeye.rnd.huawei.com/fireeye/toolbox" class="text-indigo-600 hover:underline" target="_blank">"RTOS运维平台"</a> (链接将在新标签页打开)
      </p>
    </header>

    <div class="container mx-auto px-6 py-12 md:py-20">
      <p class="text-center text-slate-700">
        Frontend is loading. If you see this, the Vue app is mounted.
        The actual content from the original HTML needs to be migrated into Vue components/views.
      </p>
      <p class="text-center mt-4 text-sm text-slate-500">
        (The feature cards from the original HTML are not rendered here yet.)
      </p>
      <!-- Example of how one might integrate one of the cards as a component -->
      <!-- <FeatureCard title="性能瓶颈分析" description="从系统级到符号级的逐层下钻..." href="https://example.com" icon="dashboard" /> -->
    </div>

    <footer class="text-center mt-12 md:mt-20 pt-8 border-t border-slate-200 pb-8">
         <p class="text-slate-500">未来更多功能模块将在此处呈现。</p>
    </footer>
  </div>
</template>

<script setup>
// No script logic needed for this basic placeholder yet
// In a real app, you'd import components, define props, data, methods, etc.
import { onMounted } from 'vue';

onMounted(() => {
  // The script to open links in new tabs was in the original index.html.
  // That script was a global event listener. For Vue, it's often better to handle
  // such behavior more explicitly, e.g., by always adding target="_blank"
  // to external links in templates, or by creating a directive for links.
  // The `target="_blank"` has been added directly to the example link in the template.
  console.log("App.vue mounted. External link handling should be done via target='_blank' in templates.");
});
</script>

<style>
/* Global styles can go here or be imported from external CSS files */
/* Tailwind is expected to be set up via postcss, so its classes should work */
/* Body styles are applied here for the whole app if not using a separate global CSS file imported in main.js */
/* However, it's common to have body styles in a global css file or handled by Tailwind's preflight. */
/* For simplicity, and as per original instructions, styles are here. */

/* Using @apply for body in a <style> tag in a .vue component might require specific setup,
   or might not be the standard way if using Tailwind's PostCSS processing.
   Typically, Tailwind's base styles (Preflight) handle body styling.
   If you import './assets/tailwind.css' in main.js, and that file has @tailwind base,
   then body styling should be covered.
   Let's remove the @apply here and assume tailwind.css handles it.
*/
body {
    font-family: 'Inter', sans-serif; /* Ensure Inter font is applied if not covered by Tailwind base */
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Feature card styles from original HTML - can be component-specific or global */
/* These are kept here for now as per original instructions. */
.feature-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}
</style>
