from typing import overload
import utils


class Element:
    def __init(self, camel_case=True, **kwargs) -> None:
        for key, value in kwargs.items():
            if camel_case:
                key = utils.camel_to_snake(key)

            if type(value) == dict:
                setattr(self, key, Element(camel_case=camel_case, **value))
            elif type(value) == list:
                setattr(self, key, [Element(
                    camel_case=camel_case, **item) if type(item) == dict else item for item in value])
            elif value is not None:
                setattr(self, key, value)

    def __copy(self, element):
        for key, value in element.__dict__.items():
            setattr(self, key, value)

    def __init__(self, element=None, *, camel_case=True, **kwargs) -> None:
        if element:
            self.__copy(element)
        self.__init(camel_case=camel_case, **kwargs)

    def clone(self):
        return Element(False, **self.as_dict(False))

    def as_dict(self, camel_case=True):
        # return {utils.snake_to_camel(key): value.as_dict() if type(value) == Element else value for key, value in self.__dict__.items()}
        ret = {}
        for key, value in self.__dict__.items():
            if camel_case:
                key = utils.snake_to_camel(key)

            if type(value) == Element:
                ret[key] = value.as_dict(camel_case)
            elif type(value) == list:
                if value:
                    ret[key] = [item.as_dict(camel_case) if type(
                        item) == Element else item for item in value]
            elif value is not None:
                ret[key] = value

        return ret
