import requests
from dataclasses import dataclass
import pytest
from bs4 import BeautifulSoup
import re

@dataclass
class ProgrammingLanguage:
    name: str
    popularity: str
    frontend: str
    backend: str

def get_programming_languages():
    url = "https://en.wikipedia.org/wiki/Programming_languages_used_in_most_popular_websites"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    languages = []
    table = soup.find("table", {"class": "wikitable"})
    rows = table.find_all("tr")[1:]

    for row in rows:
        data = row.find_all("td")
        if len(data) >= 4:
            language = ProgrammingLanguage(
                name=data[0].text.strip(),
                popularity=data[1].text.strip(),
                frontend=data[2].text.strip(),
                backend=data[3].text.strip()
            )
            languages.append(language)

    return languages

languages_data = get_programming_languages()

@pytest.mark.parametrize("threshold", [10**7, 1.5 * 10**7, 5 * 10**7, 10**8, 5 * 10**8, 10**9, 1.5 * 10**9])
def test_popularity_threshold(threshold):
    print(f"ПРОВЕРКА ПОРОГА {threshold}")
    errors = []
    for language in languages_data:
        cleaned_popularity = re.sub(r'[^\d]', '', language.popularity)  # Извлечение только чисел из строки
        print(f"Проверка языка {language.name} популярность: {cleaned_popularity}")
        if cleaned_popularity and int(cleaned_popularity) < threshold:
            error_message = f"{language.name} (Frontend: {language.frontend}|Backend: {language.backend}) has {language.popularity} unique visitors per month. (Expected more than {threshold})"
            errors.append(error_message)
   
    if errors:
        for error in errors:
            print(error)
        raise AssertionError(f"Есть строки с популярностью ниже порога {threshold}")
    else:
        print(f"Все языки программирования выше порога {threshold}")

thresholds = [10**7, 1.5 * 10**7, 5 * 10**7, 10**8, 5 * 10**8, 10**9, 1.5 * 10**9]

for threshold_value in thresholds:
    try:
        test_popularity_threshold(threshold_value)
    except AssertionError as e:
        print(e)
        continue
