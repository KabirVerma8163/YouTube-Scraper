from playwright.sync_api import sync_playwright
import datetime
import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    # 'Cookie': '__Secure-3PSID=RwgnoDcqUjpBQX1GEsUHKytz-0PkQQRrLe2TAjoRaifFbHyYHiZPBGwwm7z6vWPSfemtHw.; __Secure-3PAPISID=43WsUbnwKUKuajj4/A7hznRX7I9EWN-MyQ; __Secure-3PSIDCC=AIKkIs1Wqe96Or6s2wVsNsiDQ8wKOjg_ecWclXcz1wczn1WwFVBFNTOdu2LHwcER4fOr4Js9Oxqw; PREF=tz=America.Toronto&f6=40000000&f5=20000&f4=4000000&ID=d675d65a2ab79686%3ATM; VISITOR_INFO1_LIVE=3exX4kNbhwk; YSC=mMOQXRriAGM; SID=RwgnoDcqUjpBQX1GEsUHKytz-0PkQQRrLe2TAjoRaifFbHyYSQAYvMqYaO69hS3jibNXmQ.; __Secure-1PSID=RwgnoDcqUjpBQX1GEsUHKytz-0PkQQRrLe2TAjoRaifFbHyYavoTH19OPL7I-vVSjVNmGg.; HSID=AOSZxuC2TrLXTsD0W; SSID=Ac2wjepFAZZUmFSon; APISID=HoBhntvFWCpb7fnV/A1WsrxicX10dN1k9Y; SAPISID=43WsUbnwKUKuajj4/A7hznRX7I9EWN-MyQ; __Secure-1PAPISID=43WsUbnwKUKuajj4/A7hznRX7I9EWN-MyQ; LOGIN_INFO=AFmmF2swRAIgCAS24gSOQyRij6ifxFIMejy1X2ncn8mike0XixZK2jUCIHwNFHeYC58jiZwQ2YU9yBd_s1lJ2Vs7HBMWIlI7mfTp:QUQ3MjNmeHpYb1I2ZEV3M2tFakFJYmd5eE9mVzFILUJUc014RmItd0xaV1pMc1I1aVdtRm5rQWJ3aTN0U0FkLU1TbTdiWmhOanFOYnVqcEtneGFlcjl3bzRaTldYN3lNT29uTjJQdlljRy11RWN3S1FsMmtGX0hlWE42SEFrZEhjNE40QnRvUjdQTFpxdWxhRnVwTG5nYkFjVGJSMmFWTUJB; SIDCC=AIKkIs2ydKr89OVGPrltICYC5qYPhaEkyUbgeSFD5GdQbSVr5xs9P3IZzox6ak2E1Q4rF3aC; __Secure-1PSIDCC=AIKkIs3vfDIuZLRPwTrmtbkDF8T6R5eAAFk_yduNfnsdCLklq7lRvUqpYwfnNqlA7WOCZ1Gtaw',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

# You could make this for two different files just so you can automate how many accounts can do this shit.

## The goal is to get the data from the youtube history page for the last three days and save it to a file.

day_name = datetime.datetime.now() - datetime.timedelta(days=2)
day_name = day_name.strftime("%A")


def get_youtube_data(auth_json):
    with sync_playwright() as p:
        # browser = p.firefox.launch(headless=False, slow_mo=5000)
        browser = p.firefox.launch()
        context = browser.new_context(storage_state=auth_json)
        page = context.new_page()
        page.goto("https://www.youtube.com/feed/history")
        page.set_extra_http_headers(headers)
        page.wait_for_load_state()
        return_array = []

        to_search = ["Today", "Yesterday", day_name]

        section_selector = "ytd-item-section-renderer.style-scope.ytd-section-list-renderer"
        # first_section = page.locator(section_selector)
        all_sections = page.locator(section_selector).all()
        all_sections = all_sections[0:3]
        sections_to_search = []

        for day in to_search:
          for section in all_sections:
            header_selector = "ytd-item-section-header-renderer"
            section_header = section.locator(header_selector)
            section_header_text = section_header.inner_text()

            if section_header_text == day:
              while section.get_by_role("button", name="Next").is_visible():
                section.get_by_role("button", name="Next").click()
              sections_to_search.append(section)
              break

        # write the inner html to a file
        with open("youtube_history.html", "w") as f:
          for section in sections_to_search:
            f.write(section.inner_html())

        browser.close()

    return return_array

get_youtube_data("auth.json")
# pprint.pprint()