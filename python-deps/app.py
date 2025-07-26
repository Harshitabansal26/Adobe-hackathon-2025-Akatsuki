#!/usr/bin/env python3
"""
WORKING Web Application for Adobe Hackathon
Actually processes PDFs through a web interface
"""

from flask import Flask, request, render_template, jsonify, send_file
import os
import json
import tempfile
import zipfile
from werkzeug.utils import secure_filename
import sys
sys.path.append('round1a/src')
sys.path.append('round1b/src')

from simple_extractor import extract_pdf_outline
from simple_persona import extract_document_sections, calculate_relevance, process_documents

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('webapp.html')

@app.route('/extract-outline', methods=['POST'])
def extract_outline():
    """Round 1A: Extract PDF outline"""
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file uploaded'}), 400
        
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Please upload a PDF file'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract outline
        result = extract_pdf_outline(filepath)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/persona-analysis', methods=['POST'])
def persona_analysis():
    """Round 1B: Persona-driven analysis"""
    try:
        # Get form data
        persona = request.form.get('persona', '')
        job_description = request.form.get('job_description', '')
        
        if not persona or not job_description:
            return jsonify({'error': 'Please provide both persona and job description'}), 400
        
        # Get uploaded files
        files = request.files.getlist('pdfs')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'Please upload at least one PDF file'}), 400
        
        # Save uploaded files
        uploaded_paths = []
        for file in files:
            if file.filename and file.filename.lower().endswith('.pdf'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                uploaded_paths.append(filepath)
        
        if not uploaded_paths:
            return jsonify({'error': 'No valid PDF files uploaded'}), 400
        
        # Create config
        config = {
            'documents': uploaded_paths,
            'persona': persona,
            'job_to_be_done': job_description
        }
        
        # Process documents
        result = process_documents(config)
        
        # Clean up
        for filepath in uploaded_paths:
            if os.path.exists(filepath):
                os.remove(filepath)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Adobe Hackathon PDF Processor is running!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
