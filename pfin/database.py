import os
import random
import shelve
import pymongo
import logging

from typing import List

from .user import User
from .image import Image
from .filter import Filter
from .config import PFIN_SERVER, IMAGE_HOST_URL
from .utils import hash_password


class Database:

    srv_args: str = '?retryWrites=true&w=majority'

    def __init__(self, database_name: str, collection_name: str):
        # Create client (connect to the server)
        self._client = pymongo.MongoClient(f"{PFIN_SERVER}{self.srv_args}")

        # Select database and collection
        self._select_database(database_name)
        self._select_collection(collection_name)

        self._preprocess()

    def _preprocess(self) -> None:
        """
        Is in charge of creating the cache, which will hold often-computed information.
        """
        self.cache = Cache(self._db, self._collection)

    def _select_database(self, db_name: str) -> None:
        """
        Select instance's database.

        :param str db_name: The name of the database we want to switch to.
        :raises ValueError: If the database name is invalid.
        """
        available_databases = self._client.list_database_names()
        if db_name not in available_databases:
            raise ValueError(f'Invalid database name {db_name!r}. '
                             f'Pick one from {available_databases}')

        logging.info(f'Selecting database {db_name!r}')
        self._db: pymongo.database.Database = self._client.get_database(db_name)

    def _select_collection(self, collection_name: str) -> None:
        """
        Select instance's collection

        :param str collection_name: The name of the collection we want to switch to.
        :raises ValueError: If the database name is invalid.
        """
        available_collections = self._db.list_collection_names()
        if collection_name not in available_collections:
            raise ValueError(f'Invalid collection name {collection_name!r}. '
                             f'Pick one from {available_collections}')

        logging.info(f'Selecting collection {collection_name!r}')
        self._collection: pymongo.collection.Collection = self._db.get_collection(collection_name)


class ImageDatabase(Database):

    def get_x_random_images(self, limit: int = 10, additional_filter: dict = None) -> List[Image]:
        if additional_filter is None:
            additional_filter = {}
        images = list(self._collection.find(additional_filter, limit=limit * 5))
        random.shuffle(images)
        return [Image(info) for info in images[:limit]]

    def create_filter_from_args(self, args: dict) -> Filter:
        """
        Takes the arguments of a Flask (HTTP) request,
        and returns a corresponding Filter for an Image search.
        """
        keys = set(args.keys())
        filter_args = {}

        f = Filter(**filter_args)
        return f

    def search(self, f: Filter, limit: int = 0) -> List[Image]:
        """
        Searches the database using a filter.

        :param Filter f: The Filter instance to use.
        :param int limit: The maximum number of items we want to return.
        :return list: List of images if some were found, empty otherwise.
        """
        query = f.forge_query()
        returned_events = self._collection.find(query).limit(limit)
        return [Image(info['fields']) for info in returned_events]


class UserDatabase(Database):

    def does_user_exist(self, email_address: str) -> bool:
        """
        Takes an email address, and returns a boolean indicating whether
        the user exists in the database (True if it does, False otherwise).
        """
        search = {'email': email_address}
        result = self._collection.find(search)
        return True if result.retrieved == 1 else False

    def get_user_information(self, email_address: str):
        search = {'email': email_address}
        return self._collection.find_one(search)

    def login_user(self, email: str, password: str) -> User or None:
        """
        :param str email: The user's email address, used for authentication.
        :param str password: The clear text password
        :return User|None: User if the information is valid, None otherwise.
        """
        requested_user_info = self.get_user_information(email)

        if requested_user_info is None:
            # The user does not exist.
            return

        if hash_password(password) != requested_user_info['password']:
            # The password is invalid.
            return

        user = User(requested_user_info)
        return user


class Cache:

    cache_folder: str = '.cache/pfin/'

    def __init__(self, db, collection):
        self.create_cache_dir()
        self._empty_cache()

        self._db = db
        self._collection = collection

    def create_cache_dir(self) -> None:
        """
        Creates the cache directory.
        """
        try:
            os.makedirs(self.cache_folder)
        except FileExistsError:
            pass

    def _empty_cache(self) -> None:
        # Removes all the files contained in the cache folder
        for fl in os.listdir(self.cache_folder):
            os.remove(os.path.join(self.cache_folder, fl))

    def _get_db(self, db_name: str) -> shelve.DbfilenameShelf:
        """
        Gets the database specified.
        Creates it if not present.
        Needs for the parent directory to exist.

        :param str db_name: The database name (the file name).
        :return shelve.DbfilenameShelf:
        """
        db_path = os.path.join(self.cache_folder, db_name)
        db = shelve.open(db_path)
        logging.info(f'Opened cache file {db_path!r}')
        return db
