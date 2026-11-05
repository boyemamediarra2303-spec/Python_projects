from exceptions import InvalidInputError
def parse_amount(text):
        # Remove any commas and convert to float
        if not isinstance(text,str):
                raise InvalidInputError
        cleaned_text= text.strip()
        upper_cleaned= cleaned_text.upper()
        for char in ['XOF', 'FCFA']:
                if upper_cleaned.endswith(char):
                        cleaned_text= cleaned_text[:-len(char)].strip()
                        break
        