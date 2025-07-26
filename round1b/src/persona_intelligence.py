#!/usr/bin/env python3
"""
Persona-Driven Document Intelligence for Adobe Hackathon Challenge
Extracts and prioritizes relevant sections based on persona and job-to-be-done
"""

import fitz  # PyMuPDF
import json
import os
import sys
import re
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class PersonaIntelligence:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        # Persona-specific keywords for different roles
        self.persona_keywords = {
            'researcher': ['methodology', 'analysis', 'study', 'research', 'findings', 'results', 'conclusion', 'hypothesis', 'experiment', 'data', 'statistical', 'significant'],
            'student': ['definition', 'concept', 'example', 'explanation', 'summary', 'key points', 'important', 'fundamental', 'basic', 'introduction', 'overview'],
            'analyst': ['trend', 'performance', 'metrics', 'analysis', 'comparison', 'evaluation', 'assessment', 'financial', 'revenue', 'growth', 'market'],
            'manager': ['strategy', 'planning', 'implementation', 'objectives', 'goals', 'management', 'leadership', 'decision', 'process', 'framework'],
            'developer': ['implementation', 'code', 'algorithm', 'technical', 'system', 'architecture', 'design', 'specification', 'requirements', 'solution']
        }
        
    def extract_document_sections(self, pdf_path: str) -> List[Dict]:
        """Extract sections from PDF with text and metadata"""
        try:
            doc = fitz.open(pdf_path)
            sections = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                if text.strip():
                    # Split into paragraphs
                    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                    
                    for i, paragraph in enumerate(paragraphs):
                        if len(paragraph) > 50:  # Filter out very short paragraphs
                            sections.append({
                                'document': os.path.basename(pdf_path),
                                'page': page_num + 1,
                                'section_id': f"{os.path.basename(pdf_path)}_p{page_num + 1}_s{i + 1}",
                                'text': paragraph,
                                'word_count': len(paragraph.split())
                            })
            
            doc.close()
            return sections
            
        except Exception as e:
            logger.error(f"Error extracting sections from {pdf_path}: {str(e)}")
            return []
    
    def identify_section_titles(self, sections: List[Dict]) -> List[Dict]:
        """Identify likely section titles based on formatting and content"""
        for section in sections:
            text = section['text']
            
            # Heuristics for section titles
            is_title = False
            title = "Content Section"
            
            # Check if it's a short line that could be a heading
            lines = text.split('\n')
            first_line = lines[0].strip()
            
            if len(lines) == 1 and len(first_line) < 100:
                # Single line, not too long - likely a heading
                is_title = True
                title = first_line
            elif len(first_line) < 80 and first_line.endswith(':'):
                # Short line ending with colon
                is_title = True
                title = first_line.rstrip(':')
            elif re.match(r'^\d+\.?\s+[A-Z]', first_line):
                # Numbered heading
                is_title = True
                title = first_line
            elif first_line.isupper() and len(first_line) < 50:
                # All caps short line
                is_title = True
                title = first_line.title()
            else:
                # Extract first sentence as title
                sentences = sent_tokenize(text)
                if sentences:
                    title = sentences[0][:100] + "..." if len(sentences[0]) > 100 else sentences[0]
            
            section['section_title'] = title
            section['is_heading'] = is_title
            
        return sections
    
    def calculate_persona_relevance(self, text: str, persona: str, job_description: str) -> float:
        """Calculate relevance score based on persona and job description"""
        text_lower = text.lower()
        persona_lower = persona.lower()
        job_lower = job_description.lower()
        
        score = 0.0
        
        # Base relevance from persona keywords
        persona_type = self._identify_persona_type(persona_lower)
        if persona_type in self.persona_keywords:
            keywords = self.persona_keywords[persona_type]
            keyword_matches = sum(1 for keyword in keywords if keyword in text_lower)
            score += keyword_matches * 0.1
        
        # Job-specific keywords
        job_words = [word for word in word_tokenize(job_lower) if word not in self.stop_words and len(word) > 3]
        job_matches = sum(1 for word in job_words if word in text_lower)
        score += job_matches * 0.2
        
        # Persona-specific terms
        persona_words = [word for word in word_tokenize(persona_lower) if word not in self.stop_words and len(word) > 3]
        persona_matches = sum(1 for word in persona_words if word in text_lower)
        score += persona_matches * 0.15
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _identify_persona_type(self, persona: str) -> str:
        """Identify persona type from description"""
        persona_mappings = {
            'researcher': ['researcher', 'scientist', 'academic', 'phd'],
            'student': ['student', 'undergraduate', 'graduate', 'learner'],
            'analyst': ['analyst', 'investment', 'financial', 'business'],
            'manager': ['manager', 'director', 'executive', 'leader'],
            'developer': ['developer', 'engineer', 'programmer', 'technical']
        }
        
        for persona_type, keywords in persona_mappings.items():
            if any(keyword in persona for keyword in keywords):
                return persona_type
        
        return 'general'
    
    def rank_sections(self, sections: List[Dict], persona: str, job_description: str) -> List[Dict]:
        """Rank sections based on relevance to persona and job"""
        # Calculate relevance scores
        for section in sections:
            relevance_score = self.calculate_persona_relevance(
                section['text'], persona, job_description
            )
            section['relevance_score'] = relevance_score
        
        # Sort by relevance score (descending)
        sections.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Assign importance ranks
        for i, section in enumerate(sections):
            section['importance_rank'] = i + 1
        
        return sections
    
    def extract_subsections(self, section_text: str, max_subsections: int = 3) -> List[Dict]:
        """Extract relevant subsections from a section"""
        sentences = sent_tokenize(section_text)
        
        if len(sentences) <= max_subsections:
            # If few sentences, return all as subsections
            return [
                {
                    'refined_text': sentence.strip(),
                    'relevance_score': 0.8 - (i * 0.1)  # Decreasing relevance
                }
                for i, sentence in enumerate(sentences)
            ]
        
        # For longer sections, extract key sentences
        subsections = []
        
        # First sentence (often contains key information)
        if sentences:
            subsections.append({
                'refined_text': sentences[0].strip(),
                'relevance_score': 0.9
            })
        
        # Middle sentences with key terms
        middle_sentences = sentences[1:-1] if len(sentences) > 2 else []
        key_sentences = []
        
        for sentence in middle_sentences:
            # Score based on presence of important terms
            score = 0.0
            sentence_lower = sentence.lower()
            
            # Look for conclusion/summary indicators
            if any(indicator in sentence_lower for indicator in ['therefore', 'thus', 'in conclusion', 'importantly', 'significant']):
                score += 0.3
            
            # Look for quantitative information
            if re.search(r'\d+%|\d+\.\d+|significant|increase|decrease', sentence_lower):
                score += 0.2
            
            key_sentences.append((sentence, score))
        
        # Sort by score and take top sentences
        key_sentences.sort(key=lambda x: x[1], reverse=True)
        
        for sentence, score in key_sentences[:max_subsections-1]:
            subsections.append({
                'refined_text': sentence.strip(),
                'relevance_score': 0.7 + score
            })
        
        return subsections[:max_subsections]
    
    def process_documents(self, input_config: Dict) -> Dict:
        """Main processing function"""
        documents = input_config.get('documents', [])
        persona = input_config.get('persona', '')
        job_description = input_config.get('job_to_be_done', '')
        
        logger.info(f"Processing {len(documents)} documents for persona: {persona}")
        
        # Extract sections from all documents
        all_sections = []
        for doc_path in documents:
            if os.path.exists(doc_path):
                sections = self.extract_document_sections(doc_path)
                sections = self.identify_section_titles(sections)
                all_sections.extend(sections)
            else:
                logger.warning(f"Document not found: {doc_path}")
        
        if not all_sections:
            logger.warning("No sections extracted from documents")
            return self._create_empty_result(documents, persona, job_description)
        
        # Rank sections by relevance
        ranked_sections = self.rank_sections(all_sections, persona, job_description)
        
        # Take top sections (limit to prevent overwhelming output)
        top_sections = ranked_sections[:20]  # Top 20 sections
        
        # Process sections for output
        extracted_sections = []
        subsection_analysis = []
        
        for section in top_sections:
            # Add to extracted sections
            extracted_sections.append({
                'document': section['document'],
                'page_number': section['page'],
                'section_title': section['section_title'],
                'importance_rank': section['importance_rank']
            })
            
            # Extract subsections
            subsections = self.extract_subsections(section['text'])
            
            for subsection in subsections:
                subsection_analysis.append({
                    'document': section['document'],
                    'page_number': section['page'],
                    'refined_text': subsection['refined_text'],
                    'relevance_score': subsection['relevance_score']
                })
        
        # Create final result
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
    
    def _create_empty_result(self, documents: List[str], persona: str, job_description: str) -> Dict:
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
    
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Look for input configuration file
    config_file = os.path.join(input_dir, "config.json")
    
    if not os.path.exists(config_file):
        logger.error(f"Configuration file not found: {config_file}")
        # Create a sample config for testing
        sample_config = {
            "documents": [],
            "persona": "Sample Persona",
            "job_to_be_done": "Sample job description"
        }
        
        # Find PDF files in input directory
        pdf_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        sample_config["documents"] = pdf_files
        
        if pdf_files:
            logger.info(f"Found {len(pdf_files)} PDF files, processing with default configuration")
        else:
            logger.error("No PDF files found in input directory")
            return
    else:
        with open(config_file, 'r', encoding='utf-8') as f:
            sample_config = json.load(f)
    
    # Initialize processor
    processor = PersonaIntelligence()
    
    # Process documents
    result = processor.process_documents(sample_config)
    
    # Save result
    output_file = os.path.join(output_dir, "challenge1b_output.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Processing complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
