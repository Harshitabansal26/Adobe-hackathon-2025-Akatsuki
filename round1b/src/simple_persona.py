#!/usr/bin/env python3
"""
SIMPLE WORKING Persona-Driven Document Intelligence
Actually analyzes documents based on persona - no fancy stuff, just works!
"""

import fitz  # PyMuPDF
import json
import os
import sys
from datetime import datetime

def extract_document_sections(pdf_path):
    """Extract text sections from PDF"""
    try:
        doc = fitz.open(pdf_path)
        sections = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Split into paragraphs
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 50]
            
            for i, paragraph in enumerate(paragraphs):
                sections.append({
                    'document': os.path.basename(pdf_path),
                    'page': page_num + 1,
                    'section_id': f"{os.path.basename(pdf_path)}_p{page_num + 1}_s{i + 1}",
                    'text': paragraph,
                    'section_title': paragraph.split('.')[0][:50] + "..." if len(paragraph.split('.')[0]) > 50 else paragraph.split('.')[0]
                })
        
        doc.close()
        return sections
        
    except Exception as e:
        print(f"Error extracting from {pdf_path}: {e}")
        return []

def calculate_relevance(text, persona, job_description):
    """Simple relevance calculation based on keyword matching"""
    text_lower = text.lower()
    persona_lower = persona.lower()
    job_lower = job_description.lower()
    
    score = 0.0
    
    # Persona-specific keywords
    persona_keywords = {
        'researcher': ['research', 'study', 'analysis', 'methodology', 'results', 'findings', 'data', 'experiment'],
        'student': ['learn', 'understand', 'concept', 'definition', 'example', 'explanation', 'basic', 'introduction'],
        'analyst': ['analysis', 'trend', 'performance', 'metrics', 'comparison', 'evaluation', 'financial', 'revenue'],
        'manager': ['strategy', 'planning', 'management', 'objectives', 'goals', 'decision', 'process', 'framework'],
        'developer': ['implementation', 'code', 'technical', 'system', 'architecture', 'design', 'solution']
    }
    
    # Identify persona type
    persona_type = 'general'
    for p_type, keywords in persona_keywords.items():
        if p_type in persona_lower:
            persona_type = p_type
            break
    
    # Score based on persona keywords
    if persona_type in persona_keywords:
        for keyword in persona_keywords[persona_type]:
            if keyword in text_lower:
                score += 0.1
    
    # Score based on job description keywords
    job_words = [word for word in job_lower.split() if len(word) > 3]
    for word in job_words:
        if word in text_lower:
            score += 0.2
    
    # Score based on persona terms
    persona_words = [word for word in persona_lower.split() if len(word) > 3]
    for word in persona_words:
        if word in text_lower:
            score += 0.15
    
    return min(score, 1.0)  # Cap at 1.0

def process_documents(config):
    """Main processing function"""
    documents = config.get('documents', [])
    persona = config.get('persona', '')
    job_description = config.get('job_to_be_done', '')
    
    print(f"Processing {len(documents)} documents for persona: {persona}")
    
    # Extract sections from all documents
    all_sections = []
    for doc_path in documents:
        if os.path.exists(doc_path):
            sections = extract_document_sections(doc_path)
            all_sections.extend(sections)
        else:
            print(f"Warning: Document not found: {doc_path}")
    
    if not all_sections:
        print("No sections extracted from documents")
        return create_empty_result(documents, persona, job_description)
    
    # Calculate relevance scores
    for section in all_sections:
        section['relevance_score'] = calculate_relevance(
            section['text'], persona, job_description
        )
    
    # Sort by relevance
    all_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    # Take top 20 sections
    top_sections = all_sections[:20]
    
    # Create extracted sections
    extracted_sections = []
    for i, section in enumerate(top_sections):
        extracted_sections.append({
            'document': section['document'],
            'page_number': section['page'],
            'section_title': section['section_title'],
            'importance_rank': i + 1
        })
    
    # Create subsection analysis
    subsection_analysis = []
    for section in top_sections[:10]:  # Top 10 for subsection analysis
        # Split into sentences
        sentences = [s.strip() for s in section['text'].split('.') if s.strip() and len(s.strip()) > 20]
        
        for sentence in sentences[:3]:  # Top 3 sentences per section
            subsection_analysis.append({
                'document': section['document'],
                'page_number': section['page'],
                'refined_text': sentence + ".",
                'relevance_score': section['relevance_score'] * 0.9  # Slightly lower than section score
            })
    
    # Create result
    result = {
        'metadata': {
            'input_documents': [os.path.basename(doc) for doc in documents],
            'persona': persona,
            'job_to_be_done': job_description,
            'processing_timestamp': datetime.now().isoformat()
        },
        'extracted_sections': extracted_sections,
        'subsection_analysis': subsection_analysis
    }
    
    return result

def create_empty_result(documents, persona, job_description):
    """Create empty result structure"""
    return {
        'metadata': {
            'input_documents': [os.path.basename(doc) for doc in documents],
            'persona': persona,
            'job_to_be_done': job_description,
            'processing_timestamp': datetime.now().isoformat()
        },
        'extracted_sections': [],
        'subsection_analysis': []
    }

def main():
    """Main execution function"""
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    # For local testing
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Look for configuration file
    config_file = os.path.join(input_dir, "config.json")
    
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        # Create default config with available PDFs
        pdf_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        config = {
            "documents": pdf_files,
            "persona": "General User",
            "job_to_be_done": "Analyze document content"
        }
        print(f"No config.json found, using default config with {len(pdf_files)} PDFs")
    
    # Process documents
    result = process_documents(config)
    
    # Save result
    output_file = os.path.join(output_dir, "challenge1b_output.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Processing complete! Results saved to {output_file}")
    print(f"Found {len(result['extracted_sections'])} relevant sections")

if __name__ == "__main__":
    main()
