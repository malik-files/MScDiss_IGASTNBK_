import polars as pl
import datetime as dt


print(f"Start Time: {str(dt.datetime.now().time())}")
df = pl.scan_ndjson("artist.json")
print(df)
print(df.collect_schema().names())
print(df.head(2).collect())
result = df.select(pl.col("type").unique())
print(result.collect().__array__())


#For Groups
q1 = (
    pl.scan_ndjson("artist.json")
    .select(
        pl.col("id"),
        pl.col("name"),
        pl.col("type"),
        pl.col(["gender","country","genres","isnis","ipis","tags","life-span"]),
    )
    .filter((pl.col("type") == "Orchestra") | (pl.col("type") == "Choir") |(pl.col("type") == "Group"))
    #This drops all the duplicates that may exist
    .unique()



    #save the file
    .sink_parquet("ensemblesMusicBrainzData.parquet", engine="streaming")

)
#Saved the group data as a parquet
print(f"Saved the group data as a parquet. Time {str(dt.datetime.now().time())}")
print("Operation Done")
