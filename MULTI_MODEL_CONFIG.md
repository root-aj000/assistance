# Multi-Model Configuration with Rate Limiting

## Overview
Your Vibe Coding AI Agent has been configured to use the latest Gemini 2.5 models with intelligent rate limiting to prevent quota exceeded errors.

## 🎯 Configured Models

### 1. **gemini-2.5-flash** (Default)
- **Use Case:** General chat, code analysis, debugging
- **Speed:** Fast
- **Rate Limit:** 3 requests per minute

### 2. **gemini-2.5-pro**
- **Use Case:** Complex reasoning, advanced code generation  
- **Speed:** Slower but more capable
- **Rate Limit:** 3 requests per minute

### 3. **gemini-2.5-flash-lite**
- **Use Case:** Quick queries, simple tasks
- **Speed:** Ultra-fast
- **Rate Limit:** 3 requests per minute

### 4. **text-embedding-004**
- **Use Case:** Code embeddings for vector search
- **Rate Limit:** 3 requests per minute

## 📁 Configuration Files

### Environment Variables (.env)
Add these to your `backend/.env` file:

```bash
# Gemini API Configuration
GEMINI_API_KEY=your_actual_api_key_here

# Gemini Model Selection
GEMINI_FLASH_MODEL=gemini-2.5-flash
GEMINI_PRO_MODEL=gemini-2.5-pro
GEMINI_LITE_MODEL=gemini-2.5-flash-lite
GEMINI_EMBEDDING_MODEL=models/text-embedding-004

# Default model to use for chat
DEFAULT_CHAT_MODEL=gemini-2.5-flash

# Model-specific Rate Limiting (requests per minute)
# Set to 3 RPM to avoid quota issues on free tier
FLASH_RATE_LIMIT_RPM=3
PRO_RATE_LIMIT_RPM=3
LITE_RATE_LIMIT_RPM=3
EMBEDDING_RATE_LIMIT_RPM=3

# Graph Database (Neo4j)
GRAPH_DB_URL=neo4j://127.0.0.1:7687
GRAPH_DB_USER=neo4j
GRAPH_DB_PASSWORD=Anish_110

# Legacy Rate Limiting (kept for backwards compatibility)
RATE_LIMIT_RPM=3
RATE_LIMIT_TPM=100000
```

## 🚀 New Features

### 1. **Rate Limiting System**
- **File:** `backend/llm/rate_limiter.py`
- **Features:**
  - Thread-safe token bucket rate limiter
  - Per-model rate limiting
  - Automatic request spacing
  - Prevents quota exceeded errors

### 2. **Enhanced Error Handling**
- Clear error messages for quota issues
- Helpful links to check usage and upgrade
- Automatic retry with exponential backoff
- Fast-fail on quota errors (no wasteful retries)

### 3. **Multiple Client Instances**
Available in `backend/llm/gemini_client.py`:
- `gemini_client` - Default model (gemini-2.5-flash)
- `gemini_flash_client` - Flash model
- `gemini_pro_client` - Pro model  
- `gemini_lite_client` - Lite model

## 📊 How Rate Limiting Works

```python
# Rate limiter automatically waits before each request
rate_limiter.wait_if_needed(model_name)

# For 3 RPM, requests are spaced 20 seconds apart
# Request 1: 0s
# Request 2: 20s (waits 20s)
# Request 3: 40s (waits 20s)
# Request 4: 60s (waits 20s)
```

## 🔧 Updated Files

### Backend
1. **config.py** - Added model configurations and rate limit settings
2. **llm/rate_limiter.py** - NEW: Rate limiting utility
3. **llm/gemini_client.py** - Integrated rate limiter, multi-model support
4. **llm/embeddings.py** - Added rate limiting for embeddings
5. **.env.example** - Updated with new configuration options

### Frontend
1. **app/settings/page.tsx** - Updated UI to show new models and rate limits

## ⚡ Usage Examples

### Using Different Models

```python
from llm.gemini_client import gemini_flash_client, gemini_pro_client, gemini_lite_client

# Use Flash for quick responses
response = await gemini_flash_client.generate_response("Explain this code")

# Use Pro for complex reasoning
response = await gemini_pro_client.generate_response("Design a scalable architecture")

# Use Lite for simple queries
response = await gemini_lite_client.generate_response("What is this function?")
```

### Rate Limiter Status

```python
from llm.rate_limiter import rate_limiter

# Check if can make request
can_request = rate_limiter.can_make_request("gemini-2.5-flash")

# Get time until next request
wait_time = rate_limiter.time_until_next_request("gemini-2.5-flash")
```

## 🎛️ Adjusting Rate Limits

If you upgrade your API plan, adjust the rate limits in `.env`:

```bash
# For paid tier, you might increase to:
FLASH_RATE_LIMIT_RPM=15
PRO_RATE_LIMIT_RPM=10
LITE_RATE_LIMIT_RPM=20
EMBEDDING_RATE_LIMIT_RPM=15
```

## 🔗 Helpful Links

- **Check Usage:** https://ai.dev/usage
- **Rate Limits:** https://ai.google.dev/gemini-api/docs/rate-limits
- **Gemini API Docs:** https://ai.google.dev/gemini-api/docs

## ✅ Testing

1. Restart your backend to load new configuration:
   ```bash
   cd backend
   python main.py
   ```

2. The console will show rate limiter initialization:
   ```
   ✅ Rate limiter configured for gemini-2.5-flash: 3 RPM
   ✅ Rate limiter configured for gemini-2.5-pro: 3 RPM
   ✅ Rate limiter configured for gemini-2.5-flash-lite: 3 RPM
   ✅ Rate limiter configured for embeddings: 3 RPM
   ```

3. When making requests, you'll see:
   ```
   ⏳ Rate limit: waiting 20.0s before next request
   ```

## 🎉 Benefits

- ✅ **No More Quota Errors** - Automatic request spacing
- ✅ **Multi-Model Support** - Choose the right model for each task
- ✅ **Better Error Messages** - Clear guidance when issues occur
- ✅ **Cost Control** - Prevents wasteful retries
- ✅ **Production Ready** - Thread-safe, robust implementation

---

**Note:** Remember to add your actual Gemini API key to the `.env` file before running!
