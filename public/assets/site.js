// Mitsflix site: menu, live guide clock, forms.
(() => {
  const btn = document.querySelector('.menu-btn'), nav = document.querySelector('.nav');
  if (btn && nav) btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
    btn.textContent = open ? 'Close' : 'Menu';
  });

  // Guide header shows the visitor's own time, so the gold "now" line is really now.
  const times = document.querySelectorAll('.guide-times span');
  if (times.length) {
    const start = new Date(); start.setMinutes(start.getMinutes() < 30 ? 0 : 30, 0, 0); start.setTime(start.getTime() - 30 * 60000);
    const fmt = new Intl.DateTimeFormat(undefined, { hour: 'numeric', minute: '2-digit' });
    times.forEach((el, i) => { el.textContent = fmt.format(new Date(start.getTime() + i * 30 * 60000)); });
  }

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
      } catch (err) {
        msg.className = 'form-msg err';
        msg.textContent = err.message + ' You can also email sales@mitsflix.com.';
      } finally { submit.disabled = false; submit.textContent = label; }
    });
  });
})();
