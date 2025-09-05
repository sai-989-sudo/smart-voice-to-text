import os
import re
import spacy

# Load general spaCy model for names
general_nlp = spacy.load("en_core_web_sm")

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "custom-spacy", "ner_model")
custom_med_nlp = spacy.load(model_path)


# Preprocess text to normalize spacing and remove noise
def preprocess_text(text):
    text = text.strip().replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    return text

# Extract patient's name using the general model
def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    return "unknown"

# Extract age using regex
def extract_age(text):
    match = re.search(r"\b(\d{1,3})\s*(yo|y/o|years?\s+old|yrs?\s+old)\b", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

# Extract gender using regex
def extract_gender(text):
    if re.search(r'\bmale\b', text, re.IGNORECASE):
        return "male"
    elif re.search(r'\bfemale\b', text, re.IGNORECASE):
        return "female"
    return "unknown"

# Extract symptoms and medications from custom model
def extract_medical_entities(text):
    doc = custom_med_nlp(text)

    symptoms = set()
    drugs = set()

    for ent in doc.ents:
        label = ent.label_.upper()
        ent_text = ent.text.strip().lower()

        if label in ["MEDICALCONDITION", "DISEASE", "SYMPTOM", "DISORDER", "PROBLEM"]:
            symptoms.add(ent_text)
        elif label in ["DRUG", "MEDICATION", "MEDICINE", "TREATMENT"]:
            drugs.add(ent_text)

    return list(symptoms), list(drugs)

# Check if the mentioned drugs were actually prescribed
def check_if_prescribed(text, drugs):
    prescribed_drugs = []
    for drug in drugs:
        pattern = rf"(prescribed|administered|given|started on|put on)\s+(?:the\s+)?{re.escape(drug)}"
        if re.search(pattern, text, re.IGNORECASE):
            prescribed_drugs.append(drug)
    return prescribed_drugs

# Main pipeline function to extract structured info
def extract_insights(transcript):
    cleaned_text = preprocess_text(transcript)

    doc_general = general_nlp(cleaned_text)
    symptoms, drugs = extract_medical_entities(cleaned_text)
    prescribed = check_if_prescribed(cleaned_text, drugs)

    # Convert the symptoms list to a comma-separated string
    symptoms_str = ", ".join(symptoms)

    return {
        "name": extract_name(doc_general),
        "age": extract_age(cleaned_text),
        "gender": extract_gender(cleaned_text),
        "symptoms": symptoms_str,  # Return symptoms as a comma-separated string
        "prescribed_medications": prescribed
    }
