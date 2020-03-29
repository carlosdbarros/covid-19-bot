import os
import time
import json
import requests

from datetime import datetime, date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 

from utils import strip_accents
from utils import ParseDictAsObj, download_img
from consts import ApiCountry, UrlFlag, WppElementIdentifier, Messages


class WppBot:
    dir_path = os.getcwd()
    chromedriver = os.path.join(dir_path, "chromedriver")
    profile = os.path.join(dir_path, "profile", "wpp")

    def __init__(self, name):
        self.name = name
        self.options = webdriver.ChromeOptions()
        self.options.add_argument( r"user-data-dir={}".format(self.profile) )
        self.driver = webdriver.Chrome(self.chromedriver, chrome_options=self.options)
        self.driver.get("https://web.whatsapp.com/")
        self.driver.implicitly_wait(15)

    def get_last_msg(self):
        """ Captura a ultima mensagem da conversa """
        try:
            post = self.driver.find_elements_by_class_name(WppElementIdentifier.CHAT_MESSAGES.value)
            last = len(post) - 1
            text = post[last].find_element_by_css_selector("span.selectable-text").text

            return text

        except Exception as exc:
            print( f"Erro ao ler msg, tentando novamente!\n{exc}" )

    def send_msg(self, msg):
        """ Envia uma mensagem para a conversa aberta """

        try:
            self.message_box = self.driver.find_element_by_class_name(WppElementIdentifier.MESSAGE_BOX.value)

            for row in msg.split('\n'):
                ActionChains(self.driver).send_keys(row).perform()
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

            ActionChains(self.driver).send_keys(Keys.RETURN).perform()

        except Exception as exc:
            print( f"Erro ao enviar msg: {exc}" )

    def send_media(self, fileToSend, description=''):
        """ Envia media """

        try:
            self.driver.find_element_by_css_selector(WppElementIdentifier.ICON_CLIP.value).click()

            attach = self.driver.find_element_by_css_selector(WppElementIdentifier.ICON_IMAGE_INPUT.value)
            attach.send_keys(fileToSend)

            self.driver.find_element_by_class_name(WppElementIdentifier.DESCRIPTION_IMAGE.value).click()

            for row in description.split('\n'):
                ActionChains(self.driver).send_keys(row).perform()
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

            ActionChains(self.driver).send_keys(Keys.RETURN).perform()

        except Exception as exc:
            print( f"Erro ao enviar media: {exc}" )

    def format_msg_country(self, data, name):
        result = Messages.NOT_FOUND_COUNTRY.value

        if isinstance(data, dict):
            country = ParseDictAsObj(data)
            download_img(country.countryInfo.flag)

            result = (
                f"Total: {country.cases}\n"
                f"Casos hoje: {country.todayCases}\n"
                f"Mortes: {country.deaths}\n"
                f"Mortes hoje: {country.todayDeaths}\n"
                f"Recuperados: {country.recovered}\n"
                f"Críticos: {country.critical}"
            )

        return result

    def format_msg_state(self, data, name):
        result = Messages.NOT_FOUND_STATE.value

        if isinstance(data, dict):
            state = ParseDictAsObj(data)
            name = strip_accents(state.state).lower().replace(' ', '-')

            flag = download_img(UrlFlag.URL_FLAG_STATE.value.format(
                state = name if name != 'sao-paulo' else name+'1'
            ))

            result = (
                f"UF: {state.uf}\n"
                f"Estado: {state.state}\n"
                f"Confirmados: {state.cases}\n"
                f"Suspeitos: {state.suspects}\n"
                f"Casos descartados: {state.refuses}\n"
                f"Mortes: {state.deaths}"
            )

        return result, flag

    def format_msg_city(self, data, name):
        result = Messages.NOT_FOUND_CITY.value

        if isinstance(data, dict):
            city = ParseDictAsObj(data)

            is_today = city.date == date.today().strftime("%Y-%m-%d")
            cases = city.date if is_today else 0

            result = (
                f"UF: {city.state}\n"
                f"Cidade: {city.city_name}\n"
                f"Total: {city.count}\n"
                f"Casos hoje: {cases}\n"
            )

        return result
