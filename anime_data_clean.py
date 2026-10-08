import pandas as pd

print("Reading details.csv.")
df_details = pd.read_csv("details.csv")[[
    'mal_id', 'title', 'type', 'status', 'genres', 'studios', 
    'rating', 'episodes', 'year', 'season', 'demographics', 'source', 
    'score', 'scored_by'
]]

print("Cleaning fields.")
for col in ['title', 'type', 'status', 'genres', 'studios', 'rating', 'season', 'demographics', 'source']:
    df_details[col] = df_details[col].fillna('Unknown').str.strip()

df_details['mal_id'] = pd.to_numeric(df_details['mal_id'], errors='coerce').fillna(0).astype(int)
df_details['year'] = pd.to_numeric(df_details['year'], errors='coerce').fillna(0).astype(int)
df_details['episodes'] = pd.to_numeric(df_details['episodes'], errors='coerce').fillna(12).astype(int)
df_details['score'] = pd.to_numeric(df_details['score'], errors='coerce').fillna(0.0)
df_details['scored_by'] = pd.to_numeric(df_details['scored_by'], errors='coerce').fillna(0).astype(int)

print("Cleaning stats.csv.")
df_stats = pd.read_csv("stats.csv")[['mal_id', 'completed', 'dropped', 'total']]

for col in ['mal_id', 'completed', 'dropped', 'total']:
    df_stats[col] = pd.to_numeric(df_stats[col], errors='coerce').fillna(0).astype(int)

print("Saving files")
df_details.to_csv("clean_details.csv", index=False)
df_stats.to_csv("clean_stats.csv", index=False)

print("Success!")
