from ScoutSuite.providers.do.resources.base import DoResources
from ScoutSuite.providers.do.facade.base import DoFacade


class Droplets(DoResources):
    def __init__(self, facade: DoFacade):
        super().__init__(facade)

    async def fetch_all(self):

        droplets = await self.facade.droplet.get_droplets()
        if droplets:
            for droplet in droplets:
                id, droplet = await self._parse_droplet(droplet)
                self[id] = droplet

    async def _parse_droplet(self, raw_droplet):
        droplet_dict = {}

        droplet_dict["id"] = raw_droplet["id"]
        droplet_dict["name"] = raw_droplet["name"]
        droplet_dict["memory"] = raw_droplet["memory"]
        droplet_dict["vcpus"] = raw_droplet["vcpus"]
        droplet_dict["disk"] = raw_droplet["disk"]
        droplet_dict["locked"] = raw_droplet["locked"]
        droplet_dict["status"] = raw_droplet["status"]
        droplet_dict["kernel"] = raw_droplet["kernel"]
        droplet_dict["created_at"] = raw_droplet["created_at"]
        droplet_dict["features"] = raw_droplet["features"]
        droplet_dict["backup_ids"] = str(raw_droplet["backup_ids"])
        droplet_dict["next_backup_window"] = raw_droplet["next_backup_window"]
        droplet_dict["snapshot_ids"] = str(raw_droplet["snapshot_ids"])
        droplet_dict["image"] = raw_droplet["image"]["slug"]
        droplet_dict["image_type"] = raw_droplet["image"]["type"]
        droplet_dict["volume_ids"] = str(raw_droplet["volume_ids"])
        droplet_dict["size"] = raw_droplet["size"]["slug"]
        droplet_dict["size_slug"] = raw_droplet["size_slug"]
        droplet_dict["networks"] = str(raw_droplet["networks"])
        droplet_dict["region"] = raw_droplet["region"]["slug"]
        droplet_dict["tags"] = raw_droplet["tags"]
        droplet_dict["vpc_uuid"] = raw_droplet["vpc_uuid"]
        droplet_dict["firewalls"] = None

        droplet_fwconfig = await self.facade.droplet.get_droplet_fwconfig(
            raw_droplet["id"]
        )
        public_ports = {}

        if droplet_fwconfig:
            if droplet_fwconfig["firewalls"]:
                droplet_dict["firewalls"] = ""
                for firewall in droplet_fwconfig["firewalls"]:
                    droplet_dict["firewalls"] = (
                        droplet_dict["firewalls"] + " , " + firewall["id"]
                        if droplet_dict["firewalls"]
                        else firewall["id"]
                    )

                    for rules in firewall["inbound_rules"]:
                        if (
                            "0.0.0.0/0" in rules["sources"]["addresses"]
                            or "::/0" in rules["sources"]["addresses"]
                        ):
                            public_ports[rules["ports"]] = rules["sources"]["addresses"]

        droplet_dict["all_ports_exposed"] = (
            "True"
            if ("0" in public_ports.keys() or not droplet_fwconfig["firewalls"])
            else "False"
        )
        droplet_dict["port_22_exposed"] = (
            "True"
            if ("22" in public_ports.keys() or droplet_dict["all_ports_exposed"])
            else "False"
        )

        droplet_dict["public_ports_enabled"] = "True" if public_ports else "False"
        droplet_dict["public_port_detail"] = (
            f"Port {','.join(public_ports.keys())} exposed to public internet due to this configuration {str(public_ports)}"
            if public_ports
            else ""
        )
        droplet_dict["features_monitoring"] = (
            "True"
            if ("monitoring" in droplet_dict["features"])
            else "False"
        )
        return droplet_dict["id"], droplet_dict
