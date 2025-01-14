from transformers import pipeline

# Load zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Text to classify
text = "This study examines the impact of climate change on marine biodiversity."

# Labels with descriptions
labels = [
    "Biophysical: Related to the physical and biological aspects of the environment and living organisms.",
    "Social: Pertaining to human society, interactions, and social structures.",
    "Psychological: Concerned with mental processes and behavior."
]

# Perform classification
result = classifier(text, candidate_labels=labels, multi_class=False)

# Output results
print(result)