from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.do.authentication_strategy import DoCredentials
from ScoutSuite.providers.utils import run_concurrently


class DOFacadeUtils:

    @staticmethod
    async def get_all_from_pagination(
        list_client, current_page, per_page, object_name, filters=None
    ):
        final_output = {}
        next_page = True
        while next_page:
            if filters:
                resp = await run_concurrently(
                    lambda: list_client(**filters, per_page=per_page, page=current_page)
                )
            else:
                resp = await run_concurrently(
                    lambda: list_client(per_page=per_page, page=current_page)
                )
            if object_name in final_output.keys():
                final_output[object_name].extend(resp[object_name])
            else:
                final_output[object_name] = resp[object_name]

            pages = resp.get("links").get("pages", {})
            next_page = "next" in pages.keys()
            current_page += 1
        return final_output
