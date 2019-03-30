import asyncio

from hashlib import sha1


def get_non_provider_id(name):
    """
    Not all resources have an ID and some services allow the use of "." in names, which breaks Scout's
    recursion scheme if name is used as an ID. Use SHA1(name) instead.

    :param name:                    Name of the resource to
    :return:                        SHA1(name)
    """
    name_hash = sha1()
    name_hash.update(name.encode('utf-8'))
    return name_hash.hexdigest()


def run_concurrently(func):
    """
    Schedules the execution of function `func` in the default thread pool (referred as 'executor') that has been
    associated with the global event loop.

    :param func: function to be executed concurrently, in a dedicated thread.
    :return: an asyncio.Future to be awaited.
    """

    return asyncio.get_event_loop().run_in_executor(executor=None, func=func)


async def map_concurrently(coro, entities, **kwargs):
    """
    Given a list of entities, executes coroutine `coro` concurrently on each entity and returns a list of the obtained
    results ([await coro(entity_x), await coro(entity_a), ..., await coro(entity_z)]).

    :param coro: coroutine to be executed concurrently. Takes an entity as parameter and returns a new entity.
    :param entities: a list of the same type of entity (ex: cluster ids)

    :return: a list of new entities (ex: clusters)
    """
    results = []

    tasks = {
        asyncio.ensure_future(
            coro(entity, **kwargs)
        ) for entity in entities
    }
    for task in asyncio.as_completed(tasks):
        result = await task
        results.append(result)

    return results
