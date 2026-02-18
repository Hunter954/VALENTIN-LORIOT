/**
 * Interações principais:
 * - Hero com scroll horizontal (wheel vertical vira scroll horizontal dentro do hero)
 * - Autoplay muted (hero + showreel + works) quando em view
 * - Transição suave "Apple-like" quando o usuário tenta passar do último hero video
 */
(function () {
  const scroller = document.getElementById("heroScroller");
  const heroSection = document.getElementById("home");
  if (!scroller || !heroSection) return;

  const slides = Array.from(scroller.querySelectorAll(".hero-slide"));
  const vids = slides.map(s => s.querySelector("video")).filter(Boolean);
  const dots = Array.from(document.querySelectorAll(".hero-dot"));
  const about = document.getElementById("about");

  let isAutoJumping = false;
  let revealProgress = 0; // 0..1
  let revealRAF = null;

  function setActiveDot(index){
    dots.forEach((d,i)=> d.classList.toggle("active", i===index));
  }

  async function safePlay(v){
    try {
      if (!v) return;
      v.muted = true;
      v.playsInline = true;
      await v.play();
    } catch (_) {}
  }

  function pauseAll(except){
    vids.forEach(v => { if (v && v !== except) v.pause(); });
  }

  // Intersection observer: qual slide está mais visível (horizontal)
  const io = new IntersectionObserver((entries) => {
    const visible = entries
      .filter(e => e.isIntersecting)
      .sort((a,b)=> b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;

    const slide = visible.target;
    const idx = Number(slide.dataset.index || "0");
    const v = slide.querySelector("video");
    setActiveDot(idx);
    pauseAll(v);
    safePlay(v);
  }, { root: scroller, threshold: [0.55, 0.75] });

  slides.forEach(s => io.observe(s));
  setActiveDot(0);
  safePlay(vids[0]);

  function atLastSlide(){
    if (!slides.length) return false;
    const maxScroll = scroller.scrollWidth - scroller.clientWidth;
    return scroller.scrollLeft >= (maxScroll - 2);
  }

  function applyReveal(p){
    if (!about) return;
    // Faz o About "subir" por cima aos poucos
    const y = (1 - p) * 80; // px
    about.style.transform = `translateY(${y}px)`;
    about.style.opacity = String(Math.min(1, Math.max(0.12, p)));
    // Efeito no hero (fade suave)
    scroller.style.filter = `brightness(${1 - p*0.12}) saturate(${1 - p*0.08})`;
  }

  function resetReveal(){
    revealProgress = 0;
    if (!about) return;
    about.style.transform = "";
    about.style.opacity = "";
    scroller.style.filter = "";
  }

  function jumpToAbout(){
    if (!about) return;
    isAutoJumping = true;
    about.scrollIntoView({ behavior: "smooth", block: "start" });
    // cooldown
    setTimeout(()=> {
      isAutoJumping = false;
      resetReveal();
    }, 900);
  }

  function pumpReveal(){
    if (revealRAF) cancelAnimationFrame(revealRAF);
    revealRAF = requestAnimationFrame(()=> applyReveal(revealProgress));
  }

  // --- HERO: scroll vertical vira troca de slide (estilo Apple) ---
  // O problema do "travamento" costuma acontecer quando o wheel é capturado
  // fora do momento certo. Aqui só interceptamos quando o HERO está praticamente
  // "pinned" na viewport (ocupando a tela).
  function heroPinned(){
    const r = heroSection.getBoundingClientRect();
    const topOk = r.top >= -2 && r.top <= 2;
    const bottomOk = r.bottom >= (window.innerHeight - 2);
    return topOk && bottomOk;
  }

  function currentIndex(){
    const w = scroller.clientWidth || 1;
    return Math.round(scroller.scrollLeft / w);
  }

  function goToIndex(idx){
    const maxIdx = Math.max(0, slides.length - 1);
    const clamped = Math.max(0, Math.min(maxIdx, idx));
    const left = clamped * scroller.clientWidth;
    scroller.scrollTo({ left, behavior: "smooth" });
  }

  let wheelLock = false;
  function lockWheel(ms=650){
    wheelLock = true;
    setTimeout(()=> (wheelLock = false), ms);
  }

  window.addEventListener("wheel", (e) => {
    if (isAutoJumping) return;
    if (!heroPinned()) return; // não intercepta fora do hero
    if (wheelLock) { e.preventDefault(); return; }

    const dy = e.deltaY || 0;
    if (dy === 0) return;

    const idx = currentIndex();
    const maxIdx = Math.max(0, slides.length - 1);
    const goingNext = dy > 0;

    // Enquanto está nos vídeos 1/2/3, o scroll vertical vira troca de slide
    if (goingNext && idx < maxIdx){
      e.preventDefault();
      goToIndex(idx + 1);
      lockWheel();
      return;
    }
    if (!goingNext && idx > 0){
      e.preventDefault();
      goToIndex(idx - 1);
      lockWheel();
      return;
    }

    // No último slide: reveal MUITO suave antes de ir para o About
    if (goingNext && idx >= maxIdx){
      e.preventDefault();
      revealProgress = Math.min(1, revealProgress + Math.abs(dy) / 300);
      pumpReveal();
      if (revealProgress >= 1){
        lockWheel(900);
        jumpToAbout();
      } else {
        lockWheel(90);
      }
      return;
    }

    // Se o usuário sobe, desfaz o reveal
    if (!goingNext && revealProgress > 0){
      e.preventDefault();
      revealProgress = Math.max(0, revealProgress - Math.abs(dy) / 300);
      pumpReveal();
      lockWheel(90);
      return;
    }
  }, { passive: false });

  // Autoplay showreel quando em view
  const showreelVideos = Array.from(document.querySelectorAll(".showreel-video"));
  const gio = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      const v = e.target;
      if (e.isIntersecting) safePlay(v);
      else v.pause();
    });
  }, { threshold: 0.4 });
  showreelVideos.forEach(v=> gio.observe(v));

  // Works (Videos): toca apenas no hover
  const worksVideos = Array.from(document.querySelectorAll(".works-video"));
  worksVideos.forEach(v=>{
    v.muted = true;
    v.playsInline = true;
    try { v.pause(); } catch(_) {}
    const parent = v.closest('.works-item') || v;
    parent.addEventListener('mouseenter', ()=> safePlay(v));
    parent.addEventListener('mouseleave', ()=>{
      try { v.pause(); v.currentTime = 0; } catch (_) {}
    });
  });
})();
