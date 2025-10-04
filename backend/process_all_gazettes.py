#!/usr/bin/env python3
"""
Process All Gazette PDFs
Comprehensive script to analyze all PDF gazette documents and extract structured data
"""

import os
import sys
import logging
from pathlib import Path
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from batch_pdf_processor import BatchPDFProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'gazette_processing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main processing function"""
    print("🚀 GAZETTE PDF PROCESSING SYSTEM")
    print("=" * 50)
    
    # Initialize processor
    processor = BatchPDFProcessor("uploads/gazettes")
    
    try:
        # Get user choice
        print("\nChoose processing option:")
        print("1. Process all PDF files")
        print("2. Process specific year")
        print("3. Process limited number of files (for testing)")
        print("4. Show statistics only")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            # Process all files
            print("\n🔄 Processing all PDF files...")
            result = processor.process_all_pdfs()
            
        elif choice == "2":
            # Process specific year
            year = input("Enter year (e.g., 2004): ").strip()
            print(f"\n🔄 Processing PDFs from year {year}...")
            result = processor.process_by_year(year)
            
        elif choice == "3":
            # Process limited files
            max_files = input("Enter maximum number of files to process: ").strip()
            try:
                max_files = int(max_files)
                print(f"\n🔄 Processing first {max_files} files...")
                result = processor.process_all_pdfs(max_files)
            except ValueError:
                print("Invalid number. Processing 10 files as default.")
                result = processor.process_all_pdfs(10)
                
        elif choice == "4":
            # Show statistics only
            print("\n📊 Current gazette statistics:")
            stats = processor.get_processing_stats()
            print(f"Total files found: {len(processor.find_pdf_files())}")
            print(f"Files already processed: {stats.get('total_files_processed', 0)}")
            return
            
        else:
            print("Invalid choice. Exiting.")
            return
        
        # Display results
        print("\n" + "=" * 60)
        print("PROCESSING COMPLETED")
        print("=" * 60)
        print(f"✅ Total files processed: {result['total_files']}")
        print(f"✅ Successful files: {result['successful_files']}")
        print(f"✅ Failed files: {result['total_files'] - result['successful_files']}")
        print(f"✅ Total entries extracted: {result['total_entries']}")
        print(f"✅ Total entries saved to database: {result['saved_entries']}")
        print(f"⏱️  Processing time: {result['processing_time']} seconds")
        
        if result['total_files'] > 0:
            success_rate = (result['successful_files'] / result['total_files']) * 100
            print(f"📈 Success rate: {success_rate:.1f}%")
        
        # Save detailed results
        results_file = f"gazette_processing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        processor.save_results_to_file(results_file)
        print(f"📄 Detailed results saved to: {results_file}")
        
        # Show next steps
        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("1. Check the gazette management interface in your web app")
        print("2. Review the processing log for any errors")
        print("3. Verify the extracted data in the database")
        print("4. Use the search functionality to find specific entries")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Processing interrupted by user")
        logger.info("Processing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        logger.error(f"Processing failed: {e}")
    finally:
        processor.close()

if __name__ == "__main__":
    main()
