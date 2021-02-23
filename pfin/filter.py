import logging

from .utils import decode_json

from typing import List


class Filter:

    """

    This class implements a `Filter` object.
    It will be used to forge advanced queries.

    """

    def __init__(self,
                 text_filter: str = None,
                 image_type: str = None,
                 product_in: str = None,
                 human_in: str = None,
                 institutional: str = None,
                 picture_format: str = None,
                 author_credits: str = None,
                 limited_usage: str = None,
                 usage_end: int = None,
                 tags: list = None,
                 ):
        """
        :param str text_filter: A search to apply on the file name. Hint: it's useless.
        :param str image_type: Type of image. Can be any of {'PassionFroid', 'Fournisseur', 'Logo'}
        :param bool product_in: Whether a product is in the picture
        :param bool human_in: Whether a human is in the picture
        :param bool institutional: Whether the picture is institutional
        :param bool picture_format: Which format is the picture. True for vertical, False for horizontal.
        :param str author_credits: Similar to the text filter, for author credits.
        :param bool limited_usage: Whether the picture's usage is limited.
        :param list tags: A list of tags. An "and" operator is used.
        """
        self._global_operator = True
        self._text_filter = text_filter
        self._image_type = image_type
        self._product_in = product_in
        self._human_in = human_in
        self._institutional = institutional
        self._picture_format = picture_format
        self._author_credits = author_credits
        self._limited_usage = limited_usage
        self._tags = tags

    def text_filter(self) -> str:
        field = 'id'
        value = self._text_filter
        query = '{'
        query += f'"{field}": ' + '{"$regex": ' + f'"{value}"' + '}'
        query += '}'
        return query

    def image_type(self) -> str:
        field = 'image_type'
        value = self._image_type
        query = '{'
        query += f'"{field}": "{value}"'
        query += '}'
        return query

    def product_in(self) -> str:
        field = 'product_in'
        value = self._product_in
        query = '{'
        query += f'"{field}": "{value}"'
        query += '}'
        return query

    def human_in(self) -> str:
        field = 'human_in'
        value = self._human_in
        query = '{'
        query += f'"{field}": "{value}"'
        query += '}'
        return query

    def institutional(self) -> str:
        field = 'institutional'
        value = self._institutional
        query = '{'
        query += f'"{field}": "{value}"'
        query += '}'
        return query

    def picture_format(self) -> str:
        field = 'institutional'
        value = self._institutional
        query = '{'
        query += f'"{field}": "{value}"'
        query += '}'
        return query

    def author_credits(self) -> str:
        field = 'id'
        value = self._text_filter
        query = '{'
        query += f'"{field}": ' + '{"$regex": ' + f'"{value}"' + '}'
        query += '}'
        return query

    def limited_usage(self) -> str:
        field = 'limited_usage'
        value = self._limited_usage
        query = '{'
        query += f'"{field}": "{value}"'
        query += '}'
        return query

    def tags(self) -> str:
        field = 'tags'
        query = '{'
        if len(self._tags) > 1:
            operator = '$and'
            query += f'"{operator}": '
            query += '['
            for tag in self._tags:
                query += '{'
                query += f'"{field}": ' + '{"$regex": ' + f'".*{tag}.*' + '"}'
                query += '},'
            else:
                query = query[:-1]  # Remove the trailing comma.
            query += ']'
        elif len(self._tags) == 1:
            tag = self._tags[0]
            query += f'"{field}": ' + '{"$regex": ' + f'".*{tag}.*' + '"}'
        query += '}'
        return query

    def aggregate_all_queries(self, queries: List[str]) -> str or None:
        if len(queries) > 1:
            operator = "$and" if self._global_operator else "$or"
            query = '{'
            query += f'"{operator}": ['
            for q in queries:
                query += f'{q},'
            else:
                query = query[:-1]
            query += ']}'
        elif len(queries) == 1:
            query = queries[0]
        else:
            query = None
        return query

    def forge_query(self) -> dict:
        queries = []

        # We explicit "is not None" because some values are boolean.

        if self._text_filter is not None:
            queries.append(self.text_filter())

        if self._image_type is not None:
            queries.append(self.image_type())

        if self._product_in is not None:
            queries.append(self.product_in())

        if self._human_in is not None:
            queries.append(self.human_in())

        if self._institutional is not None:
            queries.append(self.institutional())

        if self._picture_format is not None:
            queries.append(self.picture_format())

        if self._author_credits is not None:
            queries.append(self.author_credits())

        if self._limited_usage is not None:
            queries.append(self.limited_usage())

        if self._tags is not None:
            queries.append(self.tags())

        query = self.aggregate_all_queries(queries)
        if query is not None:
            logging.debug(f'{query=}')
            return decode_json(query)
        else:
            return {}
