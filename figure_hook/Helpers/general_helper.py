from figure_hook.Models import Webhook


class DataHelper:
    @staticmethod
    def webhook_supporting_languages():
        return Webhook.supporting_langs
