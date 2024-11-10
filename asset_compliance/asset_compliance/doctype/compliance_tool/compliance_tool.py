# Copyright (c) 2024, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ComplianceTool(Document):

    def on_submit(self):
        if self.items:
            grouped_rows = self.group_items_by_asset(self.items)
            for asset_name, (rows, maintenance_team) in grouped_rows.items():
                create_asset_maintenance(asset_name, rows, maintenance_team, self)

    def group_items_by_asset(self, items):
        grouped_rows = {}

        for row in items:
            asset_name = row.asset_name
            maintenance_team = row.maintenance_team

            if asset_name not in grouped_rows:
                grouped_rows[asset_name] = ([], maintenance_team)
            else:
                _, existing_team = grouped_rows[asset_name]
                if existing_team != maintenance_team:
                    frappe.throw(
                        _(
                            "Asset {0} cannot have different maintenance teams in different rows."
                        ).format(asset_name)
                    )

            grouped_rows[asset_name][0].append(row)

        return grouped_rows


def create_asset_maintenance(asset_name, rows, maintenance_team, compliance_tool):
    asset_maintenance = frappe.new_doc("Asset Maintenance")
    asset_maintenance.asset_name = asset_name
    asset_maintenance.company = compliance_tool.company
    asset_maintenance.custom_corporation = compliance_tool.corporation
    asset_maintenance.custom_unit = compliance_tool.unit
    asset_maintenance.custom_building = compliance_tool.building
    asset_maintenance.maintenance_team = maintenance_team
    asset_maintenance.custom_tool_link = compliance_tool.name

    for row in rows:
        child_data = row.as_dict()
        child_data.pop("maintenance_team", None)
        child_data.pop("asset_name", None)
        child_data.pop("item_name", None)
        child_data.pop("asset_category", None)
        child_data.pop("item_code", None)
        asset_maintenance.append("asset_maintenance_tasks", child_data)

    asset_maintenance.save(ignore_permissions=True)
