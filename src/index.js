// mitsflix.com: short links, then the static site.
const LINKS = {
  '/discord': 'https://discord.gg/zFqtpf4XXn',
  '/windows': 'https://github.com/Mitsflix/MitsflixPlayer-Windows/releases/latest/download/MitsflixPlayer-Setup.exe',
  '/android': 'https://github.com/Mitsflix/MitsflixPlayer/releases/latest',
  '/app': 'https://github.com/Mitsflix/MitsflixPlayer/releases/latest',
  '/apk': 'https://github.com/Mitsflix/MitsflixPlayer/releases/latest',
};

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.hostname === 'www.mitsflix.com') { url.hostname = 'mitsflix.com'; return Response.redirect(url.toString(), 301); }
    const to = LINKS[url.pathname.replace(/\/+$/, '').toLowerCase()];
    if (to) return Response.redirect(to, 302);
    return env.ASSETS.fetch(req);
  },
};
