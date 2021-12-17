import pytest
from figure_hook.Factory.publish_factory.plurk_content_factory import \
    PlurkContentFactory


class TestPlurkContentFactory:
    @pytest.mark.usefixtures("release_feed")
    def test_plurk_release_content_creation(self, release_feed):
        plurk = PlurkContentFactory.create_new_release(release_feed)
        assert plurk

    class TestContentMaker:
        """
        https://www.plurk.com/API#:~:text=Error%20returns%3A-,/APP/Timeline/plurkAdd,-requires%20user%27s%20access

        ## /APP/Timeline/plurkAdd

        Required params: `content`, `qualifier`
        Optional params: `limited_to`, `excluded`, `no_comments`,
        `lang`, `replurkable`, `porn`, `publish_to_followers`, `publish_to_anonymous`
        """

        def make_expected_content(
            self,
            content,
            qualifier,
            limited_to=[],
            excluded=None,
            no_comments=0,
            lang='en',
            replurkable=1,
            porn=0,
            publish_to_followers=1,
            publish_to_anonymous=1
        ):
            obj = {
                'content': content,
                'qualifier': qualifier,
                'limited_to': str(limited_to),
                'no_comments': no_comments,
                'lang': lang,
                'replurkable': replurkable,
                'porn': porn,
                'publish_to_followers': publish_to_followers,
                'publish_to_anonymous': publish_to_anonymous
            }

            if excluded:
                obj['excluded'] = excluded

            return obj

        def test_plurk_content_maker(self):
            content = "content"
            qualifier = 'plays'

            expected = self.make_expected_content(
                content,
                qualifier,
            )

            content = PlurkContentFactory.create(
                content=content,
                qualifier=qualifier,
            )

            assert content == expected
