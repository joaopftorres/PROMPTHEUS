import json
from pathlib import Path

from settings import OUTPUT_ROOT_DIR


class OutputRepository:
    """Persists generated artifacts under the output directory tree."""

    def __init__(self, root_dir=OUTPUT_ROOT_DIR):
        self.root_dir = Path(root_dir)

    def save_text(self, text, filename, title, doc_type=None, info=""):
        path_name = title + info

        if doc_type:
            if doc_type == "bib":
                directory = "SLR"
            else:
                directory = doc_type
        else:
            directory = "results"

        target_dir = self.root_dir / path_name / directory
        target_dir.mkdir(parents=True, exist_ok=True)

        if doc_type == "SLR":
            target_path = target_dir / f"{filename}.tex"
            target_path.write_text(text)
        elif doc_type == "bib":
            target_path = target_dir / f"{filename}.bib"
            with target_path.open("a") as out_file:
                out_file.write(text + "\n")
        elif doc_type == "metrics":
            target_path = target_dir / f"{filename}.txt"
            target_path.write_text(json.dumps(text, indent=4))
        else:
            target_path = target_dir / f"{filename}.txt"
            target_path.write_text(text)
