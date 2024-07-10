import pandas as pd
import re 
from datetime import datetime

class textMining():

    def __init__(self, data):
        self.data = data

    def find_avg_length_of_text(self, col_name=None):
        if isinstance(self.data, pd.DataFrame):
            if col_name is None: 
                raise ValueError("Column name must be provided for DataFrame input")
            text = self.data[col_name].fillna('') # Replace null with empty string
        elif isinstance(self.data, pd.Series):
            text = self.data.fillna('')
        else:
            raise ValueError("Input data must be a pandas DataFrame or Series")
        
        lengths = [len(doc) for doc in text]

        print("Average length of text per doc:", sum(lengths) / len(lengths))

        return lengths
    
    # Convert various date string formats to date type
    # Helper function 
    def parse_date(self, text):
        for fmt in ('%m/%d/%Y', '%m/%d/%y', '%m-%d-%y','%-m/%d/%y', '%b-%d-%Y', '%b %d %Y', '%b, %Y', '%B %d %Y', '%B, %Y', '%d %b %Y','%B %d, %Y', '%d %B %Y','%b. %d, %Y','%B. %d, %Y', '%b %Y','%b %d, %Y', '%B %Y', '%m/%Y', '%m/%y', '%Y', '%y'):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                pass
        return None # if no valid format is found 
    
    def extract_date(self):
    
        # Define Regular Expression patterns for all possible date variants, order by highest possiblity of date match to lowest possibility of match
        patterns = [r'(\d{1,2}(?:st|nd|rd|th)? (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-,.]?\s*\d{2,4})',
                    r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-.]?\s* *\d{1,2}(?:st|nd|rd|th)?[-,.]?\s*\d{2,4})', 
                    r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-.,]?\s*\d{4})',
                    r'(\d{1,2}[\/-]\d{2}[\/-](\d{4}|\d{2}))',
                    r'(\d{1,2}\b[/-]\d{1,2}[/-]?\b(\d{4}|\d{2})\b)',
                    r'(\d{1,2}\b[/-]\d{4}\b)',
                    r'(\d{4}\b)'
        ] 

        output = []
        for text in self.data:
            parsed_date = None
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    parsed_date = self.parse_date(match.group(0))
                    if parsed_date is not None: # Check if data parsing is successful
                        break 
            
            output.append({'original_text': text, 'date': parsed_date})

        return pd.DataFrame(output)
    
    def extract_social_handle(self, col_name_with_handles: str):

        """
        Extract each social handle with @ and assign each one to a row
        """

        if isinstance(self.data, pd.DataFrame):
            output = []
            for index, row in self.data.iterrows():
                handles = re.findall(r'@\w+', row[col_name_with_handles])
                for handle in handles:
                    new_row = row.copy()
                    new_row['extracted_handle'] = handle
                    output.append(pd.DataFrame(new_row).transpose())

            result_df = pd.concat(output).reset_index(drop=True)

        else:
            raise ValueError("Data must be a pandas DataFrame")

        return result_df
    
    import re

    def remove_urls(self):

        # Define the regex pattern for any possible URLs 
        pattern = r'https?://[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)+|(?:www\.)?[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)+'
        
        # Use re.sub to replace all matches of the pattern with an empty string
        cleaned_text = re.sub(pattern, '', self.data)
        
        return cleaned_text
    
    def remove_digits_from_percentage(self, text: pd.Series) -> pd.Series: 
        if not isinstance(text, pd.Series):
            raise TypeError("Input text must be a pandas Series.")
        cleaned_text = text.str.replace(r'\b\d+%?\b', '', regex=True )
        return cleaned_text 


