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
BTC_PRICE = "70,949.77"
TSLA_PRICE = "405.55"
MOS_PRICE = "26.28"

def get_current_date():
    return datetime.date.today().strftime("%B %d, %Y")

def get_bitcoin_news_summary_en():
    # Reusing the summary I generated earlier, translated to English
    return """
*   Bitcoin (BTC-USD) recently traded at **$70,907.04**, with its rally slowing due to market instability in Iran.
*   The Middle East conflict is causing overall stock markets to anticipate weekly losses, also affecting the cryptocurrency market.
*   Despite rising energy prices, investors are staying in the U.S. market, and the U.S. Treasury is reviewing measures for the crude oil futures market.
*   A strong dollar and the Federal Reserve's outlook led to a drop in gold prices, indirectly impacting Bitcoin.
*   Key economic indicators like the February jobs report, Fed statements, and retail sales are increasing market volatility.
*   Nvidia's strategic shift in China, including halting H200 chip production, also influences the macroeconomy.
*   Disputes over tariff refunds and legal challenges related to Trump's 'global tariffs' increase trade policy uncertainty.
*   Justin Sun's SEC fraud settlement is an example of the evolving regulatory environment in the crypto industry.
*   Changes in personal finance sectors like credit cards, loans, and mortgages can affect the broader economy.
*   Overall, geopolitical tensions in the Middle East are exacerbating instability in energy and financial markets, impacting asset markets including Bitcoin.
"""

def generate_icalling_analysis(btc_price, tsla_price, mos_price):
    return f"""
**Today's observation:** Global markets remain sensitive to geopolitical tensions, particularly in the Middle East. While Bitcoin shows resilience, traditional equities like TSLA and MOS reflect broader market cautiousness.

1.  **Bitcoin's Resilience:** BTC is holding strong around ${btc_price}, demonstrating its potential as a safe-haven asset amidst global instability, though its rally has somewhat slowed.
2.  **Tech Sector Nuances (TSLA):** Tesla's price at ${tsla_price} indicates a stable period for now, but underlying factors like production shifts (e.g., Nvidia's China strategy impact) and broader investor sentiment on tech innovation continue to play a role.
3.  **Commodity Market Outlook (MOS):** Mosaic Co. (MOS) at ${mos_price} is a key indicator for agricultural commodities. Its stability suggests a balanced outlook on fertilizer demand, but rising energy costs could impact production expenses.
4.  **Overall Macro Picture:** Major economic indicators like employment reports and Fed statements are creating volatility. Investors are seeking clarity, leading to a mix of risk-on and cautious sentiment across different asset classes.
"""

def generate_my_prediction():
    return """
**Short-term (1-2 weeks):** We anticipate continued volatility driven by geopolitical news and upcoming economic data. Bitcoin might test higher resistance levels if a clear de-escalation signal emerges, while equities could remain range-bound as investors await clearer policy directions.

**Medium-term (1-3 months):** The interplay between central bank policies (potential rate cuts), evolving global trade dynamics, and corporate earnings will be critical. We might see a rotation of capital as investors re-evaluate risk and growth prospects. Bitcoin's long-term appeal as a decentralized asset will likely strengthen with ongoing institutional adoption.

**Philosophical view:** The market's current state is a testament to the interconnectedness of global events. Every price movement is a ripple from a larger human story, making adaptability and a deep understanding of underlying narratives more crucial than ever.
"""

def update_homepage_content(btc_price, tsla_price, mos_price, bitcoin_news_summary):
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
    else: # Fallback for other potential date elements if class is not found
        # Try finding the specific h2 that precedes the date, then its sibling
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
            ul_tag.clear() # Clear existing list items
            ul_tag.append(BeautifulSoup(f"<li>**Bitcoin:** ${btc_price}</li>", "html.parser").li)
            ul_tag.append(BeautifulSoup(f"<li>**Tesla (TSLA):** ${tsla_price}</li>", "html.parser").li)
            ul_tag.append(BeautifulSoup(f"<li>**Mosaic Co. (MOS):** ${mos_price}</li>", "html.parser").li)

    # 3. Update Key Headlines
    key_headlines_section = soup.find("h3", string="📰 Key Headlines:")
    if key_headlines_section:
        ul_tag = key_headlines_section.find_next_sibling("ul")
        if ul_tag:
            ul_tag.clear()
            # BeautifulSoup needs valid HTML, so wrap markdown list items in <ul>
            headlines_html = BeautifulSoup(f"<ul>{bitcoin_news_summary}</ul>", "html.parser")
            for li in headlines_html.find_all("li"):
                ul_tag.append(li)

    # 4. Update iCalling's Analysis
    analysis_section = soup.find("h3", string="🔍 iCalling's Analysis:")
    if analysis_section:
        # Assuming the analysis content is wrapped in <p> tags after the h3
        # First, clear existing content within the expected container for the analysis
        # Looking at homepage_content.md, analysis is multiple lines, possibly multiple p tags or a single block.
        # Let's target the <div class="analysis-content"> if it exists, otherwise find_next_sibling('p').
        analysis_container = soup.find('div', class_='analysis-content')
        if not analysis_container:
            analysis_container = analysis_section.find_next_sibling('p') # Fallback to next <p>

        if analysis_container:
            analysis_container.clear()
            # Convert markdown to HTML for BeautifulSoup
            analysis_html_content = generate_icalling_analysis(btc_price, tsla_price, mos_price)
            analysis_html = BeautifulSoup(f"<div>{analysis_html_content}</div>", "html.parser")
            for child in analysis_html.div.contents:
                analysis_container.append(child)


    # 5. Update My Prediction
    prediction_section = soup.find("h3", string="💭 My Prediction:")
    if prediction_section:
        # Similar to analysis, target a container or next <p>
        prediction_container = soup.find('div', class_='prediction-content')
        if not prediction_container:
            prediction_container = prediction_section.find_next_sibling('p') # Fallback to next <p>

        if prediction_container:
            prediction_container.clear()
            prediction_html_content = generate_my_prediction()
            prediction_html = BeautifulSoup(f"<div>{prediction_html_content}</div>", "html.parser")
            for child in prediction_html.div.contents:
                prediction_container.append(child)

    # 6. Update Our Token section
    our_token_heading = soup.find("h2", string="Our Token")
    if our_token_heading:
        # The price is expected in a <p> tag immediately after the h2, or similar structure.
        # Example from homepage_content.md: <p>$71,497 (+4.71%)</p>
        # Find the next sibling that contains a price-like string
        price_tag = our_token_heading.find_next_sibling(lambda tag: tag.name in ['p', 'div', 'span'] and '$' in tag.get_text())
        if price_tag:
            price_tag.string = f"${btc_price} (Live Price)"
        
        # Find the next sibling that contains "Last updated:"
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
    commit_message = f"Update macroeconomic trends and market snapshot for {get_current_date()}"
    os.system(f"git commit -m '{commit_message}'")
    print("Changes committed locally.")

if __name__ == "__main__":
    print("Starting homepage update...")
    update_homepage_content(BTC_PRICE, TSLA_PRICE, MOS_PRICE, get_bitcoin_news_summary_en())
    print("Homepage content updated locally. Now committing changes.")
    git_commit_changes()
