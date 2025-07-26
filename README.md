# Adobe "Connecting the Dots" Challenge

This repository contains solutions for Adobe's Hackathon challenge focused on reimagining PDF reading experiences through intelligent document analysis.

## 🌐 Live Demo

**Website**: https://harshitabansal26.github.io/Adobe-hackathon-2025-Akatsuki/
**Demo**: https://harshitabansal26.github.io/Adobe-hackathon-2025-Akatsuki/demo.html

## Challenge Overview

The challenge consists of two rounds:

- **Round 1A**: Extract structured outlines from PDFs (Title, H1, H2, H3 headings)
- **Round 1B**: Build persona-driven document intelligence for relevant section extraction

## Project Structure

```
├── round1a/                 # PDF Outline Extraction
│   ├── src/                 # Source code
│   ├── Dockerfile          # Docker configuration
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Round 1A specific documentation
├── round1b/                 # Persona-Driven Intelligence
│   ├── src/                 # Source code
│   ├── Dockerfile          # Docker configuration
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Round 1B specific documentation
├── samples/                 # Sample input/output files
│   ├── input/              # Sample PDFs
│   └── output/             # Expected JSON outputs
└── docs/                   # Additional documentation
```

## Quick Start

### Round 1A - PDF Outline Extraction

```bash
cd round1a
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:latest
```

### Round 1B - Persona-Driven Intelligence

```bash
cd round1b
docker build --platform linux/amd64 -t persona-intelligence:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none persona-intelligence:latest
```

## Technical Constraints

- **CPU Only**: No GPU dependencies
- **Offline**: No internet access during execution
- **Model Size**: ≤ 200MB (Round 1A), ≤ 1GB (Round 1B)
- **Performance**: ≤ 10s for 50-page PDF (1A), ≤ 60s for document collection (1B)
- **Architecture**: AMD64 (x86_64) compatible

## Approach

### Round 1A

- Uses PyMuPDF for PDF text extraction
- Implements intelligent heading detection based on font properties, positioning, and text patterns
- Multilingual support for various document types
- Hierarchical structure analysis for proper H1/H2/H3 classification

### Round 1B

- Leverages lightweight NLP models for semantic understanding
- Implements persona-aware content filtering and ranking
- Uses document structure from Round 1A for enhanced section identification
- Provides relevance scoring for extracted sections and sub-sections

## Development

Each round is self-contained with its own dependencies and Docker configuration. See individual README files in `round1a/` and `round1b/` directories for detailed implementation notes.

## License

This project is developed for Adobe's Hackathon Challenge 2025.
