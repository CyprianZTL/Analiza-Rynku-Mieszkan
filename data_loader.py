import pandas as pd
import streamlit as st


@st.cache_data
def load_data():

    df = pd.read_json("data/mieszkania.json")

    # wybieramy tylko kolumny potrzebne do dashboardu
    df = df[
        [
            "title",
            "price",
            "pricePerSqm",
            "monthlyRent",
            "areaSqm",
            "rooms",
            "floor",
            "city",
            "agencyType",
            "propertyType",
            "dateCreated",
            "fullAddress",
            "latitude",
            "longitude",
        ]
    ].copy()

    # usuwamy rekordy bez najważniejszych danych
    df = df.dropna(
        subset=[
            "price",
            "pricePerSqm",
            "areaSqm",
            "rooms",
        ]
    )

    # konwersje typów
    df["price"] = pd.to_numeric(df["price"])
    df["pricePerSqm"] = pd.to_numeric(df["pricePerSqm"])
    df["areaSqm"] = pd.to_numeric(df["areaSqm"])
    df["rooms"] = pd.to_numeric(df["rooms"])
    df["monthlyRent"] = pd.to_numeric(
        df["monthlyRent"],
        errors="coerce"
    ).fillna(0)

    # konwersja dat
    df["dateCreated"] = pd.to_datetime(
        df["dateCreated"],
        errors="coerce"
    )

    df = df.dropna(subset=["dateCreated"])

    # kolumny pomocnicze
    df["year"] = df["dateCreated"].dt.year
    df["month"] = df["dateCreated"].dt.month_name()

    df["dateCreated"] = df["dateCreated"].dt.strftime("%Y-%m-%d")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    return df