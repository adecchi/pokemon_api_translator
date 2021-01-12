import httpx

from src.utils import get_logger


logger = get_logger(__name__)


class Request:

    class HandlingError:
        def __call__(self, fn, *args, **kwargs):
            def inner(*a, **kw):
                try:
                    return fn(*a, **kw)
                except httpx._exceptions.TransportError as trans_err:
                    logger.critical(f"Transport Error. {trans_err}")
                    exception, msg = IOError, "Internal Error"
                except httpx._exceptions.HTTPStatusError as http_err:
                    logger.error(f"HTTP Error: {http_err}")
                    exception, msg = ValueError, f"HTTP Error. " \
                                                 f"The request failed with status code {http_err.response.status_code}"
                except Exception as unexpected_err:
                    logger.critical(f"Unexpected error: {unexpected_err}")
                    exception, msg = RuntimeError, "Unexpected error"
                raise exception(msg)
            return inner

    handling_errors = HandlingError

    @handling_errors()
    def get(self, url):
        """
        :param url: <string>. The url endpoint
        :return: Tuple(<int: status>, <Response: response>)
        """
        ssl_config = httpx.create_ssl_context()
        response = httpx.get(url, verify=ssl_config)
        if response.status_code == 200:
            status, response = True, response.json()
        else:
            status, response = False, response
        return status, response

    @handling_errors()
    def post(self, url, data):
        """
        :param url: <string>. The url endpoint
        :param data: <dict>. The data to post
        :return: Tuple(<int: status>, <Response: response>)
        """
        ssl_config = httpx.create_ssl_context()
        response = httpx.post(url, verify=ssl_config, data=data)
        if response.status_code == 200:
            status, response = True, response.json()
        else:
            status, response = False, response
        return status, response

