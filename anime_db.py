import sqlite3
import pandas as pd

print("Connecting to local SQL Engine.")
conn = sqlite3.connect("anime_warehouse.db")
cursor = conn.cursor()
print("Star Schema")

cursor.executescript("""
DROP TABLE IF EXISTS dim_anime_details;
DROP TABLE IF EXISTS fact_anime_stats;

CREATE TABLE dim_anime_details (
    mal_id INTEGER PRIMARY KEY,
    title TEXT,
    type TEXT,
    status TEXT,
    genres TEXT,
    studios TEXT,
    rating TEXT,
    episodes INTEGER,
    year INTEGER,
    season TEXT,
    demographics TEXT,
    source TEXT,
    score REAL,
    scored_by INTEGER
);

CREATE TABLE fact_anime_stats (    mal_id INTEGER PRIMARY KEY,
    completed INTEGER,
    dropped INTEGER,
    total INTEGER,
    FOREIGN KEY (mal_id) REFERENCES dim_anime_details(mal_id)
);
""")

df_details = pd.read_csv("clean_details.csv")
df_stats = pd.read_csv("clean_stats.csv")

# Append and insert data records straight into the active relational SQL tables
df_details.to_sql("dim_anime_details", conn, if_exists="append", index=False)
df_stats.to_sql("fact_anime_stats", conn, if_exists="append", index=False)
print("Indexing database relationship parameters.")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_details_id ON dim_anime_details(mal_id);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_stats_id ON fact_anime_stats(mal_id);")

conn.commit()
conn.close()
