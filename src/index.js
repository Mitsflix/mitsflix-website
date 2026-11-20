// mitsflix.com: app downloads served from our own address, short links, then the static site.
const FILES = {
  '/android': ['https://github.com/Mitsflix/MitsflixPlayer/releases/latest/download/MitsflixPlayer.apk', 'MitsflixPlayer.apk', 'application/vnd.android.package-archive'],
  '/windows': ['https://github.com/Mitsflix/MitsflixPlayer-Windows/releases/latest/download/MitsflixPlayer-Setup.exe', 'MitsflixPlayer-Setup.exe', 'application/octet-stream'],
  '/mac': ['https://github.com/Mitsflix/MitsflixPlayer-Windows/releases/latest/download/MitsflixPlayer.dmg', 'MitsflixPlayer.dmg', 'application/x-apple-diskimage'],
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
const WATCH = 'http://watch.mitsflix.com:8080/';

// The web player at mitsflix.com/watch: same site, so the browser says so (and can't fake it for others).
const webPlayer = (req) => req.headers.get('x-mitsflix-web') === '1' && (req.headers.get('sec-fetch-site') === 'same-origin' || /^https?:\/\/(watch\.)?mitsflix\.com(:8080)?$/.test(req.headers.get('origin') || ''));

async function subtitles(req, env, url) {
  const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
  if (url.pathname === '/subs/ready') return json({ ready: !!env.OPENSUB_API_KEY });
  const m = SUBS.exec(url.pathname);
  if (!m || !['GET', 'POST', 'DELETE'].includes(req.method) || !(/^(MitsflixPlayer\/|OwnTV$)/.test(req.headers.get('user-agent') || '') || webPlayer(req))) return json({ message: 'Not found' }, 404);
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
    // The web player lives at http://watch.mitsflix.com:8080. It's deliberately NOT https: browsers won't
    // play the http video streams IPTV servers send from a secure page. Port 8080 because Chrome quietly
    // swaps plain addresses on the normal port for https ones; it leaves other ports alone.
    // (Nothing is typed there but the viewer's own playlist login, which IPTV apps send over http anyway.)
    if (url.hostname === 'watch.mitsflix.com') {
      if (url.protocol === 'https:' || url.port !== '8080') return Response.redirect(WATCH + url.pathname.slice(1) + url.search, 302);
      if (url.pathname.startsWith('/subs/')) return subtitles(req, env, url);
      const inner = new URL(req.url); inner.protocol = 'https:'; inner.hostname = 'mitsflix.com'; inner.port = ''; inner.pathname = '/watch' + (url.pathname === '/' ? '/' : url.pathname);
      return env.ASSETS.fetch(new Request(inner.toString(), req));
    }
    if (/^\/watch(\/|$)/.test(url.pathname)) return Response.redirect(WATCH, 302);
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
