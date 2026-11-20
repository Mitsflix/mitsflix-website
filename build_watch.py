#!/usr/bin/env python3
"""Builds the web player (public/watch/) from Mitsflix Player's own interface.

    python3 build_watch.py <path to a MitsflixPlayer-Windows checkout with node_modules installed>

The same app.js and styles.css the Windows, Mac and Linux apps use, with web/bridge.js standing in
for the desktop app (see that file). Video goes straight from the IPTV server to the viewer.
"""
import os, re, shutil, sys

src = sys.argv[1]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public', 'watch')
shutil.rmtree(out, ignore_errors=True)
os.makedirs(os.path.join(out, 'lib'))
shutil.copytree(os.path.join(src, 'src', 'assets'), os.path.join(out, 'assets'))
for f in ('app.js', 'styles.css'):
    shutil.copy(os.path.join(src, 'src', f), os.path.join(out, f))
for f in ('bridge.js', 'web.css'):
    shutil.copy(os.path.join(src, 'web', f), os.path.join(out, f))
shutil.copy(os.path.join(src, 'node_modules', 'hls.js', 'dist', 'hls.min.js'), os.path.join(out, 'lib', 'hls.min.js'))
shutil.copy(os.path.join(src, 'node_modules', 'mpegts.js', 'dist', 'mpegts.js'), os.path.join(out, 'lib', 'mpegts.js'))

html = open(os.path.join(src, 'src', 'index.html'), encoding='utf-8').read()
html = html.replace('../node_modules/hls.js/dist/hls.min.js', 'lib/hls.min.js').replace('../node_modules/mpegts.js/dist/mpegts.js', 'lib/mpegts.js')
html = html.replace('<script src="app.js"></script>', '<script src="bridge.js"></script>\n  <script src="app.js"></script>')
html = html.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="styles.css">\n  <link rel="stylesheet" href="web.css">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <link rel="icon" href="assets/icon.png">')
html = html.replace('mxfile:', '')
html = html.replace('<title>Mitsflix Player</title>', '<title>Mitsflix Player – Watch in your browser</title>')
assert 'bridge.js' in html and 'lib/hls.min.js' in html, 'index.html changed shape; update build_watch.py'
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
print('Built the web player into', out)
