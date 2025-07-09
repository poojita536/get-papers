import xml.etree.ElementTree as ET
from typing import List, Dict

def is_academic(affiliation: str) -> bool:
    keywords = ["university", "college", "hospital", "school", "institute"]
    return any(word in affiliation.lower() for word in keywords)

def parse_articles(xml_data: str) -> List[Dict[str, str]]:
    root = ET.fromstring(xml_data)
    results = []

    for article in root.findall(".//PubmedArticle"):
        record = {
            "PubmedID": article.findtext(".//PMID"),
            "Title": article.findtext(".//ArticleTitle"),
            "Publication Date": article.findtext(".//PubDate/Year") or "Unknown",
            "Non-academic Author(s)": "",
            "Company Affiliation(s)": "",
            "Corresponding Author Email": "Not found"
        }

        authors, companies, email = [], [], "Not found"
        for author in article.findall(".//Author"):
            name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()
            aff = author.findtext(".//AffiliationInfo/Affiliation")
            if aff:
                if "@" in aff:
                    email = aff.split()[-1]
                if not is_academic(aff):
                    authors.append(name)
                    companies.append(aff)

        if authors:
            record["Non-academic Author(s)"] = "; ".join(authors)
            record["Company Affiliation(s)"] = "; ".join(companies)
            record["Corresponding Author Email"] = email
            results.append(record)

    return results
