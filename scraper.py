import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

def crawl_cnyes_usstock():
    """
    Crawl US stock data from cnyes.com/usstock
    """
    url = "https://www.cnyes.com/usstock"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"Starting to crawl: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract stock data - this will depend on the actual structure of the page
        stock_data = []

        # Look for common stock data patterns
        stock_tables = soup.find_all('table')
        stock_rows = soup.find_all('tr')

        for row in stock_rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 3:  # Assuming at least 3 columns for stock data
                row_data = [cell.get_text(strip=True) for cell in cells]
                if any(row_data):  # Only add non-empty rows
                    stock_data.append(row_data)

        # If no table data found, try to extract any text content
        if not stock_data:
            content_divs = soup.find_all('div', class_=['stock', 'quote', 'price', 'ticker'])
            for div in content_divs:
                text = div.get_text(strip=True)
                if text:
                    stock_data.append({'content': text})

        # Create output data
        result = {
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'total_items': len(stock_data),
            'data': stock_data[:50]  # Limit to first 50 items to avoid huge files
        }

        # Save to JSON file
        output_file = f"cnyes_usstock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Successfully crawled {len(stock_data)} items")
        print(f"Data saved to: {output_file}")

        return result

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

if __name__ == "__main__":
    crawl_cnyes_usstock()