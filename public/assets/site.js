// Mitsflix site: menu, live guide clock, forms.
(() => {
  const btn = document.querySelector('.menu-btn'), nav = document.querySelector('.nav');
  if (btn && nav) btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
    btn.textContent = open ? 'Close' : 'Menu';
  });

  // Referral links (mitsflix.com/pricing?ref=<friend's Discord username>) fill in the code, and it's remembered while they look around.
  try {
    const raw = (new URLSearchParams(location.search).get('ref') || '').trim().replace(/^@/, '');
    const fromUrl = /^mits-?/i.test(raw) ? raw.toUpperCase().replace(/[^A-Z0-9-]/g, '').slice(0, 12) : raw.toLowerCase().replace(/[^a-z0-9_.]/g, '').slice(0, 32);
    if (fromUrl) localStorage.setItem('mitsflix-ref', fromUrl);
    const code = fromUrl || localStorage.getItem('mitsflix-ref') || '';
    document.querySelectorAll('input[name=ref]').forEach((el) => { if (code && !el.value) el.value = code; });
  } catch (e) { /* storage unavailable: the box just stays empty */ }

  // Sign-up and reseller forms go straight to the Mitsflix team.
  document.querySelectorAll('form.order').forEach((form) => {
    const msg = form.querySelector('.form-msg'), submit = form.querySelector('button[type=submit]');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const data = Object.fromEntries(new FormData(form).entries());
      submit.disabled = true; const label = submit.textContent; submit.textContent = 'Sending…';
      msg.className = 'form-msg'; msg.textContent = '';
      try {
        const r = await fetch('https://mitsflix-tickets.sales-eea.workers.dev/order', {
          method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(data) });
        const j = await r.json().catch(() => ({}));
        if (!r.ok || !j.ok) throw new Error(j.error || 'Your details didn’t send. Check your connection and try again.');
        form.reset();
        msg.className = 'form-msg ok';
        msg.textContent = form.dataset.done || 'Sent. We’ll email you soon.';
        // Sign-ups with a Discord username get a private chat with us there.
        const join = document.createElement('a');
        join.href = '/discord'; join.textContent = 'Join our Discord';
        if (j.chat === 'opened') msg.textContent = 'Thanks! Your private chat with us is open in our Discord now. We’ll email your payment options too.';
        if (j.chat === 'pending') { msg.textContent = 'Thanks! We’ll email your payment options. '; msg.append(join, ' and your private chat with us opens automatically.'); }
      } catch (err) {
        msg.className = 'form-msg err';
        msg.textContent = err.message + ' You can also email sales@mitsflix.com.';
      } finally { submit.disabled = false; submit.textContent = label; }
    });
  });
})();
