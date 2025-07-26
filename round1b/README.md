# Round 1B: Persona-Driven Document Intelligence

This solution acts as an intelligent document analyst, extracting and prioritizing the most relevant sections from a collection of documents based on a specific persona and their job-to-be-done.

## Approach

### Core Strategy
1. **Document Section Extraction**: Extracts meaningful sections from multiple PDFs while preserving document context
2. **Persona-Aware Analysis**: Uses persona-specific keywords and job description matching to score relevance
3. **Intelligent Ranking**: Ranks sections based on multi-factor relevance scoring
4. **Subsection Refinement**: Extracts key subsections with refined text for granular analysis

### Key Features
- **Multi-Document Processing**: Handles 3-10 related PDFs simultaneously
- **Persona Recognition**: Identifies persona types (researcher, student, analyst, manager, developer) and applies appropriate filtering
- **Job-Specific Relevance**: Matches content to specific job-to-be-done requirements
- **Hierarchical Analysis**: Provides both section-level and subsection-level insights
- **Contextual Understanding**: Maintains document and page number context for all extracted content

### Technical Implementation

#### Section Extraction
- Extracts text from PDFs while preserving document structure
- Identifies section boundaries using paragraph breaks and formatting cues
- Generates unique section IDs for tracking and reference
- Filters out very short or irrelevant content

#### Relevance Scoring Algorithm
1. **Persona Keywords**: Matches content against persona-specific vocabulary
2. **Job Description Matching**: Scores based on job-specific terms and requirements
3. **Content Quality**: Evaluates section length, structure, and information density
4. **Contextual Relevance**: Considers document type and section positioning

#### Ranking and Prioritization
- Multi-factor scoring combining persona relevance, job alignment, and content quality
- Importance ranking from 1 (most relevant) to N (least relevant)
- Top-K selection to focus on most valuable content
- Balanced representation across input documents

## Models and Libraries Used

- **PyMuPDF (fitz)**: PDF text extraction and processing
- **scikit-learn**: TF-IDF vectorization and similarity calculations
- **NLTK**: Natural language processing, tokenization, and stopword removal
- **NumPy**: Numerical operations for scoring and ranking
- **No large ML models**: Uses lightweight NLP techniques for fast, reliable processing

## Performance Characteristics

- **Speed**: < 60 seconds for 3-5 document collections
- **Memory**: < 500MB RAM usage
- **Model Size**: < 50MB (NLTK data only)
- **Scalability**: Handles up to 10 documents efficiently

## Build and Run

```bash
# Build the Docker image
docker build --platform linux/amd64 -t persona-intelligence:latest .

# Run the container
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-intelligence:latest
```

## Input/Output Format

### Input
- Multiple PDF files in `/app/input/` directory
- Configuration file `config.json` with:
  ```json
  {
    "documents": ["doc1.pdf", "doc2.pdf", "doc3.pdf"],
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare comprehensive literature review focusing on methodologies"
  }
  ```

### Output
- Single JSON file: `challenge1b_output.json`

### JSON Schema
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare comprehensive literature review",
    "processing_timestamp": "2025-01-27T10:30:00"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page_number": 3,
      "section_title": "Methodology",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "page_number": 3,
      "refined_text": "Key finding or methodology description...",
      "relevance_score": 0.85
    }
  ]
}
```

## Persona Types Supported

- **Researcher**: Focuses on methodology, analysis, findings, statistical significance
- **Student**: Emphasizes definitions, concepts, examples, fundamental principles
- **Analyst**: Targets trends, performance metrics, comparisons, financial data
- **Manager**: Highlights strategy, planning, objectives, decision frameworks
- **Developer**: Concentrates on implementation, technical specifications, algorithms

## Limitations and Considerations

- Requires well-structured input documents for optimal performance
- Persona recognition is keyword-based and may need refinement for specialized roles
- Works best with documents that have clear section boundaries
- Performance may vary with highly technical or domain-specific content

## Testing

The solution supports various test scenarios:
- Academic research papers for literature reviews
- Business reports for financial analysis
- Educational content for exam preparation
- Technical documentation for implementation guidance
