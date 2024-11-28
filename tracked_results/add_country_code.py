import pandas as pd
import country_converter as coco


def main():
    # read country_destruction_frequency.csv

    df = pd.read_csv("country_destruction.csv")
    print(df.head())

    cc = coco.CountryConverter()

    # add country code column
    df["country_code"] = cc.convert(names=df["Country"], to="ISO3")

    print(df.head())

    # stop if country_code has any NaN values
    assert not df["country_code"].isna().any()

    # re-order columns : set country_code to the second column
    df = df[["Country", "country_code", "Frequency"]]

    # save the dataframe to a new csv file
    df.to_csv("country_destruction_with_country_code.csv", index=False)


if __name__ == "__main__":
    main()
