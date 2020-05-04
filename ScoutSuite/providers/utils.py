import asyncio
from hashlib import sha1

from ScoutSuite.core.console import print_info
from ScoutSuite.providers.aws.utils import is_throttled as aws_is_throttled


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


async def run_concurrently(function, backoff_seconds=15):
    try:
        async with asyncio.get_event_loop().throttler:
            return await run_function_concurrently(function)
    except Exception as e:
        # Determine whether the exception is due to API throttling
        if is_throttled(e):
            print_info('Hitting API rate limiting, will retry in {}s'.format(backoff_seconds))
            await asyncio.sleep(backoff_seconds)
            return await run_concurrently(function, backoff_seconds + 15)
        else:
            raise


def run_function_concurrently(function):
    """
    Schedules the execution of function `function` in the default thread pool (referred as 'executor') that has been
    associated with the global event loop.

    :param function: function to be executed concurrently, in a dedicated thread.
    :return: an asyncio.Future to be awaited.
    """

    return asyncio.get_event_loop().run_in_executor(executor=None, func=function)


async def get_and_set_concurrently(get_and_set_funcs: [], entities: [], **kwargs):
    """
    Given a list of get_and_set_* functions (ex: get_and_set_description, get_and_set_attributes,
    get_and_set_policy, etc.) and a list of entities (ex: stacks, keys, load balancers, vpcs, etc.),
    get_and_set_concurrently will call each of these functions concurrently on each entity.

    :param get_and_set_funcs: list of functions that takes a region and an entity (they must have the following
    signature: region: str, entity: {}) and then fetch and set some kind of attributes to this entity.
    :param entities: list of a same kind of entities
    :param kwargs: used to pass cloud provider specific parameters (ex: region or vpc for AWS, etc.) to the given
    functions.

    :return:
    """

    if len(entities) == 0:
        return

    tasks = {
        asyncio.ensure_future(
            get_and_set_func(entity, **kwargs)
        ) for entity in entities for get_and_set_func in get_and_set_funcs
    }
    await asyncio.wait(tasks)


async def map_concurrently(coroutine, entities, **kwargs):
    """
    Given a list of entities, executes coroutine `coroutine` concurrently on each entity and returns a list of the
    obtained results ([await coroutine(entity_x), await coroutine(entity_a), ..., await coroutine(entity_z)]).

    :param coroutine: coroutine to be executed concurrently. Takes an entity as parameter and returns a new entity.
    If the given coroutine does some exception handling, it should ensure to propagate the handled exceptions so
    `map_concurrently` can handle them as well (in particular ignoring them) to avoid `None` values in the list
    returned.
    :param entities: a list of the same type of entity (ex: cluster ids)

    :return: a list of new entities (ex: clusters)
    """

    if len(entities) == 0:
        return []

    results = []

    tasks = {
        asyncio.ensure_future(
            coroutine(entity, **kwargs)
        ) for entity in entities
    }

    for task in asyncio.as_completed(tasks):
        try:
            result = await task
        except Exception:
            pass
        else:
            results.append(result)

    return results


def is_throttled(e):
    """
    Function that tries to determine if an exception was caused by throttling
    TODO - this implementation is incomplete
    """

    if hasattr(e, 'message') and 'Google Cloud' in e.message:
        return False
    else:
        return aws_is_throttled(e)
