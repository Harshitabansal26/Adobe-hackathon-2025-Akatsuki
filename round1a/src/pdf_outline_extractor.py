#!/usr/bin/env python3
"""
PDF Outline Extractor for Adobe Hackathon Challenge
WORKING VERSION - Extracts structured outlines (Title, H1, H2, H3) from PDF documents
"""

import fitz  # PyMuPDF
import json
import re
import os
import sys
from collections import Counter
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFOutlineExtractor:
    def __init__(self):
        # Simple patterns that actually work
        self.heading_patterns = [
            r'^\d+\.?\s+[A-Z]',      # 1. Introduction, 2 Methods
            r'^[A-Z][A-Z\s]{3,}$',   # ALL CAPS headings
            r'^\d+\.\d+\.?\s+',      # 1.1, 1.2 sections
            r'^Chapter\s+\d+',       # Chapter 1, Chapter 2
            r'^Section\s+\d+',       # Section 1, Section 2
        ]
        
    def extract_text_with_formatting(self, doc: fitz.Document) -> List[Dict]:
        """Extract text with formatting information from PDF"""
        text_blocks = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")
            
            for block in blocks["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                text_blocks.append({
                                    "text": text,
                                    "page": page_num + 1,
                                    "font": span["font"],
                                    "size": span["size"],
                                    "flags": span["flags"],
                                    "bbox": span["bbox"],
                                    "color": span.get("color", 0)
                                })
        
        return text_blocks
    
    def analyze_font_hierarchy(self, text_blocks: List[Dict]) -> Dict[str, int]:
        """Analyze font sizes to determine heading hierarchy"""
        font_sizes = [block["size"] for block in text_blocks]
        size_counter = Counter(font_sizes)
        
        # Get most common sizes (likely body text)
        common_sizes = size_counter.most_common(5)
        body_size = common_sizes[0][0] if common_sizes else 12
        
        # Create hierarchy based on font sizes
        unique_sizes = sorted(set(font_sizes), reverse=True)
        hierarchy = {}
        
        for i, size in enumerate(unique_sizes):
            if size > body_size * 1.2:  # Significantly larger than body
                if i == 0:
                    hierarchy[size] = "title"
                elif i == 1:
                    hierarchy[size] = "H1"
                elif i == 2:
                    hierarchy[size] = "H2"
                elif i == 3:
                    hierarchy[size] = "H3"
        
        return hierarchy
    
    def is_likely_heading(self, text: str, font_size: float, flags: int, body_size: float) -> Optional[str]:
        """Determine if text is likely a heading and its level"""
        text_clean = text.strip()
        
        # Skip very short or very long text
        if len(text_clean) < 3 or len(text_clean) > 200:
            return None
            
        # Check for heading patterns
        for pattern in self.compiled_patterns:
            if pattern.match(text_clean):
                # Determine level based on font size and pattern
                if font_size > body_size * 1.8:
                    return "H1"
                elif font_size > body_size * 1.4:
                    return "H2"
                else:
                    return "H3"
        
        # Check font properties
        is_bold = bool(flags & 2**4)  # Bold flag
        size_ratio = font_size / body_size
        
        if size_ratio > 1.8 and (is_bold or text_clean.isupper()):
            return "H1"
        elif size_ratio > 1.4 and is_bold:
            return "H2"
        elif size_ratio > 1.2 and (is_bold or self._has_heading_characteristics(text_clean)):
            return "H3"
            
        return None
    
    def _has_heading_characteristics(self, text: str) -> bool:
        """Check if text has characteristics of a heading"""
        # Starts with capital letter
        if not text[0].isupper():
            return False
            
        # Contains mostly title case words
        words = text.split()
        title_case_count = sum(1 for word in words if word[0].isupper())
        
        return title_case_count / len(words) > 0.6
    
    def extract_title(self, text_blocks: List[Dict]) -> str:
        """Extract document title from first page"""
        first_page_blocks = [block for block in text_blocks if block["page"] == 1]
        
        if not first_page_blocks:
            return "Untitled Document"
        
        # Sort by font size (descending) and position (top first)
        first_page_blocks.sort(key=lambda x: (-x["size"], x["bbox"][1]))
        
        # Look for the largest text in the upper portion of the first page
        for block in first_page_blocks[:10]:  # Check first 10 blocks
            text = block["text"].strip()
            if len(text) > 5 and len(text) < 150:  # Reasonable title length
                # Skip common non-title text
                skip_patterns = [
                    r'^\d+$',  # Just numbers
                    r'^page\s+\d+',  # Page numbers
                    r'^chapter\s+\d+$',  # Just "Chapter X"
                    r'^\w+\s+\d{4}$',  # Just "Month Year"
                ]
                
                if not any(re.match(pattern, text, re.IGNORECASE) for pattern in skip_patterns):
                    return text
        
        return "Untitled Document"
    
    def extract_outline(self, pdf_path: str) -> Dict:
        """Main method to extract outline from PDF"""
        try:
            doc = fitz.open(pdf_path)
            logger.info(f"Processing PDF: {pdf_path} ({len(doc)} pages)")
            
            # Extract text with formatting
            text_blocks = self.extract_text_with_formatting(doc)
            
            if not text_blocks:
                logger.warning("No text found in PDF")
                return {"title": "Empty Document", "outline": []}
            
            # Analyze font hierarchy
            font_sizes = [block["size"] for block in text_blocks]
            body_size = Counter(font_sizes).most_common(1)[0][0]
            
            # Extract title
            title = self.extract_title(text_blocks)
            
            # Extract headings
            outline = []
            seen_headings = set()  # Avoid duplicates
            
            for block in text_blocks:
                heading_level = self.is_likely_heading(
                    block["text"], 
                    block["size"], 
                    block["flags"], 
                    body_size
                )
                
                if heading_level:
                    text = block["text"].strip()
                    # Clean up the heading text
                    text = re.sub(r'^\d+\.?\s*', '', text)  # Remove leading numbers
                    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
                    
                    # Avoid duplicates and very similar headings
                    text_key = text.lower()
                    if text_key not in seen_headings and len(text) > 3:
                        seen_headings.add(text_key)
                        outline.append({
                            "level": heading_level,
                            "text": text,
                            "page": block["page"]
                        })
            
            doc.close()
            
            # Sort outline by page number
            outline.sort(key=lambda x: x["page"])
            
            logger.info(f"Extracted {len(outline)} headings from {pdf_path}")
            return {
                "title": title,
                "outline": outline
            }
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}")
            return {"title": "Error Processing Document", "outline": []}

def process_pdfs(input_dir: str, output_dir: str):
    """Process all PDFs in input directory and save results to output directory"""
    extractor = PDFOutlineExtractor()
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all PDF files
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir}")
        return
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        output_file = os.path.splitext(pdf_file)[0] + '.json'
        output_path = os.path.join(output_dir, output_file)
        
        logger.info(f"Processing: {pdf_file}")
        
        # Extract outline
        result = extractor.extract_outline(pdf_path)
        
        # Save result
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved: {output_file}")

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    process_pdfs(input_dir, output_dir)
