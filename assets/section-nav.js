(() => {
  const links = new Map(Array.from(document.querySelectorAll('.nav-links a'), a => [a.hash.slice(1), a]));
  const sections = Array.from(document.querySelectorAll('main section[id]'));
  let current;
  let pending = false;

  function update() {
    pending = false;
    const top = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) + 2;
    const active = sections.filter(section => section.getBoundingClientRect().top <= top).pop();
    const atEnd = innerHeight + scrollY >= document.documentElement.scrollHeight - 2;
    const next = links.get(atEnd ? 'contact' : active?.id);
    if (next === current) return;
    current?.removeAttribute('aria-current');
    next?.setAttribute('aria-current', 'location');
    current = next;
  }

  function schedule() {
    if (!pending) {
      pending = true;
      requestAnimationFrame(update);
    }
  }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  window.addEventListener('pageshow', schedule);
  update();
})();
