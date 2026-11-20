// mitsflix.com: app downloads served from our own address, short links, then the static site.
const FILES = {
  '/android': ['https://github.com/Mitsflix/MitsflixPlayer/releases/latest/download/MitsflixPlayer.apk', 'MitsflixPlayer.apk', 'application/vnd.android.package-archive'],
  '/windows': ['https://github.com/Mitsflix/MitsflixPlayer-Windows/releases/latest/download/MitsflixPlayer-Setup.exe', 'MitsflixPlayer-Setup.exe', 'application/octet-stream'],
  '/linux': ['https://github.com/Mitsflix/MitsflixPlayer-Windows/releases/latest/download/MitsflixPlayer.deb', 'MitsflixPlayer.deb', 'application/vnd.debian.binary-package'],
  '/linux-appimage': ['https://github.com/Mitsflix/MitsflixPlayer-Windows/releases/latest/download/MitsflixPlayer.AppImage', 'MitsflixPlayer.AppImage', 'application/octet-stream'],
};
FILES['/appimage'] = FILES['/linux-appimage'];
FILES['/apk'] = FILES['/app'] = FILES['/android'];
const LINKS = { '/discord': 'https://discord.gg/zFqtpf4XXn' };

// Subtitle search for the Mitsflix Player apps: passes a handful of OpenSubtitles calls through,
// adding the app's key (the OPENSUB_API_KEY secret) so it never ships inside an app.
// Windows/Linux call /subs/<endpoint>; the Android app (OwnTV core, custom server) calls /subs/api/v1/<endpoint>.
const SUBS = /^\/subs\/(?:api\/v1\/)?(subtitles|login|logout|download|infos\/user)$/;
async function subtitles(req, env, url) {
  const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
  if (url.pathname === '/subs/ready') return json({ ready: !!env.OPENSUB_API_KEY });
  const m = SUBS.exec(url.pathname);
  if (!m || !['GET', 'POST', 'DELETE'].includes(req.method) || !/^(MitsflixPlayer\/|OwnTV$)/.test(req.headers.get('user-agent') || '')) return json({ message: 'Not found' }, 404);
  if (!env.OPENSUB_API_KEY) return json({ message: 'Subtitle search isn\'t switched on yet.' }, 503);
  const host = req.headers.get('x-os-host') === 'vip-api.opensubtitles.com' ? 'vip-api.opensubtitles.com' : 'api.opensubtitles.com';
  const headers = new Headers({ 'Api-Key': env.OPENSUB_API_KEY, 'User-Agent': 'MitsflixPlayer v1.2', Accept: 'application/json' });
  for (const k of ['authorization', 'content-type']) { const v = req.headers.get(k); if (v) headers.set(k, v); }
  const search = req.method === 'GET' && m[1] === 'subtitles';
  const r = await fetch('https://' + host + '/api/v1/' + m[1] + url.search, {
    method: req.method, headers, body: req.method === 'POST' ? await req.text() : undefined,
    cf: search ? { cacheTtl: 6 * 3600, cacheEverything: true } : undefined,
  });
  return new Response(r.body, { status: r.status, headers: { 'content-type': r.headers.get('content-type') || 'application/json', 'cache-control': 'no-store' } });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.hostname === 'www.mitsflix.com') { url.hostname = 'mitsflix.com'; return Response.redirect(url.toString(), 301); }
    if (url.pathname.startsWith('/subs/')) return subtitles(req, env, url);
    const path = url.pathname.replace(/\/+$/, '').toLowerCase();
    if (LINKS[path]) return Response.redirect(LINKS[path], 302);
    const file = FILES[path];
    if (file) {
      // Stream the latest release through mitsflix.com so people only ever see our address.
      const r = await fetch(file[0], { redirect: 'follow', cf: { cacheTtl: 600, cacheEverything: true } });
      if (!r.ok) return new Response('The download isn’t available right now. Please try again in a minute.', { status: 502 });
      const h = new Headers({ 'content-type': file[2], 'content-disposition': `attachment; filename="${file[1]}"`, 'cache-control': 'public, max-age=600' });
      const len = r.headers.get('content-length'); if (len) h.set('content-length', len);
      return new Response(r.body, { status: 200, headers: h });
    }
    return env.ASSETS.fetch(req);
  },
};
