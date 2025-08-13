class AppException(Exception):
    """Base Exception"""
    notify = "Base Exception"

    def __init__(self, *args, **kwargs):
        data = "No data"
        if kwargs:
            data = ''.join([f"{k} = {v}\n" for k, v in kwargs.items()])
        self.message = data
        self.notify_info = f"{self.notify} with: {self.message}"

    def __str__(self):
        return (
            f"Error.\n"
            f"type: {self.__class__.__name__}\n"
            f"notify info: {self.notify_info}"
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"
