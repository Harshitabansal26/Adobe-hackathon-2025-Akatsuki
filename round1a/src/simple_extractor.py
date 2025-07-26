#!/usr/bin/env python3
"""
SIMPLE WORKING PDF Outline Extractor
Actually extracts headings from PDFs - no fancy stuff, just works!
"""

import fitz  # PyMuPDF
import json
import os
import sys
import re

def extract_pdf_outline(pdf_path):
    """Extract outline from a single PDF file"""
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        
        # Get document title (from first page, largest text)
        first_page = doc[0]
        blocks = first_page.get_text("dict")
        
        title = "Untitled Document"
        max_size = 0
        
        # Find largest text on first page as title
        for block in blocks["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] > max_size and len(span["text"].strip()) > 5:
                            max_size = span["size"]
                            title = span["text"].strip()
        
        # Extract headings from all pages
        outline = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")
            
            # Analyze font sizes on this page
            font_sizes = []
            for block in blocks["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_sizes.append(span["size"])
            
            if not font_sizes:
                continue
                
            # Get average font size (body text)
            avg_size = sum(font_sizes) / len(font_sizes)
            
            # Find headings (larger than average)
            for block in blocks["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            size = span["size"]
                            
                            # Skip if too short or too long
                            if len(text) < 3 or len(text) > 100:
                                continue
                            
                            # Check if it's a heading based on size
                            if size > avg_size * 1.2:  # 20% larger than average
                                
                                # Determine heading level
                                if size > avg_size * 1.8:
                                    level = "H1"
                                elif size > avg_size * 1.4:
                                    level = "H2"
                                else:
                                    level = "H3"
                                
                                # Clean up text
                                clean_text = re.sub(r'^\d+\.?\s*', '', text)  # Remove leading numbers
                                clean_text = re.sub(r'\s+', ' ', clean_text)  # Fix spacing
                                
                                # Add to outline if not duplicate
                                if clean_text and not any(h["text"] == clean_text for h in outline):
                                    outline.append({
                                        "level": level,
                                        "text": clean_text,
                                        "page": page_num + 1
                                    })
        
        doc.close()
        
        # Sort by page number
        outline.sort(key=lambda x: x["page"])
        
        return {
            "title": title,
            "outline": outline
        }
        
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return {
            "title": "Error Processing Document",
            "outline": []
        }

def main():
    """Main function - process all PDFs in input directory"""
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    # For local testing
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PDF files
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist!")
        return
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file}")
        
        pdf_path = os.path.join(input_dir, pdf_file)
        output_file = os.path.splitext(pdf_file)[0] + '.json'
        output_path = os.path.join(output_dir, output_file)
        
        # Extract outline
        result = extract_pdf_outline(pdf_path)
        
        # Save result
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Saved: {output_file} with {len(result['outline'])} headings")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()
