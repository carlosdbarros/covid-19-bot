import json
import requests

from requests.exceptions import ReadTimeout, ConnectTimeout

from consts import ApiCountry, ApiBrazilState, ApiBrazilCity
from utils import ParseDictAsObj, strip_accents, pasrse_json


def get_data_country(name: str):

    try:
        name = name.lower()
        response = requests.get( ApiCountry.URL_COUNTRIES.value.format(country=name), timeout=2 )
        data = pasrse_json(response.json())

        print(f"get_data_country >>> {response.status_code}")
        if response.status_code == 200 and not data.get("message", None):
            return data

    except Exception as exc:
        print(f"erro na requisão: {exc}")

    return None


def get_data_state(name: str):

    try:
        name = name.lower()
        response = requests.get(
            ApiBrazilState.URL_STATE.value.format(state=name), timeout=2
        )

        print(f"get_data_state >>> {response.status_code}")
        if response.status_code == 200:
            response = response.json()

            if not response.get('error', None):
                return pasrse_json(response)

            else:
                print( "estado não encontrado pela UF. Tentando buscar pelo nome do estado." )
                response = requests.get( ApiBrazilState.URL_STATES.value, timeout=2 )
                response = pasrse_json( response.json() ).get('data')

                name = strip_accents(name).lower()
                state = [ row for row in response if strip_accents(row['state']).lower() == name ]

                if state:
                    return state.pop()

    except Exception as exc:
        print(f"erro na requisição: {exc}")

    return None


def get_data_city(name: str):

    try:
        response = requests.get(ApiBrazilCity.URL_CITY.value, timeout=2)

        print(f"get_data_city >>> {response.status_code}")
        if response.status_code == 200:
            name = name.lower()
            data = response.json().get('docs')

            data_city = []
            for item in data:
                city_name = strip_accents( item["city_name"] ).lower()

                if city_name == name:
                    data_city.append(item)

            data_city.sort(key = lambda x: x["date"])

            print(f"get_data_city >>> {city_name}, {name}")

            return data_city.pop() if len(data_city) else None

    except Exception as exc:
        print(f"erro na requisão: {exc}")

    return None