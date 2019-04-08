from abc import ABCMeta, abstractmethod


class AuthenticationStrategy(metaclass=ABCMeta):
    """
    This class represents an authentication strategy.
    """
    
    @abstractmethod
    def authenticate(self, **kwargs):
        """
        Given parameters, this authenticates the user to a provider and returns a credentials object.
        """
        raise NotImplementedError()

class AuthenticationException(Exception):
    pass