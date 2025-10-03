#!/usr/bin/env python3
"""
Test the on-demand AI analysis functionality.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from services.on_demand_ai_analysis import analyze_case_if_needed

def test_on_demand_analysis():
    """Test on-demand analysis for a specific case"""
    case_id = 10487  # Use the case we tested earlier
    
    print(f"Testing on-demand analysis for case {case_id}")
    print("=" * 50)
    
    result = analyze_case_if_needed(case_id)
    
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    
    if 'analysis' in result:
        print(f"Analysis: {result['analysis']}")
    
    if 'generated_at' in result:
        print(f"Generated at: {result['generated_at']}")
    
    print("=" * 50)
    return result

if __name__ == "__main__":
    test_on_demand_analysis()
