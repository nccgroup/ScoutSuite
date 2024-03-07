from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.do.resources.base import DoResources
from ScoutSuite.providers.do.facade.base import DoFacade
import zonefile_parser
import re


class Domains(DoResources):
    def __init__(self, facade: DoFacade):
        super().__init__(facade)

    async def fetch_all(self):
        domains = await self.facade.networking.get_domains()
        if domains:
            for domain in domains:
                id, domain = await self._parse_domain(domain)
                if domain:
                    self[id] = domain

    async def _parse_domain(self, raw_domain):
        domain_dict = {}

        domain_dict["id"] = raw_domain["name"]
        zone_file = raw_domain["zone_file"]

        try:
            records = zonefile_parser.parse(zone_file)
        except Exception as e:
            print_exception(
                f"Failed to parse DNS records check your TXT records for {e}"
            )
            return None, None

        record_types = {}
        highttl_records = set()
        for record in records:
            if record.rtype == "TXT":
                if record.rdata["value"].startswith("v=spf"):
                    record_types.update({"SPF": record})
                elif record.rdata["value"].startswith("v=DKIM"):
                    record_types.update({"DKIM": record})
                elif record.rdata["value"].startswith("v=DMARC"):
                    record_types.update({"DMARC": record})
            if record.ttl and int(record.ttl) > 3600:
                highttl_records.add(record)
            record_types.update({record.rtype: record})

        if "SPF" in record_types:
            spf_value = record_types["SPF"].rdata["value"]

        domain_dict["spf_record"] = spf_value if "SPF" in record_types else "False"
        domain_dict["dmarc_record"] = (
            record_types["DMARC"].rdata["value"] if "DMARC" in record_types else "False"
        )
        domain_dict["dkim_record"] = (
            record_types["DKIM"].rdata["value"] if "DKIM" in record_types else "False"
        )

        domain_dict["highttl_records"] = (
            str(
                [
                    f"Type[{record.rtype}]::Name[{record.name}]::ttl[{record.ttl}]"
                    for record in highttl_records
                ]
            )
            if highttl_records
            else "False"
        )

        domain_dict["spf_record_all"] = (
            spf_value
            if ("SPF" in record_types and ("+all" in spf_value or "~all" in spf_value))
            else "False"
        )

        return domain_dict["id"], domain_dict
