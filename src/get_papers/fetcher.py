import requests
from typing import List

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def fetch_pubmed_ids(query: str, max_results: int = 100) -> List[str]:
    url = f"{BASE_URL}/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": str(max_results)}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

def fetch_details(pubmed_ids: List[str]) -> str:
    url = f"{BASE_URL}/efetch.fcgi"
    params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text
