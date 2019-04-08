from hashlib import sha1


def get_non_provider_id(name):
        """
        Not all resources have an ID and some services allow the use of "." in names, which break's Scout's
        recursion scheme if name is used as an ID. Use SHA1(name) instead.

        :param name:                    Name of the resource to
        :return:                        SHA1(name)
        """
        m = sha1()
        m.update(name.encode('utf-8'))
        return m.hexdigest()
