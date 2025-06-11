import requests
import logging
logger = logging.getLogger(__name__)
from ..outputdata.output_data import write_data_to_file

class WebpageChecker:
    def __init__(self, url) -> None:
        logger.info("Initializing WebpageChecker...")
        self.url = url

    def exists(self):
        try:
            logger.info(f"Checking if the webpage {self.url} exists...")
            response = requests.head(self.url, allow_redirects=True, timeout=5)
            write_data_to_file(
                agents_name="Webpage Checker",
                number_of_tries=1,
                time_taken=1,
                user_input=self.url,
                output=f"{response.status_code} - {response.reason}"
            )
            return True if response.status_code == 200 else False
        except requests.RequestException as e:
            logger.error("Error checking URL: %s", e)
            return False