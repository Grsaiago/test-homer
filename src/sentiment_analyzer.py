from transformers import pipeline

sentiment_analyzer = pipeline(
    "sentiment-analysis", model="neuralmind/bert-base-portuguese-cased"
)
