import requests
import logging
import json
import random

class Checker:
    def request_check(self):

        logging.basicConfig(level=logging.INFO, filename="log_files/checker_log.log", filemode="a")

        with open("data_files/user_agents.json", "r") as agents:
            user_agents = json.load(agents)["agents"]

        headers = {
            "User-Agent": random.choice(user_agents)
        }

        list_of_good_cods = [200, 201, 202, 204, 300, 301, 302, 304, 307, 308]
        list_of_bad_cods = [500, 502, 503, 504, 520, 522]

        with open("data_files/domains.json", "r") as f:
            domains = json.load(f)

        text = ""

        try:
            for url in domains["domains"]:
                try:
                    clean_url = url["domain"]


                    request = requests.get(f"https://{clean_url}", headers=headers)

                    if request.status_code in list_of_good_cods:
                        result = f"✅ Сайт работает: {clean_url}, код: {request.status_code}"
                        text += result + "\n"
                    if request.status_code in list_of_bad_cods:
                        result = f"❌ Сайт не работает: {clean_url}, код ошибки: {request.status_code}"
                        text += result + "\n"

                except Exception as e:
                    logging.info(f"ПРОИЗОШЛА ОШИБКА В ТЕЛЕ ЦИКЛА: {e}")

        except Exception as e:
            logging.info(f"ПРОИЗОШЛА ОШИБКА В ТЕЛЕ ЦИКЛА ЧЕКЕРА: {e}")

        return text



check_d = Checker()