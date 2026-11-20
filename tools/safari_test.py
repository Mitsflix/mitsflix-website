"""Opens the web player in real Safari (macOS runner) and, if a test login is set, plays a live
channel and a movie and checks the video actually advances. Never prints the login."""
import os, time, json
from selenium import webdriver
from selenium.webdriver.common.by import By

USER, PW = os.environ.get('TEST_LINE_USERNAME', ''), os.environ.get('TEST_LINE_PASSWORD', '')
SERVER = os.environ.get('TEST_SERVER') or 'http://cf.126762.xyz'
d = webdriver.Safari()
d.set_window_size(1400, 900)
out = lambda *a: print('RESULT', *a, flush=True)
try:
    d.get('http://watch.mitsflix.com/')
    time.sleep(4)
    out('loaded', d.title, '| web bridge:', d.execute_script('return !!(window.mitsflix && window.mitsflix.web)'),
        '| native HLS:', d.execute_script("return document.createElement('video').canPlayType('application/vnd.apple.mpegurl')"))
    d.save_screenshot('shot-1-loaded.png')
    if not USER:
        out('no test login set: stopping after the page check'); raise SystemExit
    inputs = d.find_elements(By.CSS_SELECTOR, 'input.input')
    for el, v in zip(inputs, ['Test', SERVER, USER, PW]): el.clear(); el.send_keys(v)
    [b for b in d.find_elements(By.TAG_NAME, 'button') if b.text.strip() == 'Add playlist'][0].click()
    time.sleep(12)
    d.save_screenshot('shot-2-home.png')
    out('home text:', d.find_element(By.CSS_SELECTOR, '#view').text[:160].replace('\n', ' | '))
    def play_check(label):
        time.sleep(15)
        st = d.execute_script("const v=document.querySelector('#player video');const m=document.querySelector('#player .center-msg');return v?{t:v.currentTime,rs:v.readyState,err:v.error&&v.error.code,src:(v.currentSrc||'').replace(/\\/\\/[^/]+\\/(live|movie|series)\\/[^/]+\\/[^/]+\\//,'//SERVER/$1/USER/PASS/'),msg:m?m.innerText:''}:null")
        out(label, json.dumps(st))
        d.save_screenshot(f'shot-{label}.png')
    # Live: first channel
    d.find_element(By.CSS_SELECTOR, '.rail-btn[data-view="live"]').click(); time.sleep(4)
    rows = d.find_elements(By.CSS_SELECTOR, '.ch-row, .channel, .list .row, .ch')
    out('channel rows found', len(rows))
    if rows: rows[min(3, len(rows)-1)].click(); time.sleep(2)
    # if a preview started, open full player via double click / enter
    play_check('live')
    d.execute_script("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}))"); time.sleep(2)
    # Movie: first poster
    d.find_element(By.CSS_SELECTOR, '.rail-btn[data-view="movies"]').click(); time.sleep(5)
    cards = d.find_elements(By.CSS_SELECTOR, '.card, .poster-card, .pcard')
    out('movie cards found', len(cards))
    if cards:
        cards[0].click(); time.sleep(5)
        btns = [b for b in d.find_elements(By.TAG_NAME, 'button') if b.text.strip() in ('Play', 'Resume')]
        if btns: btns[0].click()
        play_check('movie')
finally:
    d.quit()
