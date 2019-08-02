from app.http.constants import RequestMethod
from app.http.entities import Request

import logging

logger = logging.getLogger(__name__)


class RestClient:

    @staticmethod
    def get_html(url):
        logger.info('[GET] %s', url)
        request = Request(url, method=RequestMethod.GET)
        request.add_header('Content-Type', 'text/html')
        request.add_header('Accept', 'text/html')

        http_response = request.send()
        response_data = http_response.read()
        return response_data.decode('utf-8')
