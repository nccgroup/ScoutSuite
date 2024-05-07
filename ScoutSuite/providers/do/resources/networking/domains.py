from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.do.resources.base import DoResources
from ScoutSuite.providers.do.facade.base import DoFacade
import re


class Domains(DoResources):
    def __init__(self, facade: DoFacade):
        super().__init__(facade)

    async def fetch_all(self):
        domains = await self.facade.networking.get_domains()
        if domains:
            for domain in domains:
                name, domain = await self._parse_domain(domain)
                if domain:
                    self[name] = domain
    async def _parse_domain(self, raw_domain):
        domain_dict = {}
        domain_dict["name"] = raw_domain["name"]
        zone_file = raw_domain["zone_file"]

        spf_pattern = re.compile(r'.*TXT.*v=spf.*', re.IGNORECASE)
        domain_dict["spf_record"] = "True" if bool(re.search(spf_pattern, zone_file)) else "False"
        dmarc_pattern = re.compile(r'.*TXT.*v=DMARC.*', re.IGNORECASE)
        domain_dict["dmarc_record"] = "True" if bool(re.search(dmarc_pattern, zone_file)) else "False"
        dkim_pattern = re.compile(r'.*TXT.*v=DKIM.*', re.IGNORECASE)
        domain_dict["dkim_record"] = "True" if bool(re.search(dkim_pattern, zone_file)) else "False"

        ttl_regex = r"\.\s*(\d+)\s*IN"
        ttl_matches = re.findall(ttl_regex, zone_file)
        numbers = [int(match) for match in ttl_matches]

        domain_dict["highttl_records"] = (
            "True"
            if max(numbers) > 3600
            else "False"
        )

        pattern1 = re.compile(r'.*TXT.*v=spf.*~all', re.IGNORECASE)
        pattern2 = re.compile(r'.*TXT.*v=spf.*\+all', re.IGNORECASE)
        domain_dict["spf_record_all"] = (
            "True"
            if bool(re.search(pattern1, zone_file))  or bool(re.search(pattern2, zone_file)) 
            else "False"
        )

        return domain_dict["name"], domain_dict