#!/usr/bin/python3

"""
This is the console module.

This module provides a command line interface for interacting with
the HBNB application.
"""

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from shlex import split
import cmd
import re


class HBNBCommand(cmd.Cmd):
    """
    A command line interpreter for HBNB.
    """
    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }


def parse(arg):
    """
    Parses the argument and returns a list of parts.
    It splits the argument based on square brackets '[]' or curly braces '{}'.

    Args:
        arg (str): The argument to parse.

    Returns:
        list: A list of parts of the argument.
    """

    squares = re.search(r"\[(.*?)\]", arg)
    curls = re.search(r"\{(.*?)\}", arg)
    if curls is None:
        if squares is None:
            return [i.strip(",") for i in split(arg)]
        else:
            isol = split(arg[:squares.span()[0]])
            parti = [i.strip(",") for i in isol]
            parti.append(squares.group())
            return parti
    else:
        isol = split(arg[:curls.span()[0]])
        parti = [i.strip(",") for i in isol]
        parti.append(curls.group())
        return parti


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def default(self, arg):
        """
        Default method that is called when none of
        the other do_* methods are applicable.
        It's used to handle unrecognized commands or syntax.

        Args:
            arg (str): The argument string.

        Returns:
            The return value of the called command method if the command
            is recognized, otherwise False.
        """

        command_dict = {
            "all": self.do_all,
            "count": self.do_count,
            "destroy": self.do_destroy,
            "show": self.do_show,
            "update": self.do_update
        }

        match = re.search(r"\.", arg)
        if match is not None:
            line_arg = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", line_arg[1])
            if match is not None:
                command = [line_arg[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in command_dict.keys():
                    call = "{} {}".format(line_arg[0], command[1])
                    return command_dict[command[0]](call)

        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, args):
        """ Create an object of any class"""
        try:
            if not args:
                raise SyntaxError()
            args_list = args.split(" ")
            key_w = {}
            for arg in args_list[1:]:
                tokenized = arg.split("=")
                tokenized[1] = eval(tokenized[1])
                if type(tokenized[1]) is str:
                    tokenized[1] = tokenized[1].replace("_", " ").replace('"', '\\"')
                key_w[tokenized[0]] = tokenized[1]
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        obj = HBNBCommand.classes[args_list[0]](**key_w)
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based
        on the class name and id.

        Args:
            arg (str): The class name and id of the instance.
        """

        line_arg = parse(arg)
        obj_dict = storage.all()

        if len(line_arg) == 0:
            print("** class name missing **")
        elif line_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")

        elif len(line_arg) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(line_arg[0], line_arg[1]) not in obj_dict:
            print("** no instance found **")

        else:
            print("{}.{}".format(line_arg[0], line_arg[1]))

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id.

        Args:
            arg (str): The class name and id of the instance.
        """
        line_arg = parse(arg)
        obj_dict = storage.all()

        if len(line_arg) == 0:
            print("** class name missing **")
        elif line_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")

        elif len(line_arg) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(line_arg[0], line_arg[1]) not in obj_dict:
            print("** no instance found **")

        else:
            del obj_dict["{}.{}".format(line_arg[0], line_arg[1])]
            storage.save()

    def do_all(self, arg):
        """
        Prints all instances of a class, or all instances
        of all classes if no class name is given.

        Args:
            arg (str): The name of the class.
        """
        line_arg = parse(arg)

        if len(line_arg) > 0 and line_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")

        else:
            obj_list = []
            zipped_values = storage.all().values()
            for obj in zipped_values:
                if len(line_arg) > 0 and line_arg[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(line_arg) == 0:
                    obj_list.append(obj.__str__())

            print(obj_list)

    def do_count(self, arg):
        """
        Counts the number of instances of a given class.
        """
        line_arg = parse(arg)
        counter = 0
        for obj in storage.all().values():
            if line_arg[0] == obj.__class__.__name__:
                counter += 1
        print(counter)

    def do_update(self, arg):
        """
        Updates an instance based on the class name
        and id by adding or updating an attribute.

        Args:
            arg (str): The class name, id, attribute name, and attribute value.
        """
        line_arg = parse(arg)
        obj_dict = storage.all()

        if len(line_arg) == 0:
            print("** class name missing **")
            return False

        elif line_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False

        elif len(line_arg) == 1:
            print("** instance id missing **")
            return False

        elif "{}.{}".format(line_arg[0], line_arg[1]) not in obj_dict:
            print("** no instance found **")

        elif len(line_arg) == 2:
            print("** attribute name missing **")
            return False

        elif len(line_arg) == 3:
            try:
                type(eval(line_arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(line_arg) == 4:
            obj = obj_dict["{}.{}".format(line_arg[0], line_arg[1])]

            if line_arg[2] in obj.__class__.__dict__.__keys():
                value_type = type(obj.__class__.__dict__[line_arg[2]])
                obj.__dict__[line_arg[2]] = value_type(line_arg[3])

        elif type(eval(line_arg[2])) == dict:
            obj = obj_dict["{}.{}".format(line_arg[0], line_arg[1])]
            for k, v in eval(line_arg[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt."""
        pass

    def do_EOF(self, arg):
        """EOF or quit command to exit program"""
        return True

    do_quit = do_EOF


if __name__ == '__main__':
    HBNBCommand().cmdloop()
