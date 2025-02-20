from pysentimiento import create_analyzer

# sentiment_analyzer = pipeline(
#     "sentiment-analysis", model="pysentimento/bert-base-portuguese-cased-sentiment"
# )

sentiment_analyzer = create_analyzer(task="sentiment", lang="pt")
