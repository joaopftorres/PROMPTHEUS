# PROMPTHEUS: A Human-Centered Pipeline to Streamline SLRs with LLMs

PROMPTHEUS is an AI-driven pipeline that automates major steps of a Systematic Literature Review (SLR), from query expansion and paper retrieval to topic modeling, summarization, and final LaTeX report generation.

It combines deterministic processing steps (retrieval, filtering, metrics) with LLM-powered steps (query generation, topic titles, summary refinement, document compilation).

## Journal Publication

This framework was published in *Information* (MDPI):

- Torres, J.; Mulligan, C.; Jorge, J.; Moreira, C. **PROMPTHEUS: A Human-Centered Pipeline to Streamline Systematic Literature Reviews with Large Language Models**. *Information* 2025, 16(5), 420. https://doi.org/10.3390/info16050420
- Article page: https://www.mdpi.com/2078-2489/16/5/420

![Diagram of the PROMPTHEUS Framework](./images/PROMPTHEUS.png)

## Table of Contents

1. Overview
2. Key Capabilities
3. Pipeline Stages
4. Requirements
5. Installation
6. Configuration
7. Usage
8. Output Artifacts
9. Project Structure
10. Troubleshooting

## Overview

PROMPTHEUS executes an SLR workflow in three phases:

1. Search and screening of candidate papers.
2. Data extraction and topic modeling.
3. Synthesis, summarization, and report generation.

The final outputs include plain-text intermediate artifacts, quality metrics, a BibTeX file, and a LaTeX SLR document.

## Key Capabilities

- LLM-based research topic expansion.
- LLM-based arXiv query generation.
- Semantic relevance filtering with Sentence-BERT cosine similarity.
- BERTopic clustering with generated section titles.
- T5 summarization and GPT post-editing.
- Automated LaTeX SLR compilation.
- Automatic report generation for included/excluded papers.
- Automatic quality metrics (ROUGE, readability, similarity).

## Pipeline Stages

1. `expand_title()` broadens the user topic.
2. `create_arxiv_query()` generates an arXiv query.
3. `search_arxiv()` retrieves candidate papers.
4. `filter_articles()` keeps most relevant papers by embedding similarity.
5. `topic_model_pipeline()` groups abstracts into topics.
6. `summarize()` and `improve_summary()` synthesize topic-level text.
7. `create_latex_document()` builds the final SLR document.
8. `run_metrics()` computes evaluation artifacts and diagnostic files.

## Requirements

- Python 3.10+
- `pip`
- OpenAI API key (for LLM-powered steps)

## Installation

1. Clone repository:

```bash
git clone https://github.com/joaopftorres/AI-SLR.git
cd AI-SLR/PROMPTHEUS
```

2. Create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
python3 -m spacy download en_core_web_sm
```

4. Create `.env` in project root:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

5. Optional bootstrap script:

```bash
./setup.sh
```

## Configuration

Main runtime defaults are centralized in `settings.py`.

Important values:

- `DEFAULT_GPT_MODEL`
- `DEFAULT_MAX_PAPERS`
- `SENTENCE_TRANSFORMER_MODEL`
- `T5_SUMMARIZER_MODEL`
- `OUTPUT_ROOT_DIR`

## Usage

Basic run:

```bash
python3 main.py "Title of the Literature Review"
```

With custom model and paper limit:

```bash
python3 main.py "AI in Healthcare" --gpt_model "gpt-4o" --max_papers 50
```

Help:

```bash
python3 main.py --help
```

## Output Artifacts

PROMPTHEUS writes all run artifacts under:

```text
output/<topic_slug>/
```

Where `<topic_slug>` is the input title with spaces replaced by underscores (for example `AI_in_Healthcare`).

### Output directory map

```text
output/
  <topic_slug>/
    generated_files/
      abstracts.txt
      T5_summaries.txt
      GPT_edited_summary.txt
      SLR_latex.txt
      SLR.txt
    reports/
      included_report.txt
      excluded_report.txt
      topic_report.txt
    metrics/
      rouge_metrics.txt
      readability_metrics.txt
      similarity_scores_bar.png
    SLR/
      <topic_slug>.bib
      <topic_slug>-literature_review.tex
```

### What each artifact means

- `generated_files/abstracts.txt`: concatenated raw abstracts of selected papers.
- `generated_files/T5_summaries.txt`: direct T5-generated summaries per topic.
- `generated_files/GPT_edited_summary.txt`: post-edited topic summaries after GPT refinement.
- `generated_files/SLR_latex.txt`: plain text dump of generated LaTeX content.
- `generated_files/SLR.txt`: de-LaTeXed plain-text version of the final document.
- `reports/included_report.txt`: list of selected papers and similarity scores.
- `reports/excluded_report.txt`: list of filtered-out papers and similarity scores.
- `reports/topic_report.txt`: topic model diagnostics, topic keywords, generated topic titles.
- `metrics/rouge_metrics.txt`: ROUGE-1 precision/recall/F1 for generated outputs.
- `metrics/readability_metrics.txt`: readability statistics for summary variants.
- `metrics/similarity_scores_bar.png`: chart of input-vs-document cosine similarity.
- `SLR/<topic_slug>.bib`: BibTeX entries for selected references.
- `SLR/<topic_slug>-literature_review.tex`: final LaTeX SLR manuscript.

### Notes

- `output/__init__.py` exists only as a package marker and is not a generated artifact.
- `generated_slrs/` contains historical sample PDFs and can be treated as example material.

## Project Structure

```text
PROMPTHEUS/
  main.py                      # End-to-end pipeline orchestration
  prompts.py                   # LLM prompt templates and generation helpers
  query_arxiv.py               # arXiv retrieval
  cleaner.py                   # text preprocessing and selection helpers
  topic_model.py               # BERTopic modeling and topic title generation
  summarizer_pipeline.py       # T5 summarization + GPT post-edit
  metrics.py                   # ROUGE, readability, coherence, similarity helpers
  file_saver.py                # persistence adapter used by pipeline
  settings.py                  # centralized defaults/constants
  llm/
    client.py                  # OpenAI client bootstrap
  storage/
    output_repository.py       # output path and file persistence policy
  images/                      # architecture image used in documentation
  output/                      # run outputs and generated artifacts
```

## Troubleshooting

### Build failure for `hdbscan` (WSL/Linux)

If you see errors like `x86_64-linux-gnu-gcc: No such file or directory` or `Python.h: No such file or directory`:

```bash
sudo apt update
sudo apt install -y build-essential python3-dev python3.12-dev
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
python3 -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
python3 -m spacy download en_core_web_sm
```