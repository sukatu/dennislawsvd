# AI Case Analysis System

This system automatically generates AI-powered analysis for legal cases, providing structured insights for banking and financial assessment purposes.

## Features

- **Financial Impact Assessment**: Analyzes cases for HIGH/MODERATE/LOW financial implications
- **Case Outcome Determination**: Identifies whether cases were WON/LOST/PARTIALLY_WON/PARTIALLY_LOST/UNRESOLVED
- **Court Orders Extraction**: Extracts specific court orders, judgments, and directives
- **Detailed Outcome Summary**: Provides comprehensive case summaries focused on banking and credit assessment

## Database Fields

The system populates the following fields in the `reported_cases` table:

- `ai_case_outcome` (Text): Case outcome (WON/LOST/PARTIALLY_WON/PARTIALLY_LOST/UNRESOLVED)
- `ai_court_orders` (Text): Detailed court orders and directives
- `ai_financial_impact` (Text): Financial impact assessment with explanation
- `ai_detailed_outcome` (Text): Comprehensive case summary
- `ai_summary_generated_at` (DateTime): Timestamp when analysis was generated
- `ai_summary_version` (String): Version of the AI analysis algorithm

## Setup

### 1. OpenAI Configuration

Set your OpenAI API key in one of these ways:

**Option A: Environment Variable**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

**Option B: Database Settings**
```python
# Add to database settings table
INSERT INTO settings (key, value) VALUES ('openai_api_key', 'your-openai-api-key-here');
INSERT INTO settings (key, value) VALUES ('openai_model', 'gpt-3.5-turbo');
```

### 2. Install Dependencies

```bash
pip install openai
```

## Usage

### 1. Test the System

```bash
python test_ai_analysis.py
```

### 2. Process All Cases

```bash
# Interactive mode (asks for confirmation)
python backend/migrate_ai_analysis.py

# Force mode (no confirmation)
python backend/migrate_ai_analysis.py --force
```

### 3. API Endpoints

#### Analyze Single Case
```bash
POST /api/ai-case-analysis/analyze-case/{case_id}
```

#### Analyze All Cases (Background)
```bash
POST /api/ai-case-analysis/analyze-all-cases?batch_size=10
```

#### Get Analysis Statistics
```bash
GET /api/ai-case-analysis/stats
```

#### Get Case Analysis
```bash
GET /api/ai-case-analysis/case/{case_id}/analysis
```

#### Reset Case Analysis
```bash
POST /api/ai-case-analysis/reset-case/{case_id}
```

## API Examples

### Analyze a Single Case

```bash
curl -X POST "http://localhost:8000/api/ai-case-analysis/analyze-case/123" \
  -H "Authorization: Bearer your-token"
```

### Get Analysis Statistics

```bash
curl -X GET "http://localhost:8000/api/ai-case-analysis/stats" \
  -H "Authorization: Bearer your-token"
```

Response:
```json
{
  "total_cases": 1500,
  "analyzed_cases": 1200,
  "pending_cases": 300,
  "completion_percentage": 80.0
}
```

### Get Case Analysis

```bash
curl -X GET "http://localhost:8000/api/ai-case-analysis/case/123/analysis" \
  -H "Authorization: Bearer your-token"
```

Response:
```json
{
  "case_id": 123,
  "title": "Smith v. Bank of Ghana",
  "ai_case_outcome": "WON",
  "ai_court_orders": "Court ordered bank to pay damages of GHS 50,000 and legal costs",
  "ai_financial_impact": "HIGH - Significant monetary award and legal costs",
  "ai_detailed_outcome": "Plaintiff successfully sued bank for wrongful foreclosure...",
  "ai_summary_generated_at": "2024-01-15T10:30:00Z",
  "ai_summary_version": "1.0",
  "has_analysis": true
}
```

## Configuration

### Batch Processing

The system processes cases in batches to avoid overwhelming the OpenAI API:

- Default batch size: 10 cases
- Configurable via API parameter
- Includes error handling and retry logic

### Content Truncation

- Cases are truncated to ~6000 characters to fit within token limits
- Priority given to `decision`, `judgement`, `conclusion`, and `case_summary` fields
- Additional context from `title`, `area_of_law`, `protagonist`, and `antagonist`

### Error Handling

- Failed cases are logged and skipped
- System continues processing remaining cases
- Detailed error logs available in `ai_analysis_migration.log`

## Monitoring

### Log Files

- `ai_analysis_migration.log`: Detailed processing logs
- Console output: Real-time progress updates

### Progress Tracking

The system provides real-time progress updates:

```
2024-01-15 10:30:00 - INFO - Starting AI analysis for 1500 cases in batches of 10
2024-01-15 10:30:15 - INFO - Processed 10/1500 cases
2024-01-15 10:30:30 - INFO - Processed 20/1500 cases
...
```

## Integration with Frontend

The AI analysis results are automatically displayed in the Banking-Focused Case Summary section:

1. **Summary**: Shows `ai_detailed_outcome`
2. **Case Outcome**: Shows `ai_case_outcome` with visual indicators
3. **Court Orders**: Shows `ai_court_orders`
4. **Financial Impact**: Shows `ai_financial_impact` with color coding

## Troubleshooting

### Common Issues

1. **OpenAI API Key Not Found**
   - Check environment variables or database settings
   - Ensure API key is valid and has sufficient credits

2. **Database Connection Errors**
   - Verify database configuration in `backend/config.py`
   - Check database server is running

3. **Memory Issues with Large Cases**
   - Reduce batch size in migration script
   - Check available system memory

4. **Rate Limiting**
   - OpenAI has rate limits on API calls
   - Increase delays between batches if needed

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Considerations

- **Processing Time**: ~2-5 seconds per case (depending on content length)
- **API Costs**: ~$0.01-0.05 per case (varies by content length)
- **Batch Size**: Recommended 5-10 cases per batch for stability
- **Memory Usage**: ~50-100MB per batch

## Future Enhancements

- [ ] Support for different AI models (GPT-4, Claude, etc.)
- [ ] Custom prompts for different case types
- [ ] Incremental updates for new cases
- [ ] Confidence scoring for AI analysis
- [ ] Integration with case metadata for better context
