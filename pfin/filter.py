# import logging

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
                 product_in: bool = None,
                 human_in: bool = None,
                 institutional: bool = None,
                 picture_format: bool = None,
                 author_credits: str = None,
                 limited_usage: bool = None,
                 copyrighted: bool = None,
                 usage_end: int = None,
                 tags: list = None,
                 ):
        """
        :param str text_filter:
        :param str image_type: Type of image. Can be any of {'PassionFroid', 'Fournisseur', 'Logo'}
        :param bool product_in: Whether a product is in the picture
        :param bool human_in: Whether a human is in the picture
        :param bool institutional: Whether the picture is institutional
        :param bool picture_format: Which format is the picture. True for vertical, False for horizontal.
        :param str author_credits: Similar to the text filter, for author credits.
        :param bool limited_usage: Whether the picture's usage is limited.
        :param bool copyrighted: Whether the image is copyrighted. Is dependent on limited_usage.
        :param int usage_end: Date of end of usage rights.
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
        self._copyrighted = copyrighted
        self._usage_end = usage_end
        self._tags = tags

    def tags(self) -> str:
        field = 'tags'
        query = '{'
        if len(self._tags) > 1:
            operator = '$and'
            query += f'"{operator}": '
            query += '['
            for tag in self._tags:
                query += '{'
                query += f'"fields.{field}": ' + '{"$regex": ' + f'".*{tag}.*' + '"}'
                query += '},'
            else:
                query = query[:-1]  # Remove the trailing comma.
            query += ']'
        elif len(self._tags) == 1:
            tag = self._tags[0]
            query += f'"fields.{field}": ' + '{"$regex": ' + f'".*{tag}.*' + '"}'
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

        if self._tags is not None:
            queries.append(self.tags())

        query = self.aggregate_all_queries(queries)
        if query is not None:
            # logging.debug(f'{query=}')
            return decode_json(query)
        else:
            return {}
