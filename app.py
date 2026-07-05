import streamlit as st
from data_loader import load_data
from visualizations import *


# KONFIGURACJA STRONY

st.set_page_config(
    page_title="Analiza rynku mieszkań",
    page_icon="🏠",
    layout="wide"
)


# WCZYTANIE DANYCH


df = load_data()


# Title


st.title("🏠 Dashboard analizy rynku mieszkań")
st.markdown("Interaktywna analiza ofert sprzedaży mieszkań.")


# SIDEBAR


st.sidebar.header("🔎 Filtry")

# Cena

price_min = int(df["price"].min())
price_max = int(df["price"].max())

selected_price = st.sidebar.slider(
    "Cena (PLN)",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max)
)

# Metraż

area_min = int(df["areaSqm"].min())
area_max = int(df["areaSqm"].max())

selected_area = st.sidebar.slider(
    "Metraż (m²)",
    min_value=area_min,
    max_value=area_max,
    value=(area_min, area_max)
)

# Liczba pokoi

rooms = sorted(df["rooms"].dropna().unique())

selected_rooms = st.sidebar.multiselect(
    "Liczba pokoi",
    rooms,
    default=rooms
)

# Typ nieruchomosci

property_types = sorted(df["propertyType"].dropna().unique())

selected_type = st.sidebar.multiselect(
    "Typ nieruchomości",
    property_types,
    default=property_types
)

# Wyszukiwanie

search = st.sidebar.text_input("🔍 Wyszukaj w tytule")


# FILTROWANIE


filtered = df.copy()

filtered = filtered[
    (filtered["price"] >= selected_price[0]) &
    (filtered["price"] <= selected_price[1])
    ]

filtered = filtered[
    (filtered["areaSqm"] >= selected_area[0]) &
    (filtered["areaSqm"] <= selected_area[1])
    ]

filtered = filtered[
    filtered["rooms"].isin(selected_rooms)
]

filtered = filtered[
    filtered["propertyType"].isin(selected_type)
]

if search:
    filtered = filtered[
        filtered["title"].str.contains(
            search,
            case=False,
            na=False
        )
    ]


# kpi


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🏠 Liczba ofert",
    len(filtered)
)

col2.metric(
    "💰 Średnia cena",
    f"{filtered['price'].mean():,.0f}".replace(",", " ") + " PLN"
)

col3.metric(
    "📐 Średni metraż",
    f"{filtered['areaSqm'].mean():.1f} m²"
)

col4.metric(
    "🏷 Średnia cena / m²",
    f"{filtered['pricePerSqm'].mean():,.0f}".replace(",", " ") + " PLN"
)

st.divider()


# ZAKŁADKI-  sprawdzic funkcjonalnosc


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Analiza rynku",
        "🏙 Miasta",
        "📈 Statystyki",
        "📄 Dane"
    ]
)

# TAB 1


with tab1:

    st.subheader("📊 Analiza rynku mieszkań")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            price_histogram(filtered),
            use_container_width=True
        )

        st.caption(
            "Większość mieszkań mieści się w średnim przedziale cenowym. Widoczne są pojedyncze bardzo drogie oferty."
        )

    with col2:
        st.plotly_chart(
            area_histogram(filtered),
            use_container_width=True
        )

        st.caption(
            "Najwięcej ofert dotyczy mieszkań o powierzchni około 40–70 m²."
        )

    st.divider()

    st.plotly_chart(
        scatter_price_area(filtered),
        use_container_width=True
    )

    st.caption(
        "Wraz ze wzrostem metrażu rośnie cena nieruchomości, jednak zależność nie jest idealnie liniowa."
    )


# TAB 2


with tab2:

    st.subheader("🏙 Analiza lokalizacji")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            city_chart(filtered),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            average_price_rooms(filtered),
            use_container_width=True
        )

    st.divider()

    st.plotly_chart(
        box_price_per_sqm(filtered),
        use_container_width=True
    )

    st.caption(
        "Boxplot pokazuje rozkład ceny za metr kwadratowy dla mieszkań o różnej liczbie pokoi."
    )

# TAB 3


with tab3:

    st.subheader("📈 Statystyki rynku")

    st.plotly_chart(
        correlation_heatmap(filtered),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            offers_over_time(filtered),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            property_type_chart(filtered),
            use_container_width=True
        )

    st.divider()

    st.plotly_chart(
        top_expensive(filtered),
        use_container_width=True
    )

    st.plotly_chart(
        price_trend(filtered),
        use_container_width=True
    )

    st.caption(
        "Najsilniejszą dodatnią korelację z ceną posiada metraż mieszkania oraz cena za metr kwadratowy."
    )

    st.divider()

    st.dataframe(
        filtered.describe(),
        use_container_width=True
    )


# TAB 4


with tab4:

    st.subheader("Dane")

    st.dataframe(filtered)

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Pobierz dane CSV",
        csv,
        "mieszkania.csv",
        "text/csv"
    )

st.divider()

st.header("📌 Automatyczne wnioski")

highest_price = filtered["price"].max()

avg_price = filtered["price"].mean()

avg_area = filtered["areaSqm"].mean()

most_rooms = (
    filtered["rooms"]
    .mode()
    .iloc[0]
)

st.success(f"""
Najważniejsze obserwacje:

• Najdroższa oferta kosztuje **{highest_price:,.0f} PLN**

• Średnia cena mieszkań wynosi **{avg_price:,.0f} PLN**

• Średni metraż ofert to **{avg_area:.1f} m²**

• Najczęściej występują mieszkania **{int(most_rooms)}-pokojowe**.
""")