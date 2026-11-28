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

  // The trial page: a link from the Discord trial button carries a one-time token, so name and email aren't needed.
  const trialForm = document.querySelector('form.trial');
  if (trialForm) {
    const t = (new URLSearchParams(location.search).get('t') || '').replace(/[^a-f0-9]/g, '');
    if (t) {
      trialForm.querySelector('[name=t]').value = t;
      trialForm.querySelectorAll('label.who').forEach((l) => { l.style.display = 'none'; l.querySelector('input').required = false; });
      trialForm.dataset.done = 'Done! Your trial login is on its way to you in Discord.';
    }
  }

  // Sign-up form: an additional line asks which existing account it's for.
  document.querySelectorAll('.plan-pick').forEach((sel) => {
    const form = sel.form, boxes = form.querySelectorAll('.existing-acct'), input = form.querySelector('input[name="existing"]');
    const ref = form.querySelector('input[name="ref"]'), refBox = ref && ref.closest('label');
    const sync = () => {
      const extra = sel.value === 'extra';
      boxes.forEach((b) => { b.hidden = !extra; });
      if (input) input.required = extra;
      if (refBox) refBox.hidden = extra;   // referrals are for new customers
    };
    sel.addEventListener('change', sync);
    if (new URLSearchParams(location.search).get('plan') === 'extra') sel.value = 'extra';
    sync();
  });

  // Forms talk to the Mitsflix team through mitsflix.com/api/… (some networks and blockers stop the
  // workers.dev address); the direct address is only a fallback if that can't be reached.
  const api = async (path, opts) => {
    try { return await fetch('/api/' + path, opts); }
    catch { return fetch('https://mitsflix-tickets.sales-eea.workers.dev/' + path, opts); }
  };

  // The renewal page: the link's code says which line, and the page shows it with its price.
  const renewForm = document.querySelector('form.renew');
  if (renewForm) {
    const c = (new URLSearchParams(location.search).get('c') || '').replace(/[^a-z0-9]/g, '');
    const head = document.querySelector('.renew-line');
    renewForm.querySelector('[name=c]').value = c;
    const stop = (text) => { head.textContent = text; renewForm.querySelectorAll('input, select, button').forEach((el) => { el.disabled = true; }); };
    if (!c) stop('This page needs the renewal link we sent you. Ask us for it on Discord or at sales@mitsflix.com.');
    else api('renew?c=' + c).then((r) => r.json()).then((j) => {
      if (!j.ok) return stop(j.error);
      if (j.linked) return stop(`Line ${j.line} is already linked to you, so your renewal details come by email or Discord. Need a hand? Email sales@mitsflix.com.`);
      head.textContent = `Line ${j.line} ends on ${j.ends}. Renewing is $${j.price} AUD for 12 months.`;
      if (j.name) { const n = renewForm.querySelector('[name=name]'); if (!n.value) n.value = j.name; }
    }).catch(() => stop('We couldn’t load your renewal details. Check your connection and reload the page.'));
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
        const r = await api((form.classList.contains('trial') ? 'trial' : form.classList.contains('renew') ? 'renew' : 'order'), {
          method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(data) });
        const j = await r.json().catch(() => ({}));
        if (!r.ok || !j.ok) throw new Error(j.error || 'Your details didn’t send. Check your connection and try again.');
        const token = form.querySelector('[name=t]')?.value;
        form.reset();
        msg.className = 'form-msg ok';
        msg.textContent = form.dataset.done || 'Sent. We’ll email you soon.';
        if (form.classList.contains('renew')) {
          form.dataset.sent = '1';
          msg.textContent = '';
          if (j.where === 'discord' && j.url) { msg.append('Done! Your renewal chat is open in our Discord: '); const a = document.createElement('a'); a.href = j.url; a.textContent = 'open it here'; msg.append(a, '. Pick how to pay there.'); }
          else msg.textContent = j.text || 'Done! We’ve emailed your payment details. You’ll get renewal reminders by email from now on.';
          return;
        }
        if (form.classList.contains('trial')) {
          if (token) form.querySelector('[name=t]').value = token;
          if (j.auto === false) msg.textContent = j.where === 'email' ? 'Done! We’re setting up your trial now. Your login will be emailed to you shortly.' : 'Done! We’re setting up your trial now. Your login will appear in your Discord chat shortly.';
          form.dataset.sent = '1'; return;
        }
        // Sign-ups with a Discord username get a private chat with us there.
        const join = document.createElement('a');
        join.href = '/discord'; join.textContent = 'Join our Discord';
        if (j.chat === 'opened') msg.textContent = 'Thanks! Your private chat with us is open in our Discord now. We’ll email your payment options too.';
        if (j.chat === 'pending') { msg.textContent = 'Thanks! We’ll email your payment options. '; msg.append(join, ' and your private chat with us opens automatically.'); }
      } catch (err) {
        msg.className = 'form-msg err';
        // A browser's own network errors ("Load failed", "Failed to fetch") mean nothing to people.
        const net = err instanceof TypeError || /load failed|failed to fetch|networkerror/i.test(err.message);
        msg.textContent = (net ? 'Your details didn’t send. Check your connection and try again.' : err.message) + ' You can also email sales@mitsflix.com.';
      } finally { submit.disabled = !!form.dataset.sent; submit.textContent = form.dataset.sent ? (form.classList.contains('renew') ? 'Sent' : 'Trial started') : label; }
    });
  });
})();
