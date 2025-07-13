# ReactRadar FastAPI API
🧠 ReactRadar – AI-Powered Influencer Sentiment Analysis
ReactRadar is an AI-driven system that extracts and analyzes influencer feedback from YouTube videos to generate structured brand sentiment insights. Built using FastAPI and modular LangChain components, it processes video transcripts, identifies mentioned brands, analyzes brand-wise sentiment, and generates natural language summaries — enabling brands to understand how they’re being perceived across influencer content.

🔧 Key Features
🎥 Transcript Ingestion
Extracts full transcript from YouTube videos using LangChain's YoutubeLoader.

🔍 Brand Extraction
Uses LLMs to detect and extract protein powder brand names from transcript text.

🧩 Brand-Wise Content Segmentation
Groups relevant feedback statements under each brand using GPT-based document segmentation.

📊 Sentiment Analysis
Applies pre-trained models (DistilBERT, OpenAI) to analyze sentiment (positive/neutral/negative) at the brand level.

⭐ Rating Generation
Converts sentiment scores into brand-wise 5-star rating summaries.

📝 Insight Summary Generation
Uses GPT to generate short, human-readable summaries for each brand's perception.

⚙️ Modular Architecture
Built with a clean Python module layout (data_loader.py, brand_extractor.py, sentiment_analyzer.py, etc.)

🚀 FastAPI Integration
Easily scalable via REST API endpoints for real-time or batch processing.



