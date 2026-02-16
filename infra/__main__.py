"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources

from src.event_hub import EventHub

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("eventhub-rg")

event_hub = EventHub(resource_group=resource_group).create()



# Create an Azure Storage Account
# account = storage.StorageAccount(
#     "sa",
#     resource_group_name=resource_group.name,
#     sku={
#         "name": storage.SkuName.STANDARD_LRS,
#     },
#     kind=storage.Kind.STORAGE_V2,
# )

# Export the storage account name
# pulumi.export("storage_account_name", account.name)
