import math
from exceptions import InvalidTransactionError
def parse_amount(text):
        # Remove any commas and convert to float
        if not isinstance(text,str):
                raise InvalidTransactionError
        cleaned_text= text.strip()
        upper_cleaned= cleaned_text.upper()
        for char in ['XOF', 'FCFA']:
                if upper_cleaned.endswith(char):
                        cleaned_text= cleaned_text[:-len(char)].strip()
                        break
        separators=[',', ' ', '\u00a0', '\u202f']
        for i in separators:
                cleaned_text= cleaned_text.replace(i,'')
        try:
                amount= float(cleaned_text)
        except ValueError:
                    raise InvalidTransactionError (f"Unable to parse {text} ")
        if  not math.isfinite(amount):
                raise InvalidTransactionError (f" Value must be finite got {text} ")
        return amount

def format_xof(amount):
        rounded_amount= round(amount)
        return f"{rounded_amount:,}".replace(",", " ") + " XOF"
