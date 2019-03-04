from hashlib import sha1


def get_non_provider_id(name):
        """
        Not all resources have an ID and some services allow the use of "." in names, which breaks Scout's
        recursion scheme if name is used as an ID. Use SHA1(name) instead.

        :param name:                    Name of the resource to
        :return:                        SHA1(name)
        """
        _hash = sha1()
        _hash.update(name.encode('utf-8'))
        return _hash.hexdigest()
