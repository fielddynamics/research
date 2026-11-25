"""Optional browser tests: pip install playwright; install Chromium if needed.
Local file navigation is blocked in some managed environments, so load the self-contained HTML bytes.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import shutil
p=Path(__file__).parent
with sync_playwright() as pw:
    exe=shutil.which('chromium') or shutil.which('google-chrome')
    b=pw.chromium.launch(executable_path=exe,headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'],timeout=10000)
    page=b.new_page(viewport={'width':1200,'height':900}); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((p/'explorer.html').read_text(),wait_until='domcontentloaded',timeout=10000)
    logs=[]
    def check(label,test):
        assert test,label;logs.append('PASS '+label)
    check('HTML loaded; exact integer Gram and Walsh certificates',page.locator('html').get_attribute('data-verified')=='true')
    check('initial current divergence zero',abs(float(page.locator('#div').inner_text()))<1e-12)
    page.select_option('#mode','0');check('uniform face ledger cancels',float(page.locator('#norm').inner_text())==0)
    page.select_option('#mode','7');check('parity-only cycle',float(page.locator('#pa').inner_text())>0 and float(page.locator('#sq').inner_text())==0 and float(page.locator('#co').inner_text())==0)
    page.select_option('#mode','mix');page.eval_on_selector('#kb',"el=>{el.value='1';el.dispatchEvent(new Event('input'))}");check('equal chambers eliminate complementary and parity cycles',float(page.locator('#co').inner_text())==0 and float(page.locator('#pa').inner_text())==0)
    page.eval_on_selector('#phase',"el=>{el.value='180';el.dispatchEvent(new Event('input'))}");check('opposite phase cancels bright drive',page.locator('#bright').inner_text()=='0.0%')
    page.eval_on_selector('#detune',"el=>{el.value='10';el.dispatchEvent(new Event('input'))}");check('large detuning suppresses E occupation',float(page.locator('#bound').inner_text().strip('%'))<2)
    page.select_option('#coreAxis','4');check('eight simultaneous outer ring ledger contributions',page.locator('#activeRings').inner_text()=='8 / 8')
    page.eval_on_selector('#faceB',"el=>{el.value='-1';el.dispatchEvent(new Event('input'))}");check('opposite coefficients cancel principal ring contribution, not outer rings',float(page.locator('#coreContribution').inner_text())==0 and page.locator('#activeRings').inner_text()=='8 / 8')
    page.eval_on_selector('#faceB',"el=>{el.value='0';el.dispatchEvent(new Event('input'))}");check('zero chamber coefficient leaves four active rings',page.locator('#activeRings').inner_text()=='4 / 8')
    page.eval_on_selector('#faceB',"el=>{el.value='.55';el.dispatchEvent(new Event('input'))}")
    page.click('#reset');check('no JavaScript exceptions',not errors)
    page.screenshot(path=str(p/'explorer_preview.png'),full_page=True,timeout=10000)
    page.set_viewport_size({'width':390,'height':844}); check('mobile viewport no horizontal document overflow',page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
    (p/'browser_verification.txt').write_text('Chromium; self-contained HTML loaded from bytes. Local file navigation restricted in test environment.\n'+'\n'.join(logs)+'\n')
    print('\n'.join(logs));b.close()
