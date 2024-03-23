import webbrowser
import difflib
import sys
import time

import requests
from bs4 import BeautifulSoup
import re
import os
import fitz
import random
import pymongo


def arxiv_search(query):
    search_url = f"https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&order=-announced_date_first&size=50"
    webbrowser.open(search_url)
    return search_url


def suggest_correction(query):

    dictionary = ["Algebraic Geometry", "Algebraic Topology", "Analysis of PDEs", "Category Theory",
                  "Classical Analysis and ODEs", "Combinatorics", "Commutative Algebra", "Complex Variables",
                  "Differential Geometry", "Dynamical Systems", "Functional Analysis", "General Mathematics",
                  "General Topology", "Geometric Topology", "Group Theory", "History and Overview",
                  "Information Theory", "K-Theory and Homology", "Logic", "Mathematical Physics", "Metric Geometry",
                  "Number Theory", "Numerical Analysis", "Operator Algebras", "Optimization and Control", "Probability",
                  "Quantum Algebra", "Representation Theory", "Rings and Algebras", "Spectral Theory",
                  "Statistics Theory", "Symplectic Geometry",

                  "Computation and Language", "Computational Complexity", "Computational Engineering",
                  "Finance, and Science", "Computational Geometry", "Computer Science and Game Theory",
                  "Computer Vision and Pattern Recognition", "Computers and Society", "Cryptography and Security",
                  "Data Structures and Algorithms", "Databases", "Artificial Intelligence", "Digital Libraries",
                  "Discrete Mathematics", "Distributed, Parallel, and Cluster Computing", "Emerging Technologies",
                  "Formal Languages and Automata Theory", "General Literature", "Graphics", "Hardware Architecture",
                  "Human-Computer Interaction", "Information Retrieval", "Information Theory",
                  "Logic in Computer Science", "Machine Learning", "Mathematical Software", "Multiagent Systems",
                  "Multimedia", "Networking and Internet Architecture", "Neural and Evolutionary Computing",
                  "Numerical Analysis", "Operating Systems", "Other Computer Science", "Performance",
                  "Programming Languages", "Robotics", "Social and Information Networks", "Software Engineering",
                  "Sound", "Symbolic Computation", "Systems and Control", "Python Programming", "R programming",
                  "Java Programming", "Data Manipulation", "Data Mining", "OpenCV", "Data Visualization",
                  "Data Preprocessing", "Database Programming", "Data Science", "Data Literacy", "Deep Learning",

                  "Biomolecules", "Cell Behavior", "Genomics", "Molecular Networks", "Neurons and Cognition",
                  "Other Quantitative Biology", "Populations and Evolution", "Quantitative Methods",
                  "Subcellular Processes", "Tissues and Organs",

                  "Computational Finance", "Economics", "General Finance", "Mathematical Finance", "Portfolio Management",
                  "Pricing of Securities", "Risk Management", "Statistical Finance", "Trading and Market Microstructure",

                  "Applications", "Computation", "Methodology", "Other Statistics", "Statistics Theory",

                  "Audio and Speech Processing", "Image and Video Processing", "Signal Processing", "Systems and Control",

                  "Econometrics", "General Economics", "Theoretical Economics",

                  "Astrophysics of Galaxies", "Cosmology and Nongalactic Astrophysics", "Earth and Planetary Astrophysics",
                  "High Energy Astrophysical Phenomena", "Instrumentation and Methods for Astrophysics", "Applied Physics",
                  "Solar and Stellar Astrophysics", "Disordered Systems and Neural Networks", "Materials Science",
                  "Mesoscale and Nanoscale Physics", "Other Condensed Matter", "Quantum Gases", "Soft Condensed Matter",
                  "Statistical Mechanics", "Strongly Correlated Electrons", "Superconductivity", "Chaotic Dynamics",
                  "Adaptation and Self-Organizing Systems", "Cellular Automata and Lattice Gases", "Accelerator Physics",
                  "Exactly Solvable and Integrable Systems", "Pattern Formation and Solitons", "Atomic Physics",
                  "Atmospheric and Oceanic Physics", "Atomic and Molecular Clusters", "Biological Physics", "Geophysics",
                  "Chemical Physics", "Classical Physics", "Computational Physics", "Statistics and Probability",
                  "Data Analysis", "Fluid Dynamics", "General Physics", "History and Philosophy of Physics", "Optics",
                  "Instrumentation and Detectors", "Medical Physics", "Physics and Society", "Physics Education",
                  "Plasma Physics", "Popular Physics", "Space Physics"]

    closest_match = difflib.get_close_matches(query, dictionary, n=1, cutoff=0.7)

    if closest_match:
        suggestion = closest_match[0]
        correction = input(f"Did you mean '{suggestion}'? (Y/N): ")
        if correction.upper() == "Y":
            return suggestion
        else:
            print("Query is terminating...")
            time.sleep(1)
            sys.exit(1)

    return query


if __name__ == "__main__":
    search_query = input("Enter the keyword you want to search on Arxiv.: ")

    corrected_query = suggest_correction(search_query)
    print(corrected_query)

    url = arxiv_search(corrected_query)

    response = requests.get(url)
    page_content = response.content
    soup = BeautifulSoup(page_content, "html.parser")

    Article_type_examples = ["research paper", "scientific article", "conference"]


    # ----------- Lists for scraping process --------
    article_ids = []
    article_names = []
    article_writers = []
    article_types = []
    article_publication_dates = []
    article_publisher_name = []
    keyword_related_query = []
    keywords_related_article = []
    article_summaries = []
    article_references = []
    article_quotes = []
    article_url_address = []
    article_pdfs = []

    # ----- Connect Operations for MongoDB ------
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydatabase = client["articledatabase"]
    mycollection = mydatabase["articledatas"]


    def clear_lists():  # ----- Delete Operations -----

        article_ids.clear()
        article_names.clear()
        article_writers.clear()
        article_types.clear()
        article_publication_dates.clear()
        article_publisher_name.clear()
        keyword_related_query.clear()
        keywords_related_article.clear()
        article_summaries.clear()
        article_references.clear()
        article_quotes.clear()
        article_url_address.clear()
        article_pdfs.clear()

        # -------------- End of "clear_lists" function ------------


    def scrap_arxiv(limit=10, info=True):  # ------------ Scraping Operations ----------

        if info:
            #count_of_article = 1
            for i in range(limit):
                keyword_related_query.append(corrected_query)
                random_quotation = random.randint(1, 400)
                article_quotes.append(random_quotation)
                chosen_species = random.choices(Article_type_examples, weights=[30, 60, 10], k=1)[0]
                article_types.append(chosen_species)

        # --------------- Titles and IDs of The Articles -------------------
        count_of_article = 1
        article_divs = soup.find_all('p', class_='title is-5 mathjax')
        for article_div in article_divs:
            if count_of_article > limit:
                break
            else:
                article_ids.append(count_of_article)
                article_publisher_name.append("Arxiv")
                title_nonclear = article_div.text
                title_cleared = title_nonclear.strip("\n ")
                article_names.append(title_cleared)
                count_of_article += 1

        # ---------------- Authors of Articles ------------------
        count_of_article = 1
        article_divs = soup.find_all('p', class_='authors')
        for article_div in article_divs:
            if count_of_article > limit:
                break
            else:
                authors_nonclear = article_div.text
                authors_cleared = authors_nonclear[9:]
                authors_cleared = " ".join(authors_cleared.split())
                article_writers.append(authors_cleared)
                count_of_article += 1

        # -------------------- Abstracts of Articles ---------------------
        count_of_article = 1
        article_divs = soup.find_all('p', class_='abstract mathjax')
        for article_div in article_divs:
            if count_of_article > limit:
                break
            else:
                summaries_nonclear = article_div.find('span', class_='abstract-full has-text-grey-dark mathjax')
                summaries_cleared = summaries_nonclear.text.strip("\n ")
                summaries_cleared = summaries_cleared[:-17]
                article_summaries.append(summaries_cleared)
                count_of_article += 1

        # ------------- Publication Dates of Articles -------------
        count_of_article = 1
        article_divs = soup.find_all('p', class_='is-size-7')
        for article_div in article_divs:
            if count_of_article > limit:
                break
            else:
                dates_nonclear = article_div.find('span', class_='has-text-black-bis has-text-weight-semibold')
                if dates_nonclear and "Submitted" in dates_nonclear.text:
                    dates_nonclear = article_div.text.replace("\n", "")
                    dates_cleared = re.sub(r'\s+', ' ', dates_nonclear)
                    article_publication_dates.append(dates_cleared)
                    count_of_article += 1




        # ----------------------- PDF Urls of Articles ----------------------------
        count_of_article = 1
        article_divs = soup.find_all('p', class_='list-title is-inline-block')
        for article_div in article_divs:
            if count_of_article > limit:
                break
            else:
                pdf_link = article_div.find('a', href=True, string='pdf')
                if pdf_link:
                    article_pdfs.append(pdf_link['href'])
                    count_of_article += 1

        # -------------------------- URLs of Articles -----------------------------
        count_of_article = 1
        article_divs = soup.find_all('p', class_='list-title is-inline-block')
        for article_div in article_divs:
            if count_of_article > limit:
                break
            else:
                abs_link = article_div.find('a', href=True)
                if abs_link:
                    article_url_address.append(abs_link['href'])
                    count_of_article += 1

        # ----------------------- Keywords of Articles ------------------------
        count_of_article = 1
        article_divs = soup.find_all('div', class_='tags is-inline-block')
        for article_div in article_divs:
            if count_of_article > limit:
                break
            else:
                tooltip_values = [span['data-tooltip'] for span in article_div.find_all('span', {'data-tooltip': True})]
                keywords_related = ", ".join(tooltip_values)
                keywords_related_article.append(keywords_related)
                count_of_article += 1

        # --------------------- Excerpts of Articles ------------------------

        # ---------- End of "scrap_arxiv" function ----------


    def download_pdf(url, destination_folder="."):  # ----- Download Operations -----
        response = requests.get(url)

        if response.status_code == 200:
            file_name = url.split("/")[-1]
            file_name_with_extension = f"{file_name}.pdf"
            file_path = os.path.join(destination_folder, file_name_with_extension)

            with open(file_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            print(f"{file_name_with_extension} was downloaded successfully.")
        else:
            print(f"{url} could not download. HTTP Error: {response.status_code}")

        # ---------- End of "download_pdf" function ----------


    def process_pdf_file(pdf_path):  # ----- Extract References Operations
        pdf_document = fitz.open(pdf_path)
        page_count = pdf_document.page_count

        found_references = False
        reference_index = 0
        total_str = ""
        for page_number in range(page_count):
            page = pdf_document.load_page(page_number)

            text = page.get_text("text")

            if "REFERENCES" in text.upper() or "References" in text:
                found_references = True
                reference_index = text.upper().find("REFERENCES")

            if found_references:
                total_str = total_str + text

        pdf_document.close()

        references_index = total_str.upper().find("REFERENCES")
        if references_index != -1:
            references_part = total_str[references_index + len("REFERENCES"):].strip()
            article_references.append(references_part)
        else:
            article_references.append("None")

        # ----- End of "process_pdf_file" function -----


    def write_database(limit):  # ----- Write Operations to MongoDB
        #delete_result = mycollection.delete_many({})
        for i in range(limit):
            data = {
                "Article id": article_ids[i],
                "Article name": article_names[i],
                "Article authors": article_writers[i],
                "Article types": article_types[i],
                "Article publication date": article_publication_dates[i],
                "Article publisher name": article_publisher_name[i],
                "Article keywords": keywords_related_article[i],
                "Query keywords": keyword_related_query[i],
                "Article abstract": article_summaries[i],
                "Article references":article_references[i],
                "Article quotes": article_quotes[i],
                "Article url adress": article_url_address[i],
                "Article pdf adress": article_pdfs[i]
            }
            mycollection.insert_one(data)

        # ----- End of "write_database" function -----


    Number_of_articles_to_process = 5 # Count of Article

    scrap_arxiv(Number_of_articles_to_process, True)  # ----- Get Some Informations With Count of Article -----

    download_folder = "downloaded_pdf"  # ----- Specify the folder to download PDFs -----
    os.makedirs(download_folder, exist_ok=True)  # ----- Create the folder (if not already created) -----
    for pdf_url in article_pdfs:  # ----- Download PDFs -----
        download_pdf(pdf_url, download_folder)

    pdf_folder = "downloaded_pdf"  # ----- Indicate Folder -----

    try:  # ----- Deletions Operations for "downloaded_pdf" Folder
        os.rmdir(pdf_folder)
        print(f"{pdf_folder} folder successfully deleted.")
    except OSError as e:
        print(f"Error: Could not delete folder {pdf_folder}. Error code: {e.errno}, Error message: {e.strerror}")

    for filename in os.listdir(pdf_folder):  # ----- Get Folder's Element -----
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            process_pdf_file(pdf_path)

    write_database(Number_of_articles_to_process)  # ----- Write All Informations to MongoDB ------

    print("=========================")
    print(article_ids)
    print(article_names)
    print(article_writers)
    print(article_types)
    print(article_publication_dates)
    print(article_publisher_name)
    print(keywords_related_article)
    print(keyword_related_query)
    print(article_summaries)
    print(article_references)
    print(article_quotes)
    print(article_url_address)
    print(article_pdfs)
    print("=========================")


