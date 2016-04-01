from gifbot.helpers.google_gif_search_helper import google_image_search

class GifNotFoundException(Exception):
    """
    Exception when no GIF could be found
    """
    pass


class GifSearchService(object):
    """
    Abstract base class
    """

    def search(self, query):
        """
        :param query: the search query in string
        :return: an array of URLs of all the search results
        :raise GifNotFoundException: when no GIF could be found
        """
        raise NotImplementedError

    @classmethod
    def get_default(cls):
        """
        :return: factory method that returns the default implementation
        """
        return GoogleGifSearchService()


class GoogleGifSearchService(GifSearchService):
    """
    Implementation based on Google image search API
    """

    def search(self, query):
        urls = google_image_search(query + ' gif')

        if len(urls) == 0:
            raise GifNotFoundException()

        # exclude non-GIF images if there are sufficient amount of GIFs
        gif_urls = [url for url in urls if url.endswith('.gif')]

        return gif_urls if len(gif_urls) > 2 else urls
