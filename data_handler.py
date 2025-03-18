import pandas as pd
import os

PERSONAL_CSV = "personal_info.csv"
TECHNICAL_CSV = "technical_responses.csv"

def save_personal_info(user_info):
    """Save personal details to a CSV file."""
    df = pd.DataFrame([user_info])  # Convert dictionary to DataFrame
    file_exists = os.path.exists(PERSONAL_CSV)
    df.to_csv(PERSONAL_CSV, index=False, mode='a',header=not file_exists)

def save_technical_responses(tech_responses):
    """Save technical question responses to a CSV file."""
    data = [{"Question": question, "Response": response} for question, response in tech_responses.items()]
    df = pd.DataFrame(data)
    file_exists = os.path.exists(TECHNICAL_CSV)
    df.to_csv(TECHNICAL_CSV, index=False, mode='a',header=not file_exists)

def load_personal_info():
    """Load personal info if CSV exists."""
    if os.path.exists(PERSONAL_CSV):
        return pd.read_csv(PERSONAL_CSV).to_dict(orient="records")[0]  # Return first row as dict
    return {}

def load_technical_responses():
    """Load technical responses if CSV exists."""
    if os.path.exists(TECHNICAL_CSV):
        df = pd.read_csv(TECHNICAL_CSV)
        return {row["Technology"]: row["Responses"].split(", ") for _, row in df.iterrows()}
    return {}
