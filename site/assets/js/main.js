/* Educore — interactions & animations (vanilla, no dependencies) */
(() => {
  const d = document, root = d.documentElement;
  root.classList.add('js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];

  addEventListener('load', () => d.body.classList.add('loaded'));

  /* Header shrink, scroll progress, back-to-top */
  const header = $('.header'), prog = $('.progress'), topBtn = $('.fab .top');
  const onScroll = () => {
    const y = scrollY, h = d.body.scrollHeight - innerHeight;
    header && header.classList.toggle('scrolled', y > 30);
    prog && (prog.style.transform = `scaleX(${h > 0 ? y / h : 0})`);
    topBtn && topBtn.classList.toggle('show', y > 700);
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  topBtn && topBtn.addEventListener('click', () => scrollTo({ top: 0, behavior: 'smooth' }));

  /* Mobile menu */
  const burger = $('.burger');
  burger && burger.addEventListener('click', () => {
    const open = d.body.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open);
    $$('.mobile-menu a, .mobile-menu .m-toggle').forEach((a, i) => a.style.transitionDelay = open ? `${i * 30}ms` : '0ms');
  });
  $$('.mobile-menu a').forEach(a => a.addEventListener('click', () => d.body.classList.remove('menu-open')));

  /* Dropdowns open on click; close on outside click or Escape */
  const drops = $$('.has-drop');
  const closeAll = except => drops.forEach(li => {
    if (li === except) return;
    li.classList.remove('open'); $('.nav-link', li).setAttribute('aria-expanded', 'false');
  });
  drops.forEach(li => {
    const btn = $('.nav-link', li);
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const open = !li.classList.contains('open');
      closeAll(li); li.classList.toggle('open', open); btn.setAttribute('aria-expanded', open);
    });
  });
  d.addEventListener('click', e => { if (!e.target.closest('.has-drop')) closeAll(); });
  d.addEventListener('keydown', e => { if (e.key === 'Escape') closeAll(); });
  $$('.mobile-menu .m-toggle').forEach(t => t.addEventListener('click', () => {
    const open = t.getAttribute('aria-expanded') !== 'true';
    $$('.mobile-menu .m-toggle').forEach(o => o.setAttribute('aria-expanded', 'false'));
    t.setAttribute('aria-expanded', open);
  }));

  /* Split headline words */
  $$('[data-split]').forEach(el => {
    let i = 0;
    const walk = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.append(part); return; }
            const w = d.createElement('span'); w.className = 'w';
            const s = d.createElement('span'); s.textContent = part; s.style.setProperty('--i', i++);
            w.append(s); frag.append(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && !n.classList.contains('rotator')) {
          if (n.classList.contains('grad-text') && n.tagName === 'SPAN') {
            const frag = d.createDocumentFragment();
            n.textContent.split(/(\s+)/).forEach(part => {
              if (!part) return;
              if (/^\s+$/.test(part)) { frag.append(' '); return; }
              const w = d.createElement('span'); w.className = 'w';
              const s = d.createElement('span'); s.className = 'grad-text'; s.textContent = part; s.style.setProperty('--i', i++);
              w.append(s); frag.append(w);
            });
            n.replaceWith(frag);
          } else if (n.tagName !== 'BR') walk(n);
        }
      });
    };
    walk(el); el.classList.add('split-words');
  });

  /* Reveal on scroll (+ stagger children) */
  $$('[data-stagger]').forEach(p => [...p.children].forEach((c, i) => {
    if (!c.hasAttribute('data-reveal')) c.setAttribute('data-reveal', p.dataset.stagger || '');
    c.style.setProperty('--d', `${i * 0.08}s`);
  }));
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('in');
    io.unobserve(e.target);
  }), { threshold: .14, rootMargin: '0px 0px -40px 0px' });
  $$('[data-reveal],.split-words').forEach(el => io.observe(el));

  /* Counters */
  const fmt = n => n.toLocaleString('en-US');
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target, to = +el.dataset.count, dur = 2000, t0 = performance.now();
    const tick = t => {
      const p = Math.min((t - t0) / dur, 1), v = Math.round(to * (1 - Math.pow(1 - p, 4)));
      el.textContent = fmt(v); if (p < 1) requestAnimationFrame(tick);
    };
    reduce ? el.textContent = fmt(to) : requestAnimationFrame(tick);
    cio.unobserve(el);
  }), { threshold: .5 });
  $$('[data-count]').forEach(el => cio.observe(el));

  /* Word rotator */
  $$('.rotator').forEach(r => {
    const items = $$('span', r); let i = 0;
    const w = Math.max(...items.map(s => s.getBoundingClientRect().width));
    items[0].classList.add('on');
    if (items.length < 2 || reduce) return;
    setInterval(() => {
      items[i].classList.remove('on'); items[i].classList.add('out');
      const prev = items[i]; setTimeout(() => prev.classList.remove('out'), 800);
      i = (i + 1) % items.length; items[i].classList.add('on');
    }, 2600);
  });

  /* Hero slideshow (images or videos) synced with tabs */
  $$('[data-slides]').forEach(wrap => {
    const slides = [...wrap.children], tabs = $$(`[data-slide-tabs="${wrap.dataset.slides}"] button`);
    let i = 0, timer;
    const go = n => {
      slides[i].classList.remove('on'); tabs[i] && tabs[i].classList.remove('on');
      if (slides[i].tagName === 'VIDEO') slides[i].pause();
      i = n; const s = slides[i]; s.classList.add('on');
      if (s.tagName === 'VIDEO' && !reduce) { s.currentTime = 0; s.play().catch(() => {}); }
      const nx = slides[(i + 1) % slides.length]; if (nx.tagName === 'VIDEO') nx.preload = 'auto';
      if (tabs[i]) { void tabs[i].offsetWidth; tabs[i].classList.add('on'); }
      clearTimeout(timer); timer = setTimeout(() => go((i + 1) % slides.length), 5000);
    };
    tabs.forEach((t, n) => t.addEventListener('click', () => go(n)));
    go(0);
  });

  /* Spotlight cards */
  $$('.spot').forEach(c => c.addEventListener('pointermove', e => {
    const r = c.getBoundingClientRect();
    c.style.setProperty('--mx', `${e.clientX - r.left}px`);
    c.style.setProperty('--my', `${e.clientY - r.top}px`);
  }));

  /* 3D tilt */
  if (!reduce && matchMedia('(hover:hover)').matches) {
    $$('[data-tilt]').forEach(c => {
      c.addEventListener('pointermove', e => {
        const r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        c.style.transform = `perspective(900px) rotateX(${-y * 8}deg) rotateY(${x * 8}deg) translateY(-4px)`;
      });
      c.addEventListener('pointerleave', () => c.style.transform = '');
    });
    /* Magnetic buttons */
    $$('.btn[data-magnetic]').forEach(b => {
      b.addEventListener('pointermove', e => {
        const r = b.getBoundingClientRect();
        b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * .18}px,${(e.clientY - r.top - r.height / 2) * .3}px)`;
      });
      b.addEventListener('pointerleave', () => b.style.transform = '');
    });
    /* Parallax */
    const px = $$('[data-parallax]');
    if (px.length) {
      const run = () => px.forEach(el => {
        const r = el.getBoundingClientRect(), c = r.top + r.height / 2 - innerHeight / 2;
        el.style.translate = `0 ${c * -(+el.dataset.parallax || .08)}px`;
      });
      addEventListener('scroll', () => requestAnimationFrame(run), { passive: true }); run();
    }
  }

  /* Sticky feature scroller */
  $$('.scroller').forEach(sc => {
    const steps = $$('.step', sc), imgs = $$('.screen img', sc);
    const set = i => { steps.forEach((s, n) => s.classList.toggle('on', n === i)); imgs.forEach((m, n) => m.classList.toggle('on', n === i)); };
    const sio = new IntersectionObserver(es => es.forEach(e => e.isIntersecting && set(steps.indexOf(e.target))), { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach((s, i) => { sio.observe(s); s.addEventListener('click', () => set(i)); });
    set(0);
  });

  /* Mobile apps switcher */
  $$('.apps').forEach(a => {
    const btns = $$('.app-btn', a), imgs = $$('.phone img', a); let i = 0, t;
    const set = n => { i = n; btns.forEach((b, k) => b.classList.toggle('on', k === n)); imgs.forEach((m, k) => m.classList.toggle('on', k === n)); };
    const auto = () => { clearInterval(t); t = setInterval(() => set((i + 1) % btns.length), 4500); };
    btns.forEach((b, n) => b.addEventListener('click', () => { set(n); auto(); }));
    set(0); if (!reduce) auto();
  });

  /* Tabs */
  $$('[data-tabs]').forEach(g => {
    const btns = $$('button', g), panels = $$(`[data-panel-of="${g.dataset.tabs}"]`);
    btns.forEach((b, i) => b.addEventListener('click', () => {
      btns.forEach(x => x.classList.toggle('on', x === b));
      panels.forEach((p, k) => p.classList.toggle('on', k === i));
    }));
  });

  /* FAQ: one open at a time */
  $$('.faq').forEach(f => $$('details', f).forEach(dt => dt.addEventListener('toggle', () => {
    if (dt.open) $$('details', f).forEach(o => o !== dt && (o.open = false));
  })));

  /* Legal TOC highlight */
  const toc = $$('.legal nav a');
  if (toc.length) {
    const map = new Map(toc.map(a => [a.hash.slice(1), a]));
    const lio = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { toc.forEach(a => a.classList.remove('on')); map.get(e.target.id)?.classList.add('on'); }
    }), { rootMargin: '-20% 0px -70% 0px' });
    $$('.prose h3[id]').forEach(h => lio.observe(h));
  }

  /* Multi-step form */
  $$('form[data-steps]').forEach(form => {
    const steps = $$('.fstep', form), marks = $$('.stepper span', form);
    const prev = $('[data-prev]', form), next = $('[data-next]', form), send = $('[data-send]', form);
    let i = 0;
    const show = (n, scroll = true) => {
      i = n;
      steps.forEach((s, k) => s.classList.toggle('on', k === n));
      marks.forEach((m, k) => { m.classList.toggle('on', k === n); m.classList.toggle('done', k < n); });
      prev.hidden = n === 0; next.hidden = n === steps.length - 1; send.hidden = n !== steps.length - 1;
      if (n === steps.length - 1) review();
      if (scroll) form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    const valid = () => {
      const step = steps[i];
      for (const el of $$('input,select,textarea', step)) if (!el.checkValidity()) { el.reportValidity(); return false; }
      const group = $('[data-min-one]', step), err = $('.step-err', step);
      if (group && !$$('input:checked', group).length) { err && err.classList.add('show'); return false; }
      err && err.classList.remove('show');
      return true;
    };
    const review = () => {
      const fd = new FormData(form), rows = [];
      $$('[data-label]', form).forEach(el => {
        const v = el.type === 'checkbox' ? fd.getAll(el.name).join(', ') : fd.get(el.name);
        if (!rows.some(r => r[0] === el.dataset.label)) rows.push([el.dataset.label, v || 'Not provided']);
      });
      $('.review', form).innerHTML = rows.map(([k, v]) => `<div><dt>${k}</dt><dd></dd></div>`).join('');
      $$('.review dd', form).forEach((dd, k) => dd.textContent = rows[k][1]);
    };
    next.addEventListener('click', () => valid() && show(i + 1));
    prev.addEventListener('click', () => show(i - 1));
    $$('[data-min-one] input', form).forEach(c => c.addEventListener('change', () => $('.step-err', form)?.classList.remove('show')));
    form.addEventListener('reset', () => setTimeout(() => show(0, false)));
    show(0, false);
  });

  /* Videos: YouTube loads only when the visitor presses play (privacy-enhanced mode) */
  $$('.vid[data-yt]').forEach(v => {
    $('.vid-play', v).addEventListener('click', () => {
      const f = d.createElement('iframe');
      f.src = `https://www.youtube-nocookie.com/embed/${v.dataset.yt}?autoplay=1&rel=0&modestbranding=1`;
      f.title = v.dataset.title;
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      v.classList.add('playing'); v.replaceChildren(f);
      $$('[data-slides] video').forEach(x => x.pause());
    });
  });

  /* Forms — front-end only; wire `action` to your backend */
  $$('form[data-demo]').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault();
    if (!f.reportValidity()) return;
    const t = $('.toast'); if (!t) return;
    t.querySelector('span').textContent = f.dataset.demo;
    t.classList.add('show'); f.reset();
    setTimeout(() => t.classList.remove('show'), 3800);
  }));
})();
