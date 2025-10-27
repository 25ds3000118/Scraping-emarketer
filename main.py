from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_outline(country: str = Query(..., description="Country name")):
    url = f"https://en.wikipedia.org/wiki/{country}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch Wikipedia page: {str(e)}"}

    soup = BeautifulSoup(response.text, "lxml")
    headings = soup.find_all([f"h{i}" for i in range(1, 7)])

    if not headings:
        return {"error": "No headings found on the Wikipedia page."}

    markdown = "## Contents\n\n"
    for tag in headings:
        level = int(tag.name[1])  # h1 -> 1, h2 -> 2, etc.
        text = tag.get_text().strip()
        markdown += f"{'#' * level} {text}\n\n"

    return {"country": country, "outline": markdown}
