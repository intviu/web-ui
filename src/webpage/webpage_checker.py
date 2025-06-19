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

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/114.0.0.0 Safari/537.36"
            }

            # Try HEAD request first
            response = requests.head(self.url, headers=headers, allow_redirects=True, timeout=15)

            # If HEAD gives 403 or isn't reliable, fallback to GET
            if response.status_code == 403 or response.status_code >= 400:
                logger.warning(f"HEAD request got status {response.status_code}, trying GET instead...")
                response = requests.get(self.url, headers=headers, allow_redirects=True, timeout=15)

            write_data_to_file(
                agents_name="Webpage Checker",
                number_of_tries=1,
                time_taken=1,
                user_input=self.url,
                output=f"{response.status_code} - {response.reason}"
            )

            logger.info(f"Response: {response.status_code} - {response.reason}")
            return response.status_code == 200

        except requests.RequestException as e:
            logger.error("Error checking URL: %s", e)
            return False
