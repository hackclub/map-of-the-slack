from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler
from slack_sdk.web import WebClient
import os

def getClient():
	client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
	rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=1)

	client.retry_handlers.append(rate_limit_handler)

	return client