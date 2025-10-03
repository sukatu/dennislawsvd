#!/usr/bin/env python3
"""
Script to analyze the Change of Date of Birth data from the correct sheet
"""

import pandas as pd
import sys
import os

def analyze_dob_data(file_path):
    """Analyze the Change of Date of Birth data"""
    try:
        # Read the specific sheet with the data
        df = pd.read_excel(file_path, sheet_name='GN172_Change of Date of Birth ')
        
        print("=== CHANGE OF DATE OF BIRTH DATA ANALYSIS ===")
        print(f"File: {file_path}")
        print(f"Sheet: GN172_Change of Date of Birth")
        print(f"Shape: {df.shape} (rows, columns)")
        print(f"Columns: {list(df.columns)}")
        
        print("\n=== COLUMN DETAILS ===")
        for col in df.columns:
            print(f"\nColumn: '{col}'")
            print(f"  Type: {df[col].dtype}")
            print(f"  Non-null count: {df[col].count()}")
            print(f"  Unique values: {df[col].nunique()}")
            if df[col].dtype == 'object':
                sample_values = df[col].dropna().head(5).tolist()
                print(f"  Sample values: {sample_values}")
        
        print("\n=== SAMPLE DATA (First 10 rows) ===")
        print(df.head(10).to_string())
        
        print("\n=== DATA SUMMARY ===")
        print(f"Total records: {len(df)}")
        print(f"Records with names: {df['Name of Person'].count()}")
        print(f"Records with old DOB: {df['Old Date of Birth'].count()}")
        print(f"Records with new DOB: {df['New Date of Birth'].count()}")
        print(f"Records with addresses: {df['Address'].count()}")
        print(f"Records with professions: {df['Profession'].count()}")
        
        # Check for patterns in the data
        print("\n=== DATA PATTERNS ===")
        if 'Name of Person' in df.columns:
            print(f"Name patterns:")
            names = df['Name of Person'].dropna()
            for name in names.head(10):
                print(f"  - {name}")
        
        if 'Old Date of Birth' in df.columns:
            print(f"\nOld DOB patterns:")
            old_dobs = df['Old Date of Birth'].dropna()
            for dob in old_dobs.head(10):
                print(f"  - {dob}")
        
        if 'New Date of Birth' in df.columns:
            print(f"\nNew DOB patterns:")
            new_dobs = df['New Date of Birth'].dropna()
            for dob in new_dobs.head(10):
                print(f"  - {dob}")
        
        return df
        
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return None

if __name__ == "__main__":
    file_path = "../Change of Date of Birth.xlsx"
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    df = analyze_dob_data(file_path)
    
    if df is not None:
        print(f"\n=== ANALYSIS COMPLETE ===")
        print(f"Total records: {len(df)}")
        print(f"Total columns: {len(df.columns)}")
