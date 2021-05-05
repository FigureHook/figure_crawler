import pytest
from discord import RequestsWebhookAdapter, Webhook

from utils.data_access import make_discord_webhooks


@pytest.mark.usefixtures("session")
class TestDataAccess:
    def test_make_webhooks(self):
        adapter = RequestsWebhookAdapter()
        webhooks = make_discord_webhooks(adapter)
        for webhook in webhooks:
            assert isinstance(webhook, Webhook)
