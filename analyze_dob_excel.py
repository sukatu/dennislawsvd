#!/usr/bin/env python3
"""
Script to analyze the Change of Date of Birth Excel file structure
"""

import pandas as pd
import sys
import os

def analyze_excel_file(file_path):
    """Analyze the Excel file structure and content"""
    try:
        # Read the Excel file with different parameters
        print("Trying different sheet reading approaches...")
        
        # Try reading all sheets
        xl_file = pd.ExcelFile(file_path)
        print(f"Available sheets: {xl_file.sheet_names}")
        
        # Try reading with different header rows
        for sheet_name in xl_file.sheet_names:
            print(f"\n=== SHEET: {sheet_name} ===")
            for header_row in [0, 1, 2, 3, 4, 5]:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
                    if not df.empty and len(df.columns) > 1:
                        print(f"Header row {header_row}: {df.shape} - {list(df.columns)}")
                        if header_row == 0:  # Show first sheet with first header
                            break
                except:
                    continue
        
        # Read the main sheet
        df = pd.read_excel(file_path)
        
        print("=== EXCEL FILE ANALYSIS ===")
        print(f"File: {file_path}")
        print(f"Shape: {df.shape} (rows, columns)")
        print(f"Columns: {list(df.columns)}")
        print("\n=== COLUMN DETAILS ===")
        
        for col in df.columns:
            print(f"\nColumn: '{col}'")
            print(f"  Type: {df[col].dtype}")
            print(f"  Non-null count: {df[col].count()}")
            print(f"  Unique values: {df[col].nunique()}")
            if df[col].dtype == 'object':
                print(f"  Sample values: {df[col].dropna().head(3).tolist()}")
        
        print("\n=== SAMPLE DATA (First 5 rows) ===")
        print(df.head().to_string())
        
        print("\n=== DATA TYPES ===")
        print(df.dtypes)
        
        return df
        
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return None

if __name__ == "__main__":
    file_path = "../Change of Date of Birth.xlsx"
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    df = analyze_excel_file(file_path)
    
    if df is not None:
        print(f"\n=== ANALYSIS COMPLETE ===")
        print(f"Total records: {len(df)}")
        print(f"Total columns: {len(df.columns)}")
