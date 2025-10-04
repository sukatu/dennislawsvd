#!/usr/bin/env python3
"""
Test script for PDF Gazette Analysis
Tests the PDF analysis on a few sample files
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.pdf_gazette_analyzer import PDFGazetteAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_single_pdf(file_path: str):
    """Test analysis on a single PDF file"""
    try:
        logger.info(f"Testing PDF analysis on: {file_path}")
        
        analyzer = PDFGazetteAnalyzer()
        result = analyzer.process_pdf_file(file_path)
        
        print(f"\n{'='*60}")
        print(f"ANALYSIS RESULT FOR: {os.path.basename(file_path)}")
        print(f"{'='*60}")
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")
        print(f"Entries Processed: {result['entries_processed']}")
        print(f"Entries Saved: {result['entries_saved']}")
        print(f"{'='*60}")
        
        analyzer.close()
        return result
        
    except Exception as e:
        logger.error(f"Error testing PDF {file_path}: {e}")
        return None

def test_multiple_pdfs(gazettes_dir: str = "uploads/gazettes", max_files: int = 3):
    """Test analysis on multiple PDF files"""
    try:
        logger.info(f"Testing PDF analysis on files in: {gazettes_dir}")
        
        # Find PDF files
        pdf_files = []
        if os.path.exists(gazettes_dir):
            for root, dirs, files in os.walk(gazettes_dir):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {gazettes_dir}")
            return
        
        # Test first few files
        test_files = pdf_files[:max_files]
        logger.info(f"Testing {len(test_files)} files out of {len(pdf_files)} found")
        
        results = []
        for i, pdf_file in enumerate(test_files, 1):
            print(f"\n{'='*80}")
            print(f"TESTING FILE {i}/{len(test_files)}: {os.path.basename(pdf_file)}")
            print(f"{'='*80}")
            
            result = test_single_pdf(pdf_file)
            if result:
                results.append(result)
        
        # Summary
        print(f"\n{'='*80}")
        print("TEST SUMMARY")
        print(f"{'='*80}")
        successful = [r for r in results if r['success']]
        total_entries = sum(r['entries_processed'] for r in successful)
        total_saved = sum(r['entries_saved'] for r in successful)
        
        print(f"Files tested: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(results) - len(successful)}")
        print(f"Total entries extracted: {total_entries}")
        print(f"Total entries saved: {total_saved}")
        print(f"{'='*80}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error in batch testing: {e}")
        return []

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test PDF gazette analysis')
    parser.add_argument('--file', help='Test specific PDF file')
    parser.add_argument('--gazettes-dir', default='uploads/gazettes', help='Directory containing PDF files')
    parser.add_argument('--max-files', type=int, default=3, help='Maximum number of files to test')
    
    args = parser.parse_args()
    
    if args.file:
        # Test single file
        if os.path.exists(args.file):
            test_single_pdf(args.file)
        else:
            logger.error(f"File not found: {args.file}")
    else:
        # Test multiple files
        test_multiple_pdfs(args.gazettes_dir, args.max_files)

if __name__ == "__main__":
    main()
