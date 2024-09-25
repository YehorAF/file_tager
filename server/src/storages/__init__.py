import abc


class Storage(abc.ABC):
    @abc.abstractmethod
    def save_file():
        pass


    @abc.abstractmethod
    def remove_file():
        pass


    @abc.abstractmethod
    def load_file():
        pass


    @abc.abstractmethod
    def get_file_information():
        pass