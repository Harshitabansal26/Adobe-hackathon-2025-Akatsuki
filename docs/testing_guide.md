# Testing Guide

This guide provides comprehensive instructions for testing both Round 1A and Round 1B solutions.

## Prerequisites

- Docker installed and running
- Sample PDF files for testing
- Basic understanding of command line operations

## Round 1A Testing

### Quick Test

1. **Prepare test files**:
   ```bash
   mkdir -p input output
   # Place your PDF files in the input directory
   ```

2. **Build and run**:
   ```bash
   cd round1a
   docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
   docker run --rm -v $(pwd)/../input:/app/input -v $(pwd)/../output:/app/output --network none pdf-outline-extractor:latest
   ```

3. **Check results**:
   - Look for JSON files in the `output` directory
   - Each PDF should have a corresponding `.json` file
   - Verify the JSON structure matches the required format

### Expected Output Format

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "Background",
      "page": 2
    }
  ]
}
```

### Performance Validation

- Processing time should be < 10 seconds for 50-page PDFs
- Memory usage should remain reasonable
- No network calls should be made (--network none)

## Round 1B Testing

### Setup Test Environment

1. **Prepare input directory**:
   ```bash
   mkdir -p input_1b output_1b
   ```

2. **Create configuration file** (`input_1b/config.json`):
   ```json
   {
     "documents": [
       "/app/input/doc1.pdf",
       "/app/input/doc2.pdf"
     ],
     "persona": "PhD Researcher in Computer Science",
     "job_to_be_done": "Literature review focusing on methodologies"
   }
   ```

3. **Add PDF files** to `input_1b/` directory

### Build and Run

```bash
cd round1b
docker build --platform linux/amd64 -t persona-intelligence:latest .
docker run --rm -v $(pwd)/../input_1b:/app/input -v $(pwd)/../output_1b:/app/output --network none persona-intelligence:latest
```

### Expected Output

The system will generate `challenge1b_output.json` with:

```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "PhD Researcher in Computer Science", 
    "job_to_be_done": "Literature review focusing on methodologies",
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
      "refined_text": "Key methodology description...",
      "relevance_score": 0.85
    }
  ]
}
```

## Test Scenarios

### Scenario 1: Academic Research
- **Documents**: Research papers on a specific topic
- **Persona**: PhD Researcher
- **Job**: Literature review preparation
- **Expected**: High relevance for methodology, results, conclusions

### Scenario 2: Business Analysis  
- **Documents**: Annual reports, financial statements
- **Persona**: Investment Analyst
- **Job**: Financial trend analysis
- **Expected**: Focus on financial metrics, performance data

### Scenario 3: Student Learning
- **Documents**: Textbook chapters
- **Persona**: Undergraduate Student
- **Job**: Exam preparation
- **Expected**: Emphasis on definitions, key concepts, examples

## Validation Checklist

### Round 1A
- [ ] JSON output format is correct
- [ ] All heading levels (H1, H2, H3) are properly identified
- [ ] Page numbers are accurate
- [ ] Title extraction works correctly
- [ ] Processing time < 10 seconds for 50-page PDFs
- [ ] Works with multilingual documents

### Round 1B
- [ ] JSON output matches required schema
- [ ] Sections are ranked by relevance
- [ ] Subsections contain meaningful content
- [ ] Processing time < 60 seconds for document collection
- [ ] Persona-specific content is prioritized
- [ ] Job description influences section selection

## Troubleshooting

### Common Issues

1. **Docker build fails**:
   - Check Docker is running
   - Verify platform specification (linux/amd64)
   - Check internet connection for dependency downloads

2. **No output generated**:
   - Verify input directory contains PDF files
   - Check file permissions
   - Review container logs

3. **Incorrect JSON format**:
   - Validate JSON using online tools
   - Check for encoding issues
   - Verify all required fields are present

4. **Performance issues**:
   - Monitor memory usage
   - Check PDF file sizes
   - Verify no network calls are being made

### Debug Commands

```bash
# Check container logs
docker logs <container_id>

# Run container interactively
docker run -it --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output persona-intelligence:latest /bin/bash

# Validate JSON output
python -m json.tool output/result.json
```

## Performance Benchmarks

### Round 1A Targets
- 10-page PDF: < 2 seconds
- 25-page PDF: < 5 seconds  
- 50-page PDF: < 10 seconds

### Round 1B Targets
- 3 documents: < 30 seconds
- 5 documents: < 45 seconds
- 10 documents: < 60 seconds

## Quality Metrics

### Round 1A
- Heading detection accuracy > 90%
- Title extraction accuracy > 85%
- False positive rate < 10%

### Round 1B  
- Section relevance accuracy > 80%
- Persona alignment score > 75%
- Job description matching > 70%
