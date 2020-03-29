from enum import Enum


class ApiCountry(Enum):
    URL_COUNTRIES = "https://corona.lmao.ninja/countries/{country}?strict=true"
    # URL_COUNTRIES = "https://covid19-brazil-api.now.sh/api/report/v1/countries"
    URL_COUNTRY = "https://covid19-brazil-api.now.sh/api/report/v1/{country}"
    ALL_COUNTRY_CASES = "https://corona.lmao.ninja/all"


class ApiBrazilState(Enum):
    URL_STATES = "https://covid19-brazil-api.now.sh/api/report/v1"
    URL_STATE = "https://covid19-brazil-api.now.sh/api/report/v1/brazil/uf/{state}"


class ApiBrazilCity(Enum):
    URL_CITY = "https://especiais.g1.globo.com/bemestar/coronavirus/mapa-coronavirus/data/brazil-cases.json"


class UrlJson(Enum):
    COUNTRIES = "https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-abbreviation.json"
    BRAZIL_STATES = "https://raw.githubusercontent.com/gcorreaalves/brazil-states-cities-json/master/states.json"


class UrlFlag(Enum):
    URL_FLAG_STATE = "https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{state}.png?x64851"
    URL_FLAG_COUNTRY_CODE = "https://flagpedia.net/data/flags/ultra/{code}.png"
    URL_FLAG_COUNTRY_NAME = "https://www.countries-ofthe-world.com/flags-normal/flag-of-{country}.png"


class Messages(Enum):
    NOT_FOUND_COUNTRY = "Não foi possível recuperar as informações deste país."
    NOT_FOUND_STATE = "Não foi possível recuperar as informações deste estado."
    NOT_FOUND_CITY = "Não foi possível recuperar as informações deste cidade."
    HELP_TEXT = "Commands\n/covid country name\n/covidbr state name or UF\n/covidcity city name"
    # HELP_TEXT = "Commands\n/covid nome do país\n/covidbr nome do estado ou UF\n/covidcity nome da cidade"


class WppElementIdentifier(Enum):
    CHAT_MESSAGES = "Tkt2p"
    MESSAGE_BOX = "_2WovP"
    BTN_SEND_MESSAGE_BOX = "_35EW6"
    ICON_CLIP = "span[data-icon='clip']"
    ICON_IMAGE_INPUT = "input[type='file']"
    DESCRIPTION_IMAGE = "_1ZxJu"
    BTN_SEND_IMAGE = "//div[contains(@class, 'yavlE')]"
