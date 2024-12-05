import pandas as pd

def load_data(csv_file):
    #Load the .csv file
    return pd.read_csv(csv_file)

def filter_by_label(df, label):
    #Filter after label
    return df[df['label'] == label]

def analyze_connections(df):
    #Find connections within entities based on entity_id and source text
    return df[df['entity_id'].notnull() & df['source_text_id'].notnull()]

def save_to_csv(df, filename):
    #Save data to a csv file
    return df.to_csv(filename, index=False)

if __name__ == "__main__":
    # Path to the CSV file containing the data
    csv_file = 'fastapi_db_public_entities.csv'

    # Load the data
    df = load_data(csv_file)

    # Filter entities
    people = filter_by_label(df, 380)  # People, including fictional
    places = filter_by_label(df, 386)  # Geopolitical entities (countries, cities, states)
    money = filter_by_label(df, 394)  # Monetary values, including currency
    org = filter_by_label(df, 384)  # Organizations, companies, institutions
    norp = filter_by_label(df, 398) # Nationalities, religious groups, political groups
    fac = filter_by_label(df, 399) # Buildings, airports, highways, bridges, etc.
    work_of_art = filter_by_label(df, 400) # Titles of books, songs, etc

    # Analyze connections
    connections = analyze_connections(df)

    # Display results
    #print("People:\n", people)
    #print("Places:\n", places)
    #print("Money:\n", money)
    #print("Organizations\n", org)
    #print("Connections:\n", connections)

    # Save results to CSV (optional)
    #save_to_csv(people, 'people.csv')
    #save_to_csv(places, 'places.csv')
    #save_to_csv(money, 'money.csv')
    #save_to_csv(org, 'org.csv')
    #save_to_csv(connections, 'connect.csv')
    #save_to_csv(norp, 'norp.csv')
    #save_to_csv(fac, 'fac.csv')
    #save_to_csv(work_of_art, 'work_of_art.csv')

    print("Money Mentions:\n", money['text'].value_counts())
    print("People mentions:\n", people['text'].value_counts())
    print("Locations:\n", places['text'].value_counts())
    print("Named locations:\n", fac['text'].value_counts())
    print("Nationalities:\n", norp['text'].value_counts())
    print("Art:\n", work_of_art['text'].value_counts())

    #clara_mentions = people['text'].str.contains(r'\bClara\b|\bClara Davenport\b', regex=True).sum()
    #print("Clara mentions count:\n", clara_mentions)



