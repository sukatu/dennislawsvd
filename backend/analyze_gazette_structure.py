#!/usr/bin/env python3
"""
Analyze Gazette Structure
Analyzes the gazette directory structure and provides statistics
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def analyze_gazette_structure(gazettes_dir: str = "uploads/gazettes"):
    """Analyze the gazette directory structure"""
    
    if not os.path.exists(gazettes_dir):
        print(f"❌ Gazette directory not found: {gazettes_dir}")
        return
    
    print("🔍 ANALYZING GAZETTE STRUCTURE")
    print("=" * 50)
    
    year_stats = defaultdict(lambda: {'files': 0, 'size_mb': 0})
    total_files = 0
    total_size = 0
    
    # Analyze each year directory
    for year_dir in sorted(os.listdir(gazettes_dir)):
        year_path = os.path.join(gazettes_dir, year_dir)
        
        if not os.path.isdir(year_path):
            continue
            
        try:
            year = int(year_dir)
        except ValueError:
            continue
            
        # Count PDF files in this year
        pdf_files = []
        for file in os.listdir(year_path):
            if file.lower().endswith('.pdf'):
                pdf_files.append(file)
                file_path = os.path.join(year_path, file)
                file_size = os.path.getsize(file_path)
                year_stats[year]['files'] += 1
                year_stats[year]['size_mb'] += file_size / (1024 * 1024)
                total_files += 1
                total_size += file_size
        
        print(f"📅 {year}: {year_stats[year]['files']} files ({year_stats[year]['size_mb']:.1f} MB)")
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY STATISTICS")
    print("=" * 50)
    print(f"Total years: {len(year_stats)}")
    print(f"Total PDF files: {total_files}")
    print(f"Total size: {total_size / (1024 * 1024 * 1024):.2f} GB")
    
    # Find years with most files
    top_years = sorted(year_stats.items(), key=lambda x: x[1]['files'], reverse=True)[:10]
    print(f"\n🏆 TOP 10 YEARS BY FILE COUNT:")
    for year, stats in top_years:
        print(f"  {year}: {stats['files']} files ({stats['size_mb']:.1f} MB)")
    
    # Find years with most data
    top_years_size = sorted(year_stats.items(), key=lambda x: x[1]['size_mb'], reverse=True)[:10]
    print(f"\n💾 TOP 10 YEARS BY DATA SIZE:")
    for year, stats in top_years_size:
        print(f"  {year}: {stats['files']} files ({stats['size_mb']:.1f} MB)")
    
    return year_stats

def recommend_processing_strategy(year_stats):
    """Recommend processing strategy based on analysis"""
    
    print("\n" + "=" * 50)
    print("🎯 PROCESSING RECOMMENDATIONS")
    print("=" * 50)
    
    # Find years with good data density
    good_years = []
    for year, stats in year_stats.items():
        if stats['files'] >= 20:  # Years with substantial data
            good_years.append((year, stats['files']))
    
    good_years.sort(key=lambda x: x[1], reverse=True)
    
    print("✅ RECOMMENDED YEARS TO START WITH:")
    for year, file_count in good_years[:5]:
        print(f"  {year}: {file_count} files")
    
    print("\n📋 PROCESSING STRATEGY:")
    print("1. Start with recent years (2010-2021) - better OCR quality")
    print("2. Process high-volume years first")
    print("3. Test on 2-3 files per year before full processing")
    print("4. Monitor success rates and adjust patterns")
    
    return good_years

def main():
    """Main function"""
    year_stats = analyze_gazette_structure()
    
    if year_stats:
        good_years = recommend_processing_strategy(year_stats)
        
        print("\n" + "=" * 50)
        print("🚀 READY TO START PROCESSING")
        print("=" * 50)
        print("Next steps:")
        print("1. Run: python process_all_gazettes.py")
        print("2. Choose option 3 (limited files) for testing")
        print("3. Start with 5-10 files from recent years")
        print("4. Scale up based on success rates")

if __name__ == "__main__":
    main()
