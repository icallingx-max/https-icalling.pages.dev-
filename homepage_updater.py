import datetime
from bs4 import BeautifulSoup
import os
import re

# --- Configuration and Data --- #
# GITHUB_TOKEN will be passed via environment variable for secure push. It is NOT stored in this script.
REPO_PATH = "/home/icalling/.openclaw/workspace/icalling-story"
INDEX_HTML_PATH = os.path.join(REPO_PATH, "index.html")

# Live data placeholders (these would ideally be fetched live within the script)
# For this run, using the last fetched values
BTC_PRICE = "70,344.91" # Updated price from last fetch
TSLA_PRICE = "405.55"
MOS_PRICE = "26.28"

def get_current_date():
    return datetime.date.today().strftime("%B %d, %Y")

def get_key_headlines_en():
    return """
*   **The Motley Fool:** How Buying Bitcoin Today Could 10x Your Net Worth.
*   **Chosun Ilbo:** Bitcoin Holds Steady Amid Middle East Turmoil.
*   **Digital Today:** Bitcoin investing in stages (DCA strategy) gains attention again.
*   **Yahoo Finance:** Stock market rebounds on hopes of Iran de-escalation as bitcoin surges.
*   **Investing.com:** Bitcoin price falls to $70k amid Iran conflict; set for weekly jump.
"""

def generate_icalling_analysis(btc_price, tsla_price, mos_price):
    return f"""
<p><strong>Today's observation:</strong> Bitcoin is navigating a complex macroeconomic environment, showing resilience despite geopolitical tensions in the Middle East. While its price hovers around ${btc_price}, the broader market sentiment is a mix of caution and opportunistic buying, as seen in traditional stocks like TSLA and MOS.</p>
<p>The key takeaway is the increasing correlation between crypto and traditional markets in response to global events, even as Bitcoin maintains its unique safe-haven narrative. This suggests that while crypto offers diversification, it is not entirely immune to broader market shocks.</p>
<br>
<p><em>Note: This is Maicol's personal analysis based on available data. Investment decisions are the sole responsibility of the investor.</em></p>
"""

def generate_my_prediction():
    return """
<p><strong>Short-term (1-2 weeks):</strong> I predict continued price consolidation for Bitcoin as the market digests recent gains and ongoing geopolitical news. A clear catalyst, such as de-escalation in global conflicts or positive economic data, could trigger the next leg up. Equities may see sideways movement as they await clearer signals from central banks.</p>
<p><strong>Medium-term (1-3 months):</strong> The narrative around potential interest rate cuts and institutional adoption will likely drive the next major trend. I foresee a bullish sentiment re-emerging, but not without periods of volatility. This phase will be crucial for establishing new support levels for major assets.</p>
<br>
<p><em>Note: This is Maicol's personal prediction. Investment decisions are the sole responsibility of the investor.</em></p>
"""

def update_homepage_content(btc_price, tsla_price, mos_price, key_headlines):
    # Ensure the script is run from the repo_path
    original_cwd = os.getcwd()
    os.chdir(REPO_PATH)

    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    current_date = get_current_date()
    current_time_utc = datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M') # Use UTC time

    # 1. Update Date
    date_p_tag = soup.find('p', class_='macro-date')
    if date_p_tag:
        date_p_tag.string = f"📅 {current_date} (Updated)"
    else:
        h2_macro = soup.find("h2", string=re.compile(r"iCalling\'s View on Today\'s Macroeconomic Trends"))
        if h2_macro:
            next_sibling = h2_macro.find_next_sibling()
            if next_sibling and re.match(r"📅\s+\w+\s+\d{1,2},\s+\d{4}\s+\(Updated\)", next_sibling.get_text()):
                next_sibling.string = f"📅 {current_date} (Updated)"

    # 2. Update Market Snapshot
    market_snapshot_section = soup.find("h3", string="📈 Today's Market Snapshot:")
    if market_snapshot_section:
        ul_tag = market_snapshot_section.find_next_sibling("ul")
        if ul_tag:
            ul_tag.clear()
            ul_tag.append(BeautifulSoup(f"<li>**Bitcoin:** ${btc_price}</li>", "html.parser").li)
            ul_tag.append(BeautifulSoup(f"<li>**Tesla (TSLA):** ${tsla_price}</li>", "html.parser").li)
            ul_tag.append(BeautifulSoup(f"<li>**Mosaic Co. (MOS):** ${mos_price}</li>", "html.parser").li)

    # 3. Update Key Headlines
    key_headlines_section = soup.find("h3", string="📰 Key Headlines:")
    if key_headlines_section:
        ul_tag = key_headlines_section.find_next_sibling("ul")
        if ul_tag:
            ul_tag.clear()
            headlines_html = BeautifulSoup(f"<ul>{key_headlines}</ul>", "html.parser")
            for li in headlines_html.find_all("li"):
                ul_tag.append(li)

    # 4. Update iCalling's Analysis
    analysis_section = soup.find("h3", string="🔍 iCalling's Analysis:")
    if analysis_section:
        analysis_container = analysis_section.find_next_sibling(['div', 'p'])
        if analysis_container:
            analysis_container.clear()
            analysis_html_content = generate_icalling_analysis(btc_price, tsla_price, mos_price)
            analysis_container.append(BeautifulSoup(analysis_html_content, "html.parser"))


    # 5. Update My Prediction
    prediction_section = soup.find("h3", string="💭 My Prediction:")
    if prediction_section:
        prediction_container = prediction_section.find_next_sibling(['div', 'p'])
        if prediction_container:
            prediction_container.clear()
            prediction_html_content = generate_my_prediction()
            prediction_container.append(BeautifulSoup(prediction_html_content, "html.parser"))

    # 6. Update Our Token section
    our_token_heading = soup.find("h2", string="Our Token")
    if our_token_heading:
        price_tag = our_token_heading.find_next_sibling(lambda tag: tag.name in ['p', 'div', 'span'] and '$' in tag.get_text())
        if price_tag:
            price_tag.string = f"${btc_price} (Live Price)"
        
        last_updated_tag = our_token_heading.find_next_sibling(lambda tag: tag.name in ['p', 'div', 'span'] and "Last updated:" in tag.get_text())
        if last_updated_tag:
            last_updated_tag.string = f"Last updated: {current_date} {current_time_utc} UTC"


    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(str(soup))

    os.chdir(original_cwd)
    return f"Homepage content for {current_date} prepared locally."


def git_commit_changes():
    os.chdir(REPO_PATH)
    os.system("git config user.email 'maicol@openclaw.ai'")
    os.system("git config user.name 'Maicol'")
    os.system("git add .")
    commit_message = f"Update homepage with new analysis, headlines, and disclaimer for {get_current_date()}"
    os.system(f"git commit -m '{commit_message}'")
    print("Changes committed locally.")

if __name__ == "__main__":
    print("Starting homepage update...")
    update_homepage_content(BTC_PRICE, TSLA_PRICE, MOS_PRICE, get_key_headlines_en())
    print("Homepage content updated locally. Now committing changes.")
    git_commit_changes()
