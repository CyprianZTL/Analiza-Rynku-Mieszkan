import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



# Histogram cen mieszkań


def price_histogram(df):
    fig = px.histogram(
        df,
        x="price",
        nbins=40,
        title="Rozkład cen mieszkań",
        labels={"price": "Cena [PLN]"},
        template="plotly_white"
    )

    fig.update_layout(height=450)

    return fig



# Histogra metrażu


def area_histogram(df):
    fig = px.histogram(
        df,
        x="areaSqm",
        nbins=35,
        title="Rozkład metrażu mieszkań",
        labels={"areaSqm": "Metraż [m²]"},
        template="plotly_white"
    )

    fig.update_layout(height=450)

    return fig



# Cena względem metrażu


def scatter_price_area(df):
    fig = px.scatter(
        df,
        x="areaSqm",
        y="price",
        color="rooms",
        hover_name="title",
        size="pricePerSqm",
        title="Cena względem metrażu",
        template="plotly_white"
    )

    fig.update_layout(height=500)

    return fig



# Średnia cena wg liczby pokoi


def average_price_rooms(df):

    rooms = (
        df.groupby("rooms")["price"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        rooms,
        x="rooms",
        y="price",
        text_auto=".0f",
        title="Średnia cena według liczby pokoi",
        template="plotly_white"
    )

    fig.update_layout(height=450)

    return fig



# Boxplot ceny za m²


def box_price_per_sqm(df):

    fig = px.box(
        df,
        x="rooms",
        y="pricePerSqm",
        color="rooms",
        title="Cena za m² według liczby pokoi",
        template="plotly_white"
    )

    fig.update_layout(height=450)

    return fig



# Heatmap korelacji


def correlation_heatmap(df):

    corr = df[
        [
            "price",
            "pricePerSqm",
            "monthlyRent",
            "areaSqm",
            "rooms",
        ]
    ].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Macierz korelacji"
    )

    fig.update_layout(height=550)

    return fig



# Ranking miast


def city_chart(df):

    city = (
        df.groupby("city")
        .size()
        .reset_index(name="offers")
        .sort_values("offers", ascending=False)
    )

    fig = px.bar(
        city,
        x="city",
        y="offers",
        text="offers",
        title="Liczba ofert według miasta",
        template="plotly_white"
    )

    fig.update_layout(height=450)

    return fig

def map_chart(df):

    mapa = df.dropna(
        subset=["latitude", "longitude"]
    )

    fig = px.scatter_mapbox(
        mapa,
        lat="latitude",
        lon="longitude",
        hover_name="title",
        hover_data=[
            "price",
            "areaSqm",
            "rooms"
        ],
        zoom=10,
        height=650,
        color="pricePerSqm"
    )



    return fig

def price_trend(df):

    trend = (
        df.groupby("dateCreated")["price"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        trend,
        x="dateCreated",
        y="price",
        markers=True,
        title="Średnia cena ofert w czasie",
        template="plotly_white"
    )

    fig.update_layout(height=500)

    return fig


# TOP 10


def top_expensive(df):

    top = (
        df.sort_values("price", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top,
        x="price",
        y="title",
        orientation="h",
        text="price",
        title="TOP 10 najdroższych ofert",
        template="plotly_white"
    )

    fig.update_layout(
        height=600,
        yaxis=dict(categoryorder="total ascending")
    )

    return fig


# Typ nieruchomści


def property_type_chart(df):

    prop = (
        df.groupby("propertyType")
        .size()
        .reset_index(name="count")
    )

    fig = px.pie(
        prop,
        names="propertyType",
        values="count",
        hole=0.45,
        title="Struktura typów nieruchomości"
    )

    fig.update_layout(height=500)

    return fig


# Liczba ofert w czasie

def offers_over_time(df):

    offers = (
        df.groupby("dateCreated")
        .size()
        .reset_index(name="offers")
    )

    fig = px.line(
        offers,
        x="dateCreated",
        y="offers",
        markers=True,
        title="Liczba nowych ofert w czasie",
        template="plotly_white"
    )

    fig.update_layout(height=500)

    return fig