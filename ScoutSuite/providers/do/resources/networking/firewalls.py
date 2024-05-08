from ScoutSuite.providers.do.resources.base import DoResources
from ScoutSuite.providers.do.facade.base import DoFacade


class Firewalls(DoResources):
    def __init__(self, facade: DoFacade):
        super().__init__(facade)

    async def fetch_all(self):

        firewalls = await self.facade.networking.get_firewalls()
        if firewalls:
            for firewall in firewalls:
                id, firewall = await self._parse_firewall(firewall)
                self[id] = firewall

    async def _parse_firewall(self, raw_firewall):
        firewall_dict = {}

        firewall_dict["id"] = raw_firewall["id"]
        firewall_dict["name"] = raw_firewall["name"]
        firewall_dict["status"] = raw_firewall["status"]
        firewall_dict["inbound_rules"] = raw_firewall["inbound_rules"]
        firewall_dict["outbound_rules"] = raw_firewall["outbound_rules"]
        firewall_dict["created_at"] = raw_firewall["created_at"]
        firewall_dict["droplet_ids"] = str(raw_firewall["droplet_ids"])
        firewall_dict["tags"] = str(raw_firewall["tags"])
        firewall_dict["pending_changes"] = str(raw_firewall["pending_changes"])
        public_ports = {}
        for rules in raw_firewall["inbound_rules"]:
            if (
                "0.0.0.0/0" in rules["sources"]["addresses"]
                or "::/0" in rules["sources"]["addresses"]
            ):
                public_ports[rules["ports"]] = rules["sources"]["addresses"]

        firewall_dict["all_ports_exposed"] = (
            "True" if ("0" in public_ports.keys()) else "False"
        )
        firewall_dict["public_ports_enabled"] = "True" if public_ports else "False"
        firewall_dict["public_port_detail"] = (
            f"Port {','.join(public_ports.keys())} exposed to public internet due to this configuration {str(public_ports)}"
            if public_ports
            else ""
        )

        return firewall_dict["id"], firewall_dict
