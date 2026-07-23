import polars as pl
import datetime as dt


print(f"Start Time: {str(dt.datetime.now().time())}")
df = pl.scan_ndjson("artist.json")
print(df)
print(df.collect_schema().names())
print(df.head(2).collect())
result = df.select(pl.col("type").unique())



#For People
print(f"Start the journey of reading in the file. Time {str(dt.datetime.now().time())}")
#For People
q2 = (
    pl.scan_ndjson("artist.json")
    .filter(pl.col("type") == "Person")
    .select(
        pl.col("id"),
        pl.col("name"),
        pl.col("type"),
        pl.col(["gender","country","genres","isnis","ipis","life-span"]),
    )
        #This drops all the duplicates that may exist
    
    .sink_parquet("personMusicBrainzData.parquet")
)

#Saved the people data as a parquet
print(f"Saved the people data as a parquet. Time {str(dt.datetime.now().time())}")

print("Operation Done")
