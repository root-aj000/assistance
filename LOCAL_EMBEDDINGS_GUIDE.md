# Free Local Embeddings Setup Guide

## 🎉 Problem Solved!

You're hitting Gemini API quota limits for embeddings. The solution: **Use FREE local embeddings** that run on your machine with **zero API calls** and **unlimited usage**!

## 🚀 Quick Start

### Step 1: Install Required Packages

```bash
cd backend
pip install sentence-transformers==2.2.2 torch==2.1.2
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 2: Update Your .env File

Add these lines to your `backend/.env`:

```bash
# Embedding Configuration
USE_LOCAL_EMBEDDINGS=true
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Step 3: Restart Backend

```bash
python main.py
```

You should see:
```
🏠 Using LOCAL embeddings (free, unlimited)
📦 Loading local embedding model: all-MiniLM-L6-v2...
✅ Local embedding model loaded! Dimension: 384
```

## ✅ Done!

No more quota errors! Your embeddings now run 100% locally and for free.

---

## 📊 Available Free Models

You can choose different models in `.env`:

### 1. **all-MiniLM-L6-v2** (Default - Recommended)
```bash
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2
```
- **Size:** Small (~80MB)
- **Dimensions:** 384
- **Speed:** Very Fast ⚡
- **Quality:** Good for most tasks

### 2. **all-mpnet-base-v2** (Better Quality)
```bash
LOCAL_EMBEDDING_MODEL=all-mpnet-base-v2
```
- **Size:** Medium (~420MB)
- **Dimensions:** 768 (same as Gemini!)
- **Speed:** Fast
- **Quality:** Excellent, highest quality

### 3. **multi-qa-MiniLM-L6-cos-v1** (Optimized for Q&A)
```bash
LOCAL_EMBEDDING_MODEL=multi-qa-MiniLM-L6-cos-v1
```
- **Size:** Small (~80MB)
- **Dimensions:** 384
- **Speed:** Very Fast
- **Quality:** Optimized for question-answering

## 🔄 Switching Between Local and Gemini

You can easily switch:

### Use Local Embeddings (FREE, no quota):
```bash
USE_LOCAL_EMBEDDINGS=true
```

### Use Gemini Embeddings (requires API quota):
```bash
USE_LOCAL_EMBEDDINGS=false
```

## 💡 How It Works

1. **Unified Interface**: The system automatically uses the right embedding generator
2. **No Code Changes**: Everything works exactly the same
3. **Lazy Loading**: Model loads only when first needed
4. **Cached**: Once loaded, model stays in memory for fast access

## 🎯 Performance Comparison

| Feature | Local (all-MiniLM-L6-v2) | Gemini |
|---------|-------------------------|--------|
| **Cost** | FREE ✅ | Free tier limited |
| **Speed** | ~10ms per text | ~100-500ms (API call) |
| **Quota** | UNLIMITED ✅ | 50-1500 per day |
| **Quality** | Good | Excellent |
| **Offline** | Works offline ✅ | Requires internet |
| **Privacy** | 100% local ✅ | Data sent to Google |

## 📝 Code Usage

The unified interface makes it transparent:

```python
from llm.unified_embeddings import unified_embedding_generator

# Generate embedding (automatically uses local or Gemini based on settings)
embedding = await unified_embedding_generator.generate_embedding("Hello world")

# Batch embeddings
embeddings = await unified_embedding_generator.generate_embeddings_batch([
    "First text",
    "Second text"
])

# Query embedding
query_embedding = await unified_embedding_generator.generate_query_embedding("search query")
```

## 🔧 Files Created

1. **llm/local_embeddings.py** - Local embedding generator using sentence-transformers
2. **llm/unified_embeddings.py** - Smart interface that chooses local or Gemini
3. **requirements.txt** - Updated with sentence-transformers

## ⚠️ Note: First Run

The first time you run with local embeddings, it will:
1. Download the model from HuggingFace (~80-420MB depending on model)
2. Cache it in `~/.cache/torch/sentence_transformers/`
3. Subsequent runs will be instant!

## 🎉 Benefits

✅ **No API quota errors**
✅ **Unlimited embeddings**  
✅ **Faster than API calls**
✅ **Works offline**
✅ **100% free forever**
✅ **Privacy-friendly (data stays local)**

---

**Recommendation:** Keep `USE_LOCAL_EMBEDDINGS=true` for development and free usage. Only switch to Gemini if you need their specific embedding quality and have quota available.
