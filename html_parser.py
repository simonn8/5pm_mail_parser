from bs4 import BeautifulSoup
from pathlib import Path
import json

def extract_topic_links(email_html:str):
    soup = BeautifulSoup(email_html, 'html.parser')
    spans = soup.find_all("span", class_="topic-tag")
    extracted_topics = {}
    for span in spans:
        table = span.findParents('table')[0].parent.parent.parent
        titles = table.find_all("h2")
        extracted_titles = []
        for title in titles:
            extracted_titles.append(title.get_text().strip())
        extracted_topics[span.get_text()] = extracted_titles
    
    first_row = soup.find("tr")
    # Check if a row is found
    if first_row:
        # Get the first cell (assuming it's a <td> element)
        first_div = first_row.find("td").find("div")
        intro_text = ""
        for child in first_div.children:
            if child.name != "p":
                break
            intro_text += " " + child.text.strip()
        extracted_topics["intro_text"] = intro_text
    return extracted_topics

#Putting all newsletters in a json file with all different segments of the mail as key's of a dictionary
with open("data/email_links.jsonl", "w", encoding="utf-8") as jsonl:
   for html_filename in Path("data/").glob("*.html"):
      with open(html_filename, "r") as f:
         html_text = f.read()
      links = extract_topic_links(html_text)
      links["publication_date"] = html_filename.as_posix()[-11:-5]
      assert len(links["publication_date"]) == 6, f"{links['publication_date']=}"
      jsonl.write(json.dumps(links, ensure_ascii=False) + "\n")