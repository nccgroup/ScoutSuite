from hashlib import sha1
import asyncio


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
        return asyncio.get_event_loop().run_in_executor(executor=None, func=func)

async def run_tasks_concurrently(tasks):
    entities = []
    # tasks = {
    #     asyncio.ensure_future(run_concurrently(lambda: self._get_table(region, table_name))) for table_name in tables_names
    # }

    parallelized_tasks = {
        asyncio.ensure_future(run_concurrently(task)) for task in tasks
    }

    for task in asyncio.as_completed(parallelized_tasks):
        entity = await task
        entities.append(entity)

    return entities
