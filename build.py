#!/usr/bin/env python3
"""Builds the static pages in public/ from the content below. Run: python3 build.py"""
import pathlib

SITE = 'https://mitsflix.com'
PAGES = [('index', 'Home'), ('download', 'Download'), ('guides', 'Setup guides'), ('pricing', 'Pricing'), ('resellers', 'Resellers'), ('support', 'Support')]
FONTS = 'https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Figtree:wght@400;600;700&display=swap'


def page(slug, title, desc, body):
    nav = '\n'.join(f'<a href="/{"" if s == "index" else s}"{" aria-current=page" if s == slug else ""}>{n}</a>' for s, n in PAGES[1:])
    full_title = 'Mitsflix | One service. Stream all.' if slug == 'index' else f'{title} | Mitsflix'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#000000">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/og.jpg">
<meta property="og:url" content="{SITE}/{'' if slug == 'index' else slug}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
  <a class="brand" href="/" aria-label="Mitsflix home"><img src="/assets/wordmark-400.png" alt="Mitsflix" width="118" height="53"></a>
  <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav">{nav}<a class="btn solid" href="/pricing#sign-up" style="min-height:40px;padding:0 18px">Sign up</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
  <img src="/assets/wordmark-400.png" alt="Mitsflix" width="140" height="62">
  <nav>{nav}<a href="/discord">Discord</a><a href="mailto:sales@mitsflix.com">sales@mitsflix.com</a></nav>
  <p style="margin:0">© Mitsflix. One service. Stream all.</p>
</div></footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''


def app_html():
    return '''<figure class="tv">
  <img class="shot" src="/assets/app-home.jpg" width="1600" height="644" alt="The Mitsflix Player home screen, with a featured movie, Play and Trailer buttons, and a Keep watching row">
  <div class="stand"></div>
  <figcaption>Mitsflix Player, our free app</figcaption>
</figure>'''


HOME = f'''
<section class="hero"><div class="wrap">
  <div>
    <h1>One service. Stream all.</h1>
    <p class="lead">Live TV from around the world, sport and PPV events, and a huge library of movies and series. Download to watch offline, record live TV, and use one login on the devices you already own.</p>
    <p class="price-line">$100 AUD for a whole year</p>
    <div class="btns"><a class="btn solid" href="/pricing#sign-up">Sign up</a><a class="btn" href="/download">Get the app</a></div>
  </div>
  {app_html()}
</div></section>

<section><div class="wrap split">
  <div><h2>What you get</h2><p class="muted">Everything is included in the one price. No add-on packs, no lock-in contract.</p></div>
  <ul class="ticks">
    <li><b>Live channels from around the world</b><span>News, entertainment, kids and local channels from many countries.</span></li>
    <li><b>Sport and PPV events</b><span>Football, fights, racing and more. Our sports guide on Discord shows what’s on in your time zone.</span></li>
    <li><b>Movies and series on demand</b><span>New titles added every day, with posters, plots and trailers.</span></li>
    <li><b>Download movies and shows</b><span>Save them to your device and watch offline, on a plane, at work camp or anywhere without internet.</span></li>
    <li><b>Record live TV</b><span>Record a match or show to watch later, or set a time and it records by itself.</span></li>
    <li><b>Our own free app</b><span>Mitsflix Player for Fire TV, Google TV, Android, Windows, Mac and Linux, with Continue Watching and subtitles for movies and shows.</span></li>
    <li><b>Real people helping you</b><span>Private support tickets on Discord, or email us any time.</span></li>
  </ul>
</div></section>

<section><div class="wrap">
  <h2>Up and running in minutes</h2>
  <ol class="steps">
    <li><b>Sign up</b><span>Fill in the short form. We email you payment options.</span></li>
    <li><b>Get your login</b><span>Once paid, your username and password arrive by email.</span></li>
    <li><b>Install and watch</b><span>Install Mitsflix Player with Downloader code 6284643, add your login and press play.</span></li>
  </ol>
  <div class="btns" style="margin-top:36px"><a class="btn solid" href="/pricing#sign-up">Sign up</a><a class="btn" href="/guides">See the setup guides</a></div>
</div></section>

<section><div class="wrap split">
  <div><h2>Works on</h2><p class="muted">One screen at a time on any of these.</p></div>
  <ul class="ticks">
    <li><b>Fire TV and Google TV</b><span>Fire TV Stick 4K Max or Google TV Streamer 4K recommended.</span></li>
    <li><b>Android TV boxes, phones and tablets</b><span>Mitsflix Player, free.</span></li>
    <li><b>iPhone, iPad and Apple TV</b><span>Use TiviMax from the App Store.</span></li>
    <li><b>Smart TVs and computers</b><span>Any IPTV player that supports Xtream Codes.</span></li>
  </ul>
</div></section>
'''

DOWNLOAD = '''
<div class="wrap page-head"><h1>Download</h1><p>Mitsflix Player is free, has no ads and updates itself. On Fire TV, Google TV, Android, Windows, Mac and Linux you can download movies and shows to watch offline, record live TV and add subtitles.</p></div>
<section style="padding-top:0"><div class="wrap">
  <div class="rows">
    <div class="row"><h3>Fire TV &amp; Google TV</h3><p>Install the <b>Downloader</b> app, open it and enter this code. It always installs the latest version. <a href="/guides#fire-tv">Step-by-step guide</a></p><div class="code">6284643</div></div>
    <div class="row"><h3>Android phone or tablet</h3><p>Download the APK file and open it to install. <a href="/guides#android">Step-by-step guide</a></p><a class="btn solid" href="/android">Download APK</a></div>
    <div class="row"><h3>Windows <span class="tag">Beta</span></h3><p>Mitsflix Player for Windows 10 and 11, with offline downloads and live TV recording. If Windows shows a blue warning, choose <b>More info</b>, then <b>Run anyway</b>.</p><a class="btn" href="/windows">Download for Windows</a></div>
    <div class="row"><h3>Mac <span class="tag">Beta</span></h3><p>Mitsflix Player for Macs with Apple silicon or Intel (macOS 11 or newer). Open the download and drag Mitsflix Player into Applications. The first time, macOS asks you to approve it. <a href="/guides#computer">Step-by-step guide</a></p><a class="btn" href="/mac">Download for Mac</a></div>
    <div class="row"><h3>Linux <span class="tag">Beta</span></h3><p>The same player for Linux. On Ubuntu, Debian or Mint, download the .deb and open it. On other systems use the <a href="/linux-appimage">AppImage</a>: make it executable, then open it.</p><a class="btn" href="/linux">Download for Linux</a></div>
    <div class="row"><h3>Web browser <span class="tag">Beta</span></h3><p>Watch on any computer without installing anything: open the web player and sign in with your login. Best in Chrome, Edge or Firefox. Downloads and recording need the app.</p><a class="btn" href="/watch/">Open web player</a></div>
    <div class="row"><h3>Chromebook &amp; Steam Deck</h3><p>Chromebooks with an Intel or AMD processor run the Linux version, and so does the Steam Deck. <a href="/guides#chromebook">Chromebook guide</a> · <a href="/guides#steam-deck">Steam Deck guide</a></p></div>
    <div class="row"><h3>iPhone, iPad &amp; Apple TV</h3><p>Install <b>TiviMax Premium</b> from the App Store and add your Mitsflix login. <a href="/guides#apple">Step-by-step guide</a></p><a class="btn" href="https://apps.apple.com/au/app/id1632953327">Open App Store</a></div>
  </div>
  <p class="muted" style="margin-top:28px">Fire TV and Android need Android 8 or newer. Fire TV Sticks with <b>Select</b> or <b>HD</b> in the name aren’t powerful enough.</p>
</div></section>
'''

STEP4 = '''<ol class="do">
  <li>Open the app and choose <b>Add playlist</b>, then <b>Xtream Codes</b>.</li>
  <li><b>Server</b>, <b>Username</b> and <b>Password:</b> copy them exactly from the welcome email we sent you.</li>
  <li>Save. Live TV, movies and series load by themselves.</li>
</ol>'''

GUIDES = f'''
<div class="wrap page-head"><h1>Setup guides</h1><p>Pick your device. Each guide takes about five minutes.</p>
<ul class="guide-nav"><li><a href="#fire-tv">Fire TV &amp; Google TV</a></li><li><a href="#android">Android phone</a></li><li><a href="#apple">iPhone &amp; Apple TV</a></li><li><a href="#computer">Windows, Mac &amp; Linux</a></li><li><a href="#chromebook">Chromebook</a></li><li><a href="#steam-deck">Steam Deck</a></li><li><a href="#fixes">Buffering fixes</a></li></ul></div>

<div class="wrap">
<article class="howto" id="fire-tv"><h2>Fire TV, Google TV &amp; Android TV</h2>
  <h3>Install Downloader</h3>
  <ol class="do"><li>Go to <b>Search</b>. On Google TV, open the <b>Play Store</b>.</li><li>Type <b>Downloader</b>.</li><li>Install the orange <b>Downloader</b> app.</li></ol>
  <h3>Allow unknown apps</h3>
  <ol class="do"><li><b>Fire TV:</b> Settings, My Fire TV, Developer Options, Install Unknown Apps, then turn <b>Downloader</b> on.</li>
  <li><b>Google TV:</b> Settings, Apps, Security &amp; restrictions, Unknown sources, then turn <b>Downloader</b> on.</li></ol>
  <p class="note">No Developer Options on your Fire TV? Go to Settings, My Fire TV, About, click <b>Fire TV Stick</b> seven times, then go back.</p>
  <h3>Install Mitsflix Player</h3>
  <ol class="do"><li>Open <b>Downloader</b>.</li><li>Enter code <b>6284643</b> and press <b>Go</b>.</li><li>Press <b>Install</b>, then <b>Open</b>.</li></ol>
  <h3>Add your login</h3>{STEP4}
</article>

<article class="howto" id="android"><h2>Android phone or tablet</h2>
  <ol class="do"><li>On your phone, <a href="/android">download the Mitsflix Player APK</a>.</li><li>Open the file. If asked, allow your browser to install unknown apps, then press <b>Install</b>.</li></ol>
  <h3>Add your login</h3>{STEP4}
</article>

<article class="howto" id="apple"><h2>iPhone, iPad &amp; Apple TV</h2>
  <ol class="do"><li>Install <b><a href="https://apps.apple.com/au/app/id1632953327">TiviMax Premium</a></b> from the App Store.</li>
  <li>Add a playlist using <b>Xtream Codes</b>.</li><li><b>Server</b>, <b>Username</b> and <b>Password:</b> copy them exactly from the welcome email we sent you.</li></ol>
</article>

<article class="howto" id="computer"><h2>Windows, Mac &amp; Linux</h2>
  <h3>Windows 10 or 11</h3>
  <ol class="do"><li><a href="/windows">Download Mitsflix Player for Windows</a> and open the file.</li><li>If a blue “Windows protected your PC” box appears, choose <b>More info</b>, then <b>Run anyway</b>.</li><li>Follow the installer. Mitsflix Player opens when it’s done.</li></ol>
  <h3>Mac</h3>
  <ol class="do"><li><a href="/mac">Download Mitsflix Player for Mac</a> and open the file.</li><li>Drag <b>Mitsflix Player</b> into the <b>Applications</b> folder.</li><li>Open Mitsflix Player from Applications. macOS says it can’t check the app: choose <b>Done</b>.</li><li>Open <b>System Settings</b>, then <b>Privacy &amp; Security</b>. Scroll down and choose <b>Open Anyway</b> next to Mitsflix Player, then confirm.</li></ol>
  <p class="note">You only need to approve it once. On older macOS versions, right-click the app, choose <b>Open</b>, then <b>Open</b> again.</p>
  <h3>Linux</h3>
  <ol class="do"><li>On Ubuntu, Debian or Mint, <a href="/linux">download the .deb</a> and open it to install.</li><li>On other systems, <a href="/linux-appimage">download the AppImage</a>, make it executable (right-click, Properties, Permissions), then open it.</li></ol>
  <h3>Add your login</h3>{STEP4}
</article>

<article class="howto" id="chromebook"><h2>Chromebook</h2>
  <p>This works on Chromebooks with an Intel or AMD processor. It uses the Chromebook’s built-in Linux.</p>
  <ol class="do"><li>Open <b>Settings</b>, then <b>About ChromeOS</b>, <b>Developers</b>, and turn on <b>Linux development environment</b>. Follow the steps (the defaults are fine).</li>
  <li><a href="/linux">Download the .deb file</a>.</li><li>Open the <b>Files</b> app, double-click the file and choose <b>Install</b>.</li><li>Open <b>Mitsflix Player</b> from the launcher. It’s in the <b>Linux apps</b> folder.</li></ol>
  <h3>Add your login</h3>{STEP4}
</article>

<article class="howto" id="steam-deck"><h2>Steam Deck</h2>
  <ol class="do"><li>Press the <b>Steam</b> button, then <b>Power</b>, then <b>Switch to Desktop</b>.</li><li>Open the web browser and <a href="/linux-appimage">download the AppImage</a>.</li>
  <li>In the <b>Downloads</b> folder, right-click the file, choose <b>Properties</b>, then <b>Permissions</b>, and tick <b>Is executable</b>.</li>
  <li>To use it in Gaming Mode: open <b>Steam</b>, then <b>Games</b>, <b>Add a Non-Steam Game</b>, choose the file and press <b>Add</b>.</li>
  <li>Go back to Gaming Mode. Mitsflix Player is in your library under <b>Non-Steam</b>.</li></ol>
  <h3>Add your login</h3>{STEP4}
</article>

<article class="howto" id="fixes"><h2>Buffering or not loading</h2>
  <ol class="do">
    <li><b>Try another server address.</b> Your welcome email has backups, or ask us for one.</li>
    <li><b>Restart</b> the app, your device and your modem.</li>
    <li><b>Use Cloudflare DNS on your modem:</b> primary <code>1.1.1.1</code>, secondary <code>1.0.0.1</code>. Turning off IPv6 in the modem can help too.</li>
    <li><b>Try a VPN</b> connected to a US or European server, not one near Australia. Ask us for the VPN server address to use with it.</li>
  </ol>
  <p>Still stuck? <a href="/support">Get help</a>.</p>
</article>
</div>
'''

PRICING = '''
<div class="wrap page-head"><h1>Pricing</h1><p>One plan with everything in it.</p></div>
<section style="padding-top:0"><div class="wrap">
  <div class="ticket">
    <div class="main">
      <h2 style="margin-bottom:.2em">12 months of Mitsflix</h2>
      <p class="muted">Admit one screen at a time.</p>
      <ul class="ticks" style="margin-top:20px">
        <li><b>Live channels from around the world</b></li>
        <li><b>Sport and PPV events</b></li>
        <li><b>Movies and series on demand</b></li>
        <li><b>Free Mitsflix Player app</b></li>
        <li><b>Download to watch offline</b></li>
        <li><b>Record live TV</b></li>
        <li><b>Support on Discord and email</b></li>
      </ul>
    </div>
    <div class="stub">
      <div class="amount"><sup>$</sup>100</div>
      <div class="per">AUD for 12 months</div>
      <a class="btn solid" href="#sign-up">Sign up</a>
    </div>
  </div>
</div></section>

<section id="ways-to-pay" style="padding-top:8px"><div class="wrap">
  <h2>Ways to pay</h2>
  <p class="muted">Pick whichever suits you when you sign up. There’s no subscription or automatic charge: we remind you before your 12 months end, and renewing keeps the same login.</p>
  <dl class="pay">
    <div><dt>Card, Apple Pay or Google Pay</dt><dd>Pay through a secure checkout page. Your login is sent automatically as soon as payment goes through.</dd></div>
    <div><dt>Crypto (USDT)</dt><dd>USDT on the TRON network. We give you the exact amount to send, and your login is sent automatically once it arrives.</dd></div>
    <div><dt>Wise</dt><dd>Pay from your Wise account or with a Wise payment link. Your login follows once we see the payment.</dd></div>
    <div><dt>PayID</dt><dd>For Australian bank accounts. Use your Discord username or email as the reference, and your login follows once it arrives.</dd></div>
  </dl>
</div></section>

<section id="sign-up"><div class="wrap split">
  <div>
    <h2>Sign up</h2>
    <p>Tell us a little about how you’ll watch. We’ll email you payment options, and your login arrives as soon as payment comes through.</p>
    <p class="muted">Prefer Discord? Use the Sign up button in <a href="/discord">our server</a>.</p>
    <p class="muted">Not sure yet? <a href="/trial">Try Mitsflix free for a day</a>.</p>
  </div>
  <form class="order" data-done="Thanks! We’ve got your details and will email you payment options shortly.">
    <input type="hidden" name="kind" value="signup">
    <label>Name<input name="name" autocomplete="name" required maxlength="100"></label>
    <label>Email<input name="email" type="email" autocomplete="email" required maxlength="200"></label>
    <label>Phone or WhatsApp <small>Optional</small><input name="phone" autocomplete="tel" maxlength="40"></label>
    <label>Discord username <small>Optional. We’ll open a private chat with you in our Discord and give you your member role</small><input name="discord" maxlength="40" autocapitalize="none" placeholder="e.g. alex_1234"></label>
    <label>Referral code <small>Optional. Your friend’s Discord username. You both get 1 month free</small><input name="ref" maxlength="32" autocapitalize="none" autocomplete="off" spellcheck="false" placeholder="e.g. alex_1234"></label>
    <label class="full">What will you watch on?
      <select name="device" required><option value="">Choose a device</option><option>Fire TV Stick</option><option>Google TV / Android TV</option><option>Android phone or tablet</option><option>iPhone, iPad or Apple TV</option><option>Smart TV</option><option>Computer</option><option>Not sure yet</option></select></label>
    <label class="full">Channels
      <select name="bouquet"><option value="en_xxx">English channels + adult</option><option value="en">English channels, no adult</option><option value="ww_xxx">Worldwide channels + adult</option><option value="ww">Worldwide channels, no adult</option></select></label>
    <label class="full">Anything else we should know? <small>Optional</small><textarea name="prefs" maxlength="800"></textarea></label>
    <label class="full">How did you hear about us? <small>Optional</small><input name="found" maxlength="200"></label>
    <label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
    <div class="full"><button class="btn solid" type="submit">Send my details</button></div>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form>
</div></section>

<section><div class="wrap">
  <h2>Selling to friends or customers?</h2>
  <p>Mitsflix has a reseller program with your own panel. <a href="/resellers">See how it works</a>.</p>
</div></section>
'''

RESELLERS = '''
<div class="wrap page-head"><h1>Become a Mitsflix reseller</h1><p>Sell Mitsflix to your own customers, set your own prices and manage every account yourself.</p>
<div class="btns"><a class="btn solid" href="#apply">Apply now</a><a class="btn" href="/discord">Ask us on Discord</a></div></div>

<section style="padding-top:24px"><div class="wrap split">
  <div><h2>What you get</h2><p class="muted">Everything you need to run your own little streaming business.</p></div>
  <ul class="ticks">
    <li><b>Your own reseller panel</b><span>Create trials, new accounts and renewals yourself, any time of day, without waiting on us.</span></li>
    <li><b>Credits you buy upfront</b><span>Load credits and use them as you sell. You set what your customers pay.</span></li>
    <li><b>Private server addresses</b><span>Addresses just for resellers, so your customers get a smoother connection.</span></li>
    <li><b>A free app for your customers</b><span>Mitsflix Player installs with one Downloader code and updates itself. Setup guides are ready to share.</span></li>
    <li><b>Updates first</b><span>Service news, outages and fixes as they happen, so you can keep your customers informed.</span></li>
    <li><b>Help when you need it</b><span>A direct line to us on Discord or email for anything your customers get stuck on.</span></li>
  </ul>
</div></section>

<section id="packages"><div class="wrap">
  <h2>Credit packages</h2>
  <p class="muted">12 credits make one 1-year line. New resellers start with at least 120 credits.</p>
  <div class="table-wrap"><table class="packages">
    <thead><tr><th scope="col">Package</th><th scope="col">Credits</th><th scope="col">1-year lines</th><th scope="col">Per line</th><th scope="col">Price (AUD)</th></tr></thead>
    <tbody>
      <tr><th scope="row">Top-up <small>existing resellers</small></th><td>60</td><td>5</td><td>$60</td><td>$300</td></tr>
      <tr class="start"><th scope="row">Standard <small>minimum to start</small></th><td>120</td><td>10</td><td>$60</td><td>$600</td></tr>
      <tr><th scope="row">Bulk</th><td>240</td><td>20</td><td>$50</td><td>$1,000</td></tr>
      <tr><th scope="row">Pro</th><td>480</td><td>40</td><td>$45</td><td>$1,800</td></tr>
      <tr><th scope="row">Elite</th><td>960</td><td>80</td><td>$40</td><td>$3,200</td></tr>
    </tbody>
  </table></div>
  <p class="muted">Pay by card, Apple Pay, Google Pay, crypto, Wise or PayID.</p>
</div></section>

<section><div class="wrap">
  <h2>How it works</h2>
  <ol class="steps">
    <li><b>Apply</b><span>Fill in the form below. It takes a minute.</span></li>
    <li><b>Get your panel</b><span>Choose your package, pay, and we set up your panel login.</span></li>
    <li><b>Start selling</b><span>Load credits, create accounts for your customers and send them the setup guide.</span></li>
  </ol>
</div></section>

<section id="apply"><div class="wrap split">
  <div>
    <h2>Apply</h2>
    <p>Tell us a bit about yourself and we’ll be in touch by email with next steps.</p>
    <p class="muted">Questions first? Email <a href="mailto:sales@mitsflix.com">sales@mitsflix.com</a> or ask on <a href="/discord">Discord</a>.</p>
  </div>
  <form class="order" data-done="Thanks! We’ll email you next steps.">
    <input type="hidden" name="kind" value="reseller">
    <label>Name<input name="name" autocomplete="name" required maxlength="100"></label>
    <label>Email<input name="email" type="email" autocomplete="email" required maxlength="200"></label>
    <label>Where are you based?<input name="where" required maxlength="100"></label>
    <label>How many customers do you expect?<input name="size" required maxlength="40" placeholder="e.g. 5, 20, 50+"></label>
    <label class="full">Have you resold IPTV before? <small>Optional</small><textarea name="exp" maxlength="800"></textarea></label>
    <label>Phone or WhatsApp <small>Optional</small><input name="phone" autocomplete="tel" maxlength="40"></label>
    <label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
    <div class="full"><button class="btn solid" type="submit">Apply to resell</button></div>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form>
</div></section>

<section><div class="wrap">
  <h2>Questions</h2>
  <details><summary>How much does it cost?</summary><p>Reseller pricing depends on how many credits you buy. We send the current price list when you apply.</p></details>
  <details><summary>How do I set my prices?</summary><p>That’s up to you. You buy credits from us and charge your customers whatever you like.</p></details>
  <details><summary>Can I offer free trials?</summary><p>Yes. Your panel can create short trial accounts so customers can test before they buy.</p></details>
  <details><summary>How many screens does each account get?</summary><p>Each account plays on one screen at a time.</p></details>
  <details><summary>What do my customers use to watch?</summary><p>Mitsflix Player on Fire TV, Google TV, Android and Windows, TiviMax on Apple devices, or any app that supports Xtream Codes. Point them to our <a href="/guides">setup guides</a>.</p></details>
</div></section>
'''

SUPPORT = '''
<div class="wrap page-head"><h1>Support</h1><p>Most questions are answered in the <a href="/guides">setup guides</a>. If not, we’re here.</p></div>
<section style="padding-top:0"><div class="wrap">
  <div class="contact">
    <div><h3>Discord</h3><p>The fastest way to reach us. Open a private ticket for account help, report a channel that isn’t working, request a movie or show, and see live service updates.</p><a class="btn solid" href="/discord">Join our Discord</a></div>
    <div><h3>Email</h3><p>Prefer email? Write to us and include your Mitsflix username if you have one.</p><a class="btn" href="mailto:sales@mitsflix.com">sales@mitsflix.com</a></div>
  </div>
</div></section>
<section><div class="wrap">
  <h2>Questions</h2>
  <details><summary>How many screens can I watch on?</summary><p>One at a time. You can install the app on as many devices as you like, but only one can play at once.</p></details>
  <details><summary>Which device should I buy?</summary><p>A Google TV Streamer 4K or a Fire TV Stick 4K Max. Avoid Fire TV Sticks with Select or HD in the name, they aren’t powerful enough.</p></details>
  <details><summary>How do I pay?</summary><p>After you sign up we email you the payment options. Your login is sent as soon as payment comes through.</p></details>
  <details><summary>A channel isn’t working. What do I do?</summary><p>First try one of the backup server addresses from your welcome email. If it still won’t play, report it in our Discord and we’ll look into it.</p></details>
  <details><summary>It keeps buffering.</summary><p>Follow the <a href="/guides#fixes">buffering fixes</a>. Switching to a backup server address or setting Cloudflare DNS on your modem fixes most cases.</p></details>
  <details><summary>Can I use my own IPTV app?</summary><p>Yes. Any app that supports Xtream Codes works. Use the server, username and password from your welcome email.</p></details>
  <details><summary>Can I ask for a movie or show to be added?</summary><p>Yes. Use the Make a request channel in our Discord.</p></details>
</div></section>
'''

RENEW = '''
<div class="wrap page-head"><h1>Renew your Mitsflix</h1><p class="renew-line">Checking your renewal link…</p></div>

<section style="padding-top:24px"><div class="wrap split">
  <div>
    <h2>Keep watching</h2>
    <p>Add your email, and your Discord username if you use Discord, then choose how to pay. Your login and app set-up stay exactly the same.</p>
    <p class="muted">Once your details are added, we’ll send your renewal reminders automatically. Card and crypto payments renew your line straight away.</p>
  </div>
  <form class="order renew" data-done="Done! Check your email for your payment details.">
    <input type="hidden" name="c" value="">
    <label>Name<input name="name" autocomplete="name" required maxlength="80"></label>
    <label>Email<input name="email" type="email" autocomplete="email" required maxlength="200"></label>
    <label class="full">Discord username <small>Optional. If you add it, your renewal opens in a private chat in our Discord</small><input name="discord" maxlength="40" autocapitalize="none" placeholder="e.g. alex_1234"></label>
    <label class="full">How would you like to pay?
      <select name="method"><option value="kofi">Card, Apple Pay or Google Pay</option><option value="crypto">Crypto (USDT)</option><option value="wise">Wise</option><option value="payid">PayID (Australia only)</option></select></label>
    <label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
    <div class="full"><button class="btn solid" type="submit">Renew my line</button></div>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form>
</div></section>
'''

TRIAL = '''
<div class="wrap page-head"><h1>Try Mitsflix free for a day</h1><p>Choose your channels and we’ll send you a login for 24 hours. No payment needed.</p></div>

<section style="padding-top:24px"><div class="wrap split">
  <div>
    <h2>How it works</h2>
    <p>Start your trial below. Your login arrives by email, or in Discord if you came from our server. Set it up with our free <a href="/download">Mitsflix Player</a> app and watch for 24 hours.</p>
    <p class="muted">To keep trials fair, there’s one per person, and we check the connection a trial is started from. Please turn off any VPN while you start it. We give out a limited number of trials each day.</p>
  </div>
  <form class="order trial" data-done="Done! Check your email for your trial login.">
    <input type="hidden" name="t" value="">
    <label class="who">Name<input name="name" autocomplete="name" required maxlength="100"></label>
    <label class="who">Email<input name="email" type="email" autocomplete="email" required maxlength="200"></label>
    <label class="full">Channels
      <select name="bouquet"><option value="en_xxx">English channels + adult</option><option value="en">English channels, no adult</option><option value="ww_xxx">Worldwide channels + adult</option><option value="ww">Worldwide channels, no adult</option></select></label>
    <label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
    <div class="full"><button class="btn solid" type="submit">Start my free trial</button></div>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form>
</div></section>
'''

CONTENT = {
    'index': ('Home', 'Live TV, sport, movies and series in one service. $100 AUD a year, with our free Mitsflix Player app.', HOME),
    'download': ('Download', 'Download Mitsflix Player for Fire TV, Google TV, Android, Windows, Mac and Linux. Downloader code 6284643.', DOWNLOAD),
    'guides': ('Setup guides', 'Step-by-step setup for Fire TV, Google TV, Android, Apple, Windows, Mac, Linux, Chromebook and Steam Deck, plus buffering fixes.', GUIDES),
    'pricing': ('Pricing', 'Mitsflix is $100 AUD for 12 months. Sign up in a minute.', PRICING),
    'resellers': ('Resellers', 'Sell Mitsflix with your own reseller panel. Create and renew accounts yourself and set your own prices.', RESELLERS),
    'renew': ('Renew', 'Renew your Mitsflix line. Your login and set-up stay the same.', RENEW),
    'trial': ('Free trial', 'Try Mitsflix free for 24 hours. Choose your channels and get a login straight away.', TRIAL),
    'support': ('Support', 'Get help with Mitsflix on Discord or by email.', SUPPORT),
}

out = pathlib.Path(__file__).parent / 'public'
for slug, (title, desc, body) in CONTENT.items():
    (out / f'{slug}.html').write_text(page(slug, title, desc, body))
(out / '404.html').write_text(page('404', 'Page not found', 'Page not found.', '<div class="wrap page-head"><h1>Page not found</h1><p>That page doesn’t exist. Try the <a href="/">home page</a>.</p></div>'))
print('built', len(CONTENT) + 1, 'pages')
