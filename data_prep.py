import pandas as pd

class DataPrep():
    def __init__(self):
        # Renaming of Traits in Dataset if misplaced
        self.trait_cat_dict = {
            'O': 'cOPN',
            'C': 'cCON',
            'E': 'cEXT',
            'A': 'cAGR',
            'N': 'cNEU',
            'OPN': 'cOPN',
            'CON': 'cCON',
            'EXT': 'cEXT',
            'AGR': 'cAGR',
            'NEU': 'cNEU',
            'Openness': 'cOPN',
            'Conscientiousness': 'cCON',
            'Extraversion': 'cEXT',
            'Agreeableness': 'cAGR',
            'Neuroticism': 'cNEU'
            }

    # loads and gives the Data about the text and the category to requested
    # module 
    def prep_data(self, trait):
        
        df_status = self.prep_status_data()

        X = df_status['STATUS']
        
        y_column = self.trait_cat_dict[trait]
        
        y = df_status[y_column]

        return X, y

    # loads and makes basic necessary changes to the Training Dataset
    def prep_status_data(self):
        df = pd.read_csv('data/myPersonality/mypersonality_final.csv', encoding="ISO-8859-1")
        df = self.convert_traits_to_boolean(df)
        return df

    # Turns the 'y' and 'n' to True/False type present in Categorical Data
    def convert_traits_to_boolean(self, df):
        trait_columns = ['cOPN', 'cCON', 'cEXT', 'cAGR', 'cNEU']
        d = {'y': True, 'n': False}

        for trait in trait_columns:
            df[trait] = df[trait].map(d)

        return df

