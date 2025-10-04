#!/usr/bin/env python3
"""
Batch PDF Processor for Gazette Documents
Processes all PDF files in the gazettes directory and extracts gazette information
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.pdf_gazette_analyzer import PDFGazetteAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gazette_processing.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class BatchPDFProcessor:
    """Batch processor for PDF gazette documents"""
    
    def __init__(self, gazettes_dir: str = "uploads/gazettes"):
        self.gazettes_dir = gazettes_dir
        self.analyzer = PDFGazetteAnalyzer()
        self.results = []
        
    def find_pdf_files(self) -> List[str]:
        """Find all PDF files in the gazettes directory"""
        pdf_files = []
        
        if not os.path.exists(self.gazettes_dir):
            logger.error(f"Gazettes directory not found: {self.gazettes_dir}")
            return pdf_files
        
        for root, dirs, files in os.walk(self.gazettes_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        return pdf_files
    
    def process_all_pdfs(self, max_files: int = None) -> Dict:
        """Process all PDF files and return summary"""
        start_time = time.time()
        
        # Find all PDF files
        pdf_files = self.find_pdf_files()
        
        if not pdf_files:
            return {
                'success': False,
                'message': 'No PDF files found',
                'total_files': 0,
                'processed_files': 0,
                'successful_files': 0,
                'total_entries': 0,
                'saved_entries': 0,
                'processing_time': 0
            }
        
        # Limit files if specified
        if max_files:
            pdf_files = pdf_files[:max_files]
            logger.info(f"Processing first {max_files} files")
        
        # Process each PDF
        successful_files = 0
        total_entries = 0
        saved_entries = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"Processing file {i}/{len(pdf_files)}: {os.path.basename(pdf_file)}")
            
            try:
                result = self.analyzer.process_pdf_file(pdf_file)
                self.results.append(result)
                
                if result['success']:
                    successful_files += 1
                    total_entries += result['entries_processed']
                    saved_entries += result['entries_saved']
                    logger.info(f"✓ {result['message']}")
                else:
                    logger.warning(f"✗ {result['message']}")
                    
            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {e}")
                self.results.append({
                    'file_path': pdf_file,
                    'success': False,
                    'message': f'Exception: {str(e)}',
                    'entries_processed': 0,
                    'entries_saved': 0
                })
        
        processing_time = time.time() - start_time
        
        summary = {
            'success': True,
            'message': f'Batch processing completed',
            'total_files': len(pdf_files),
            'processed_files': len(self.results),
            'successful_files': successful_files,
            'total_entries': total_entries,
            'saved_entries': saved_entries,
            'processing_time': round(processing_time, 2)
        }
        
        logger.info(f"Batch processing completed in {processing_time:.2f} seconds")
        logger.info(f"Summary: {summary}")
        
        return summary
    
    def process_by_year(self, year: str) -> Dict:
        """Process PDFs from a specific year"""
        year_dir = os.path.join(self.gazettes_dir, year)
        
        if not os.path.exists(year_dir):
            logger.error(f"Year directory not found: {year_dir}")
            return {
                'success': False,
                'message': f'Year directory not found: {year_dir}',
                'total_files': 0,
                'processed_files': 0,
                'successful_files': 0,
                'total_entries': 0,
                'saved_entries': 0,
                'processing_time': 0
            }
        
        # Temporarily change gazettes_dir to year directory
        original_dir = self.gazettes_dir
        self.gazettes_dir = year_dir
        
        try:
            result = self.process_all_pdfs()
            result['year'] = year
            return result
        finally:
            self.gazettes_dir = original_dir
    
    def get_processing_stats(self) -> Dict:
        """Get detailed processing statistics"""
        if not self.results:
            return {'message': 'No processing results available'}
        
        successful_results = [r for r in self.results if r['success']]
        failed_results = [r for r in self.results if not r['success']]
        
        # Group by gazette type
        gazette_types = {}
        for result in successful_results:
            # This would need to be enhanced to track gazette types
            pass
        
        return {
            'total_files_processed': len(self.results),
            'successful_files': len(successful_results),
            'failed_files': len(failed_results),
            'success_rate': round(len(successful_results) / len(self.results) * 100, 2),
            'total_entries_extracted': sum(r['entries_processed'] for r in successful_results),
            'total_entries_saved': sum(r['entries_saved'] for r in successful_results),
            'failed_files_details': [{'file': r['file_path'], 'error': r['message']} for r in failed_results]
        }
    
    def save_results_to_file(self, filename: str = "gazette_processing_results.json"):
        """Save processing results to JSON file"""
        import json
        
        results_data = {
            'processing_summary': self.get_processing_stats(),
            'detailed_results': self.results,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        logger.info(f"Results saved to {filename}")
    
    def close(self):
        """Close analyzer and cleanup"""
        if hasattr(self, 'analyzer'):
            self.analyzer.close()

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch process PDF gazette documents')
    parser.add_argument('--gazettes-dir', default='uploads/gazettes', help='Directory containing PDF files')
    parser.add_argument('--max-files', type=int, help='Maximum number of files to process')
    parser.add_argument('--year', help='Process only files from specific year')
    parser.add_argument('--output', default='gazette_processing_results.json', help='Output file for results')
    
    args = parser.parse_args()
    
    # Create processor
    processor = BatchPDFProcessor(args.gazettes_dir)
    
    try:
        if args.year:
            # Process specific year
            logger.info(f"Processing PDFs from year: {args.year}")
            result = processor.process_by_year(args.year)
        else:
            # Process all PDFs
            logger.info("Processing all PDF files")
            result = processor.process_all_pdfs(args.max_files)
        
        # Print summary
        print("\n" + "="*50)
        print("PROCESSING SUMMARY")
        print("="*50)
        print(f"Total files: {result['total_files']}")
        print(f"Processed files: {result['processed_files']}")
        print(f"Successful files: {result['successful_files']}")
        print(f"Total entries extracted: {result['total_entries']}")
        print(f"Total entries saved: {result['saved_entries']}")
        print(f"Processing time: {result['processing_time']} seconds")
        print("="*50)
        
        # Save results
        processor.save_results_to_file(args.output)
        
        # Print detailed stats
        stats = processor.get_processing_stats()
        print(f"\nSuccess rate: {stats['success_rate']}%")
        
        if stats['failed_files'] > 0:
            print(f"\nFailed files ({stats['failed_files']}):")
            for failed in stats['failed_files_details'][:5]:  # Show first 5
                print(f"  - {os.path.basename(failed['file'])}: {failed['error']}")
            if stats['failed_files'] > 5:
                print(f"  ... and {stats['failed_files'] - 5} more")
        
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
    except Exception as e:
        logger.error(f"Processing failed: {e}")
    finally:
        processor.close()

if __name__ == "__main__":
    main()
