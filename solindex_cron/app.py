import json
from bs4 import BeautifulSoup
from datetime import datetime
import boto3
import os
from decimal import Decimal
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')


def fetch_data(url, tokens):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Click on Filters button and select the desired token number
    filters_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div[1]/div/form/div/div[2]/button/button"))
    )
    filters_button.click()

    token_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/button"))
    )
    token_button.click()

    if tokens == 5:
        token_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[3]/div[1]"))
        )
    elif tokens == 10:
        token_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[3]/div[2]"))
        )
    elif tokens == 15:
        token_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[3]/div[3]"))
        )
    elif tokens == 20:
        token_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[3]/div[4]"))
        )

    token_option.click()

    # Fetch page source after filter selection
    html = driver.page_source
    driver.quit()

    return html


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select("table tbody tr")
    data = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            name = cols[0].text.strip()
            price = (cols[1].text.strip()
                     .replace('$', '')
                     .replace('₀', '0')
                     .replace('₁', '1')
                     .replace('₂', '2')
                     .replace('₃', '3')
                     .replace('₄', '4')
                     .replace('₅', '5')
                     .replace('₆', '6')
                     .replace('₇', '7')
                     .replace('₈', '8')
                     .replace('₉', '9')
                     )
            try:
                price = Decimal(price)
                data.append((name, price))
            except ValueError:
                print(f"Skipping invalid price: {price}")

    return data


def store_data_in_dynamodb(data, index_name, timestamp):
    table = dynamodb.Table(os.environ["table"])

    with table.batch_writer() as batch:
        for name, price in data:
            unique_id = str(uuid.uuid4())
            try:
                batch.put_item(
                    Item={
                        'IndexName': index_name,
                        'CoinName': name,
                        'Timestamp': timestamp,
                        'Price': str(price),  # DynamoDB uses string for numbers
                        'UniqueId': unique_id  # Ensure uniqueness
                    }
                )
                print(f"Stored: {index_name}, {name}, {timestamp}, {price}, {unique_id}")
            except (NoCredentialsError, PartialCredentialsError) as e:
                print(f"Credentials error: {e}")
            except ClientError as e:
                print(f"Failed to insert {name} into DynamoDB: {e.response['Error']['Message']}")
            except Exception as e:
                print(f"Error storing data in DynamoDB: {e}")


def lambda_handler(event, context):
    urls = {
        "https://www.solindex.xyz/index/sol-essentials": "sol-essentials",
        "https://www.solindex.xyz/index/memes": "memes",
        "https://www.solindex.xyz/index/dogs": "dogs",
        "https://www.solindex.xyz/index/cats": "cats"
    }

    token_counts = [5, 10, 15, 20]
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S+00:00')

    for url, base_index_name in urls.items():
        for tokens in token_counts:
            index_name = f"{base_index_name}{tokens}"
            try:
                html = fetch_data(url, tokens)
                data = parse_html(html)
                store_data_in_dynamodb(data, index_name, timestamp)
            except Exception as e:
                print(f"Error fetching data from {url} with {tokens} tokens: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Data fetch and store completed successfully')
    }