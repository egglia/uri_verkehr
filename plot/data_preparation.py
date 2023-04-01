from pandasql import sqldf
import pandasql


def addAggregationsForEachDay(df_prepared_example):
    df_prepared_example
    carsPerHour = "SELECT Zst, Datumszeit, sum(Querschnitt) as anzahlZurStunde FROM df_prepared_example GROUP BY Zst, Datumszeit"
    df_cars_per_hour = sqldf(carsPerHour)
    df_cars_per_hour

    zstMeasruesPerDay = "SELECT Zst, cast(Datumszeit as date) as Datum, sum(anzahlZurStunde) as amountOnThisDay, sum(anzahlZurStunde)/24 as avgPerHourOnThisDay, min(anzahlZurStunde) as lowestAmountOnThisDay, max(anzahlZurStunde) as highestAmountOnThisDay " \
                        "FROM df_cars_per_hour " \
                        "GROUP BY Zst, Datum"
    return sqldf(zstMeasruesPerDay)
