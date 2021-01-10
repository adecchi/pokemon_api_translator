import httpx
import logging

FORMAT = "%(asctime)s %(name)-4s %(process)d %(levelname)-6s %(funcName)-8s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("Pokemon Translator")
log_level = logging.DEBUG
logger.setLevel(log_level)


class Request:

    def get(self, url):
        try:
            ssl_config = httpx.create_ssl_context()
            response = httpx.get(url, verify=ssl_config)
            if response.status_code == 200:
                status, response = True, response.json()
            else:
                status, response = False, response
            return status, response
        except Exception as ex:
            logger.error(f"Error Fetching(GET) url: {url} with error: {ex}")

    def post(self, url, data):
        try:
            ssl_config = httpx.create_ssl_context()
            response = httpx.post(url, verify=ssl_config, data=data)
            if response.status_code == 200:
                status, response = True, response.json()
            else:
                status, response = False, response
            return status, response
        except Exception as ex:
            logger.error(f"Error Fetching(POST) url: {url} with data {data} with error: {ex}")
