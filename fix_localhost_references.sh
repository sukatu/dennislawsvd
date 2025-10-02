#!/bin/bash

# Fix all localhost:8000 references in src directory
echo "Fixing localhost:8000 references..."

# Find all files with localhost:8000 and replace them
find src -name "*.js" -type f -exec sed -i '' 's|http://localhost:8000|/api|g' {} \;

echo "Fixed localhost:8000 references in all JavaScript files"

# Also fix any remaining double /api/api/ patterns
find src -name "*.js" -type f -exec sed -i '' 's|/api/api/|/api/|g' {} \;

echo "Fixed double /api/api/ patterns"

echo "All localhost references have been fixed!"
