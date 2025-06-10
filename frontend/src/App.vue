<!-- frontend/src/App.vue -->
<template>
  <div id="app-container">
    <header class="text-center mb-12 md:mb-16 py-8 bg-slate-200">
      <h1 class="text-4xl md:text-5xl font-bold text-slate-900">
        <span class="text-indigo-600">RTOS V2X</span> 智能运维平台<span class="text-indigo-600">原子能力验证平台</span>
      </h1>
      <p class="mt-4 text-lg md:text-xl text-slate-600 max-w-3xl mx-auto">
        仅用于内部运维功能穿刺预研，正式平台为<a href="https://fireeye.rnd.huawei.com/fireeye/toolbox" class="text-indigo-600 hover:underline" target="_blank">"RTOS运维平台"</a> (链接将在新标签页打开)
      </p>
    </header>

    <div class="container mx-auto px-6 py-12 md:py-20">
        <!-- 功能模块网格布局 -->
        <main class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">

            <!-- 卡片 1: 性能瓶颈分析 -->
            <a href="https://fireeye.rnd.huawei.com/fireeye/parse/result?bizType=perf_analysis" target="_blank" class="feature-card block bg-white p-8 rounded-xl shadow-lg border border-slate-200">
                <div class="flex items-center justify-center h-16 w-16 rounded-full bg-indigo-100 mb-6">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-indigo-600"><path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/></svg>
                </div>
                <h2 class="text-xl font-bold text-slate-900 mb-3">性能瓶颈分析</h2>
                <p class="text-slate-600 leading-relaxed">
                    从系统级到符号级的逐层下钻，精准分析高频函数与调度切换，定位性能热点。
                </p>
            </a>

            <!-- 卡片 2: 微架构分析 -->
            <a href="http://rtosdfx.rnd.huawei.com:8888/view/performance_spe_analyzer/topdown_microarchitecture_analysis_report.html" target="_blank" class="feature-card block bg-white p-8 rounded-xl shadow-lg border border-slate-200">
                <div class="flex items-center justify-center h-16 w-16 rounded-full bg-pink-100 mb-6">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-pink-600"><rect x="5" y="5" width="14" height="14" rx="2" /><path d="M9 9h6v6H9z" /><path d="M9 1v4" /><path d="M15 1v4" /><path d="M9 23v-4" /><path d="M15 23v-4" /><path d="M1 9h4" /><path d="M1 15h4" /><path d="M23 9h-4" /><path d="M23 15h-4" /></svg>
                </div>
                <h2 class="text-xl font-bold text-slate-900 mb-3">微架构分析</h2>
                <p class="text-slate-600 leading-relaxed">
                    深入CPU微架构，分析缓存命中率、指令流水线等关键硬件性能指标。
                </p>
            </a>

            <!-- 卡片 3: 调度轨迹分析 -->
            <a href="https://fireeye.rnd.huawei.com/fireeye/parse/result?bizType=sched_analysis" target="_blank" class="feature-card block bg-white p-8 rounded-xl shadow-lg border border-slate-200">
                <div class="flex items-center justify-center h-16 w-16 rounded-full bg-purple-100 mb-6">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-600"><path d="M6 3v12"/><path d="M18 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/><path d="M6 21a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/><path d="M18 21a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/><path d="M6 15V9a3 3 0 0 1 3-3h6a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H9a3 3 0 0 1-3-3z"/></svg>
                </div>
                <h2 class="text-xl font-bold text-slate-900 mb-3">调度轨迹分析</h2>
                <p class="text-slate-600 leading-relaxed">
                    精细化追踪线程调度过程，识别抢占、阻塞点，提升系统并发效率。
                </p>
            </a>

            <!-- 卡片 4: 中断轨迹分析 -->
            <a href="https://rtosdfx.rnd.huawei.com/application/" target="_blank" class="feature-card block bg-white p-8 rounded-xl shadow-lg border border-slate-200">
                <div class="flex items-center justify-center h-16 w-16 rounded-full bg-amber-100 mb-6">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber-600"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                </div>
                <h2 class="text-xl font-bold text-slate-900 mb-3">中断轨迹分析</h2>
                <p class="text-slate-600 leading-relaxed">
                    可视化中断响应流程，分析中断延迟与频率，优化系统实时性。
                </p>
            </a>

            <!-- 卡片 5: 启动时序建模 -->
            <a href="https://fireeye.rnd.huawei.com/fireeye/parse/result?bizType=fast_start_timing" target="_blank" class="feature-card block bg-white p-8 rounded-xl shadow-lg border border-slate-200">
                <div class="flex items-center justify-center h-16 w-16 rounded-full bg-sky-100 mb-6">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-sky-600"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.3.5-3.5-1.17-1.17-2.65-.84-3.5-.5Z"/><path d="m12 15.5 3.5-3.5C12.84 9.36 12.5 6.5 15 4c.66-.66 1.5-1 2.5-1s1.84.34 2.5 1c2.5 2.5 1.36 5.16-1.5 7.84l-3.5 3.5"/><path d="m20 21-1.5-1.5"/><path d="M17 18a2 2 0 0 0-2-2"/><path d="m15 13-3.5-3.5"/></svg>
                </div>
                <h2 class="text-xl font-bold text-slate-900 mb-3">启动时序建模</h2>
                <p class="text-slate-600 leading-relaxed">
                    通过时序火焰图和差分分析，可视化启动流程，快速发现性能退化与优化点。
                </p>
            </a>

            <!-- 卡片 6: 内存小型化分析 -->
            <a href="https://fireeye.rnd.huawei.com/fireeye/parse/result?bizType=memory_analysis" target="_blank" class="feature-card block bg-white p-8 rounded-xl shadow-lg border border-slate-200">
                <div class="flex items-center justify-center h-16 w-16 rounded-full bg-emerald-100 mb-6">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-600"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 7h4"/><path d="M7 12h4"/><path d="M7 17h4"/><path d="M15 7h1"/><path d="M15 12h1"/><path d="M15 17h1"/></svg>
                </div>
                <h2 class="text-xl font-bold text-slate-900 mb-3">内存小型化分析</h2>
                <p class="text-slate-600 leading-relaxed">
                    覆盖全局、业务进程与OS底噪的精细化分析，全面洞悉动静态内存开销与分布。
                </p>
            </a>

            <!-- 卡片 7: 异常日志辅助定位 -->
            <a href="https://rtosdfx.rnd.huawei.com/application/" target="_blank" class="feature-card block bg-white p-8 rounded-xl shadow-lg border border-slate-200">
                <div class="flex items-center justify-center h-16 w-16 rounded-full bg-rose-100 mb-6">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-rose-600"><path d="m8 6 4-4 4 4"/><path d="M12 2v10.3a4 4 0 0 1-1.172 2.872L4 22"/><path d="m20 22-5-5"/><path d="M16 13.3a4 4 0 0 0 1.172-2.872V2"/></svg>
                </div>
                <h2 class="text-xl font-bold text-slate-900 mb-3">异常日志辅助定位</h2>
                <p class="text-slate-600 leading-relaxed">
                    利用日志泳道图聚合上下文，结合AI辅助诊断，高效识别异常模式与根因。
                </p>
            </a>

            <!-- 卡片 8: 运维原子能力试验场 (新增) -->
            <a href="http://rtosdfx.rnd.huawei.com:8888/tree" target="_blank" class="feature-card block bg-white p-8 rounded-xl shadow-lg border border-slate-200">
                <div class="flex items-center justify-center h-16 w-16 rounded-full bg-teal-100 mb-6">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-teal-600">
                       <path d="M4.5 3h15"/>
                       <path d="M6 3v16a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V3"/>
                       <path d="M6 14h12"/>
                     </svg>
                </div>
                <h2 class="text-xl font-bold text-slate-900 mb-3">运维原子能力试验场</h2>
                <p class="text-slate-600 leading-relaxed">
                    (基于jupyter_notebook) 探索、测试和验证运维场景下的各种原子能力。
                </p>
            </a>
        </main>
    </div>

    <footer class="text-center mt-12 md:mt-20 pt-8 border-t border-slate-200 pb-8">
         <p class="text-slate-500">未来更多功能模块将在此处呈现。</p>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';

onMounted(() => {
  console.log("App.vue mounted. Feature cards are now part of the template.");
  // The script to open links in new tabs from the original HTML is not needed here
  // as all links now have target="_blank" directly in their <a> tags.
});
</script>

<style>
/* Global styles can go here or be imported from external CSS files */
/* Tailwind is expected to be set up via postcss, so its classes should work */
body {
    font-family: 'Inter', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.feature-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}
</style>
