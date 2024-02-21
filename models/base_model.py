#!/usr/bin/python3
"""
Module containing the BaseModel class.
"""

from sqlalchemy.ext.declarative import declarative_base
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class BaseModel:
    """
    The BaseModel class for the cmd Airbnb console project.

    Attributes:
        id (str): The unique identifier for each instance.
        created_at: The datetime representing instance creation time.
        updated_at: The datetime representing instance last update time.
    """

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        If kwargs are provided, it sets the attributes of the instance
        based on the key-value pairs in kwargs.
        If 'created_at' or 'updated_at' are in kwargs,
        it converts them to datetime objects.
        If kwargs are not provided, it generates a unique id
        and the current datetime for 'created_at' and 'updated_at'.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':

                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the instance.

        The string includes the class name, id, and dictionary of the instance.
        """
        return (
            f"[{self.__class__.__name__}] "
            f"({self.id})"
            f"{self.__dict__}"
        )

    def save(self):
        """
        Updates the 'updated_at' attribute to current datetime
        and saves the instance.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the instance.

        The dictionary includes all attributes of the instance.
        If 'created_at' or 'updated_at' are attributes of the instance
        and are datetime objects, it converts them to ISO format strings.
        """

        dict = self.__dict__
        dict['__class__'] = self.__class__.__name__

        if 'created_at' in dict and isinstance(dict['created_at'], datetime):
            dict['created_at'] = dict['created_at'].isoformat()
        if 'updated_at' in dict and isinstance(dict['updated_at'], datetime):
            dict['updated_at'] = dict['updated_at'].isoformat()

        return dict

    def delete(self):
        """ delete object
        """
        models.storage.delete(self)
