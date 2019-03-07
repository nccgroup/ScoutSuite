
class Facade:
    def __init__(self):
        self._client = None

    def _build_client(self):
        raise NotImplementedError()

    def _get_client(self):
        if self._client is None:
            self._client = self._build_client()
        return self._client