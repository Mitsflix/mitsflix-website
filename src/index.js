// mitsflix.com: app downloads served from our own address, short links, then the static site.
const FILES = {
  '/android': ['https://github.com/Mitsflix/MitsflixPlayer/releases/latest/download/MitsflixPlayer.apk', 'MitsflixPlayer.apk', 'application/vnd.android.package-archive'],
  '/windows': ['https://github.com/Mitsflix/MitsflixPlayer-Windows/releases/latest/download/MitsflixPlayer-Setup.exe', 'MitsflixPlayer-Setup.exe', 'application/octet-stream'],
};
FILES['/apk'] = FILES['/app'] = FILES['/android'];
const LINKS = { '/discord': 'https://discord.gg/zFqtpf4XXn' };

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.hostname === 'www.mitsflix.com') { url.hostname = 'mitsflix.com'; return Response.redirect(url.toString(), 301); }
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
