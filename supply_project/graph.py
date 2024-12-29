from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from collections import Counter
import matplotlib.pyplot as plt
from models import Tool
from config import DATABASE_URL


def display_pie_chart(year_counts):
    """
    Wyświetla wykres kołowy z podziałem według wartości 'added_year'
    oraz legendą obok wykresu.
    """
    labels = [f"{year} ({count})" for year, count in year_counts.items()]  # Etykiety
    sizes = year_counts.values()  # Wielkości dla każdego roku
    explode = [0.1] * len(labels)  # Wyróżnienie wszystkich kawałków (opcjonalne)

    fig = plt.figure(figsize=(8, 6))
    fig.canvas.manager.set_window_title("Rok dodania")  # Ustawienie tytułu okna
    wedges, texts, autotexts = plt.pie(
        sizes, labels=None, autopct='%1.1f%%', startangle=140, explode=explode
    )

    # Dodanie legendy
    plt.legend(
        wedges, labels,
        title="Legenda: (Liczba narzędzi w danym roku)",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    plt.title("Procentowy podział narzędzi według roku dodania")
    plt.tight_layout()  # Automatyczne dopasowanie elementów
    plt.show()

def count_added_years(tools):
    """
    Liczy wystąpienia wartości 'added_year' w narzędziach.
    """
    years = [tool.added_year for tool in tools]
    return Counter(years)


class ToolDataVisualizer:
    def __init__(self, database_url):
        """
        Inicjalizacja klasy z konfiguracją połączenia do bazy danych.
        """
        self.database_url = database_url
        self.engine = create_engine(self.database_url)
        self.session = sessionmaker(bind=self.engine)()

    def fetch_tools(self):
        """
        Pobiera wszystkie narzędzia z bazy danych.
        """
        return self.session.query(Tool).all()

    def run(self):
        """
        Główna metoda uruchamiająca proces: pobranie danych, analiza i wizualizacja.
        """
        tools = self.fetch_tools()
        year_counts = count_added_years(tools)

        # Wyświetlanie wykresu kołowego
        display_pie_chart(year_counts)


if __name__ == "__main__":
    visualizer = ToolDataVisualizer(DATABASE_URL)
    visualizer.run()


