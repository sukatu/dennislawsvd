#!/usr/bin/env python3
"""
Script to fix import statements in all model files
Changes 'from database import Base' to 'from backend.database import Base'
"""

import os
import glob

def fix_imports_in_file(file_path):
    """Fix import statements in a single file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace the import statement
        original_content = content
        content = content.replace('from database import Base', 'from backend.database import Base')
        
        # Only write if there were changes
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Fixed imports in: {file_path}")
            return True
        else:
            print(f"⏭️  No changes needed in: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all model files"""
    models_dir = "backend/models"
    
    if not os.path.exists(models_dir):
        print(f"❌ Models directory not found: {models_dir}")
        return
    
    # Find all Python files in models directory
    python_files = glob.glob(os.path.join(models_dir, "*.py"))
    
    print(f"🔍 Found {len(python_files)} Python files in {models_dir}")
    
    fixed_count = 0
    for file_path in python_files:
        # Skip __init__.py files
        if os.path.basename(file_path) == "__init__.py":
            continue
            
        if fix_imports_in_file(file_path):
            fixed_count += 1
    
    print(f"\n🎉 Fixed imports in {fixed_count} files!")
    print("✅ All model files now use 'from backend.database import Base'")

if __name__ == "__main__":
    main()
