from datetime import datetime

import pyperclip
import requests
from typing import Optional, Type, List, Dict
from pydantic import BaseModel, Field
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.service import Controller
import logging

logger = logging.getLogger(__name__)

class Tweet(BaseModel):
    username: str
    tweet_text: str
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    url: str = ""


class TwitterUser(BaseModel):
    username: str
    total_posts: int = 0
    total_engagement: int = 0  # sum of likes, retweets, replies
    tweets: List[Tweet] = Field(default_factory=list)


class Contributors(BaseModel):
    contributors: List[TwitterUser] = Field(default_factory=list)


class TweetList(BaseModel):
    tweets: List[Tweet] = Field(default_factory=list)


class CustomTwitterController(Controller):
    def __init__(self, exclude_actions: list[str] = [],
                 output_model: Optional[Type[BaseModel]] = None
                 ):
        super().__init__(exclude_actions=exclude_actions, output_model=output_model)
        self._register_custom_actions()

    def _register_custom_actions(self):
        """Register all custom browser actions"""

        @self.registry.action("Copy text to clipboard")
        def copy_to_clipboard(text: str):
            pyperclip.copy(text)
            return ActionResult(extracted_content=text)

        @self.registry.action("Paste text from clipboard")
        async def paste_from_clipboard(browser: BrowserContext):
            text = pyperclip.paste()
            page = await browser.get_current_page()
            await page.keyboard.type(text)

            return ActionResult(extracted_content=text)

        @self.registry.action("Aggregate tweets by user", param_model=TweetList)
        def aggregate_tweets(params: TweetList):
            """Aggregate tweets by username and compute engagement metrics."""
            try:
                logger.info(f"Aggregating {len(params.tweets)} tweets by username")

                users_dict: Dict[str, TwitterUser] = {}

                for tweet in params.tweets:
                    username = tweet.username

                    engagement = tweet.likes + tweet.retweets + tweet.replies

                    if username not in users_dict:
                        users_dict[username] = TwitterUser(
                            username=username,
                            total_posts=1,
                            total_engagement=engagement,
                            tweets=[tweet]
                        )
                    else:
                        users_dict[username].total_posts += 1
                        users_dict[username].total_engagement += engagement
                        users_dict[username].tweets.append(tweet)

                # Convert to list and sort by engagement and post count
                users_list = list(users_dict.values())
                users_list.sort(key=lambda x: (x.total_engagement, x.total_posts), reverse=True)

                # Get top 10 contributors
                top_contributors = Contributors(contributors=users_list[:10])

                logger.info(f"Successfully aggregated tweets. Found {len(users_dict)} unique users.")
                return ActionResult(
                    extracted_content=top_contributors.model_dump_json(),
                    include_in_memory=True
                )
            except Exception as e:
                logger.error(f"Error aggregating tweets: {str(e)}")
                return ActionResult(
                    extracted_content=f"Error aggregating tweets: {str(e)}",
                    include_in_memory=True
                )

        @self.registry.action("Send data to external API", param_model=Contributors)
        def send_contributors_to_external_api(params: Contributors):
            """Send the top contributors data to external API."""
            try:
                api_url = "https://7005-95-181-173-6.ngrok-free.app/api"
                logger.info(f"Sending {len(params.contributors)} contributors to external API")

                data = {
                    "content": {
                        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "contributors": params.model_dump()["contributors"]
                    }
                }

                response = requests.post(
                    api_url,
                    json=data,
                    headers={"Content-Type": "application/json"}
                )

                response_status = "success" if response.status_code == 200 else f"error: {response.status_code}"
                message = f"Data sent to API with status: {response_status}"

                logger.info(message)
                return ActionResult(
                    extracted_content=message,
                    include_in_memory=True
                )
            except Exception as e:
                error_message = f"Error sending data to API: {str(e)}"
                logger.error(error_message)
                return ActionResult(
                    extracted_content=error_message,
                    include_in_memory=True
                )