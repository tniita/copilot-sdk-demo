<template>
  <div class="slidev-layout cover">
    <!-- Copilot-style floating orbs -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="orb orb-blue"></div>
      <div class="orb orb-purple"></div>
    </div>
    <div class="my-auto w-full relative z-10">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 6s ease-in-out infinite;
}

.orb-blue {
  width: 300px;
  height: 300px;
  background: #58a6ff;
  top: -50px;
  right: -50px;
  animation-delay: 0s;
}

.orb-purple {
  width: 250px;
  height: 250px;
  background: #7c3aed;
  bottom: -30px;
  left: -30px;
  animation-delay: -3s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(20px, -20px) scale(1.1);
  }
}
</style>
