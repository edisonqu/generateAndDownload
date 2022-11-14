import shutil
from bs4 import BeautifulSoup
import openai as openai
import os
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

def run(playwright):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    inputted_prompt = input("Input your Prompt: ")
    response = openai.Image.create(
        prompt= inputted_prompt,
        n=1,
        size="1024x1024"
    )

    image_url = response['data'][0]['url']  # URL of the website of the generated Art
    print(image_url)
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    page.goto(image_url)
    print(str(page.title()))
    title_html = page.title().strip("(1024×1024)")
    browser.close()
    return title_html,image_url

with sync_playwright() as playwright:
    image_name,image_url = run(playwright)
    img_data = requests.get(image_url).content
    with open(image_name, 'wb') as handler:
        handler.write(img_data)
        shutil.move(image_name, 'images')
    print("Success")
