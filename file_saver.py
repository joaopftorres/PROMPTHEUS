import requests

from storage import OutputRepository


_output_repository = OutputRepository()

def save_text(text, filename, title, doc_type=None, info=""):
  _output_repository.save_text(text, filename, title, doc_type=doc_type, info=info)

        

def get_arxiv_bibtex(arxiv_id):
    """Fetches the BibTeX entry for an arXiv paper and adds the URL."""

    base_url = "https://arxiv.org/bibtex/"
    url = base_url + arxiv_id

    response = requests.get(url)
    response.raise_for_status()

    bibtex_entry = response.text

    # Remove any existing `url` line
    lines = bibtex_entry.split('\n')
    lines = [line for line in lines if not line.strip().startswith('url')]

    # Ensure there is a comma at the end of the second to last line
    if not lines[-2].strip().endswith(','):
        lines[-2] += ','

    # Add the URL field with proper indentation before the closing brace
    lines.insert(-1, f"      url = {{https://arxiv.org/abs/{arxiv_id}}},")

    return "\n".join(lines) + "\n"  # Add newline at the end for better formatting