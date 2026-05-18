/* vzw Werken Glorieux - shared scripts
 * Loads header/footer partials, sets active nav, mobile menu toggle, cookie banner.
 */

(function () {
  'use strict';

  // -----------------------------------------------------------
  // Partial loader. Allows /js/partials/header.html etc.
  // Falls back gracefully if a partial isn't fetched (e.g. file://)
  // -----------------------------------------------------------
  async function loadPartials() {
    const slots = document.querySelectorAll('[data-include]');
    for (const slot of slots) {
      const url = slot.getAttribute('data-include');
      try {
        const res = await fetch(url);
        if (!res.ok) throw new Error('fetch failed');
        slot.innerHTML = await res.text();
      } catch (e) {
        // swallow — partials may not load on file:// without server
        console.warn('Partial not loaded:', url);
      }
    }
  }

  // -----------------------------------------------------------
  // Mark active nav item based on current page slug
  // -----------------------------------------------------------
  function markActiveNav() {
    const pathFile = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    const slug = pathFile.replace('.html', '');
    document.querySelectorAll('.nav-primary a, .nav-mobile a').forEach(a => {
      const target = a.getAttribute('href') || '';
      const tFile = target.split('/').pop().replace('.html', '').toLowerCase();
      if (tFile === slug || (slug === 'index' && (tFile === '' || tFile === 'index'))) {
        a.classList.add('is-active');
      }
    });
  }

  // -----------------------------------------------------------
  // Mobile nav toggle
  // -----------------------------------------------------------
  function bindMobileNav() {
    const toggle = document.querySelector('.nav-toggle');
    const mobile = document.querySelector('.nav-mobile');
    if (!toggle || !mobile) return;
    toggle.addEventListener('click', () => {
      mobile.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded',
        mobile.classList.contains('is-open') ? 'true' : 'false');
    });
  }

  // -----------------------------------------------------------
  // Cookie banner — minimal opt-in flow
  // -----------------------------------------------------------
  function bindCookieBanner() {
    const banner = document.querySelector('.cookie-banner');
    if (!banner) return;
    if (localStorage.getItem('wg-cookies-accepted') === 'yes') return;
    banner.classList.add('is-visible');
    const btn = banner.querySelector('button');
    if (btn) {
      btn.addEventListener('click', () => {
        localStorage.setItem('wg-cookies-accepted', 'yes');
        banner.classList.remove('is-visible');
      });
    }
  }

  // -----------------------------------------------------------
  // Init
  // -----------------------------------------------------------
  document.addEventListener('DOMContentLoaded', async () => {
    await loadPartials();
    markActiveNav();
    bindMobileNav();
    bindCookieBanner();
  });
})();
