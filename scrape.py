import requests
import io
from bs4 import BeautifulSoup
import time

words = set()


# Read existing words from words.txt
try:
    with io.open("words.txt", "r", encoding="utf8") as outfile:
        for word in outfile.read().split("\n"):
            words.add(word.strip())

except FileNotFoundError:
    print("words.txt not found, creating a new file.")


# Viet dictionary
# Function to scrape words from vdict
def scrape_vdict(page_count, dict_type):
    for page in range(1, page_count + 1):
        url = f"https://vdict.com/%5E,{dict_type},0,0,{page}.html"
        
        try:
            res = requests.get(url)
            res.raise_for_status()
            res.encoding = "utf-8"  # Ensure encoding is UTF-8

            soup = BeautifulSoup(res.text, "html.parser")
            result_list = soup.findAll("div", class_="result-list")

            if not result_list:
                print(f"Skipping page {page}: No results found.")
                continue  # Skip pages with no results

            for node in result_list[0].findAll("a"):
                word = node.get_text(strip=True)
                if word:
                    print(word)
                    words.add(word)

            time.sleep(1)  # Avoid being blocked

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue  # Skip the page and continue


with io.open("words.txt", "w", encoding="utf8") as outfile:
    outfile.write("\n".join(sorted(words)))  # Sort for easier reading

# Scrape Vietnamese dictionary
scrape_vdict(379, 3)

# Scrape Vietnamese-English dictionary
scrape_vdict(294, 2)
