import pulumi
from pulumi_azure_native import resources, eventhub


class EventHub:

    def __init__(self, resource_group:resources.ResourceGroup):
        self.resource_group = resource_group

    def get_connection_string(self, ns_name, hub_name, rule_name):
        return pulumi.Output.all(
        self.resource_group.name, 
        ns_name, 
        hub_name, 
        rule_name
    ).apply(lambda args: eventhub.list_event_hub_keys_output(
        resource_group_name=args[0],
        namespace_name=args[1],
        event_hub_name=args[2],
        authorization_rule_name=args[3]
    ).primary_connection_string)
    

    def create_auth_rule(self, topics: list[eventhub.EventHub], namespace: eventhub.Namespace):

        auth_rules =  {}
        for topic in topics:
            producer_auth_rule = eventhub.EventHubAuthorizationRule(
                f"{topic.name}-prod-auth-rule",
                resource_group_name=self.resource_group.name,
                namespace_name=namespace.name,
                event_hub_name=topic.name,
                rights=[eventhub.AccessRights.SEND]
            )

            consumer_auth_rule = eventhub.EventHubAuthorizationRule(
                f"{topic.name}-con-auth-rule",
                resource_group_name=self.resource_group.name,
                namespace_name=namespace.name,
                event_hub_name=topic.name,
                rights=[eventhub.AccessRights.LISTEN]
            )

            # self.get_connection_string(namespace.name, topic.name, producer_auth_rule.name)
            # self.get_connection_string(namespace.name, topic.name, consumer_auth_rule.name)
        

    def create(self):

        namespace = eventhub.Namespace(
            "sc-event-hub",
            resource_group_name=self.resource_group.name,
            location=self.resource_group.location,
            sku = eventhub.SkuArgs(
                name=eventhub.SkuName.STANDARD,
                tier=eventhub.SkuTier.STANDARD,
                capacity=1
            ),
            tags={
                "environment": "development",
            }
        )

        traffic_hub = eventhub.EventHub(
            "sc-traffic-hub",
            resource_group_name=self.resource_group.name,
            namespace_name=namespace.name,
            partition_count=1,
            message_retention_in_days=7

        )

        population_hub= eventhub.EventHub(
            "sc-population-hub",
            resource_group_name=self.resource_group.name,
            namespace_name=namespace.name,
            partition_count=1,
            message_retention_in_days=7
        )

        weather_hub = eventhub.EventHub(
            'sc-weather-hub',
            resource_group_name=self.resource_group.name,
            namespace_name=namespace.name,
            partition_count=1,
            message_retention_in_days=7
        )

        schema_group = eventhub.SchemaRegistry(
            'sc-schema-registry',
            resource_group_name=self.resource_group.name,
            namespace_name=namespace.name,
            schema_type=eventhub.SchemaType.AVRO

        )

        auth_rule = eventhub.get_namespace_authorization_rule_output(
            authorization_rule_name="RootManageSharedAccessKey",
            namespace_name=namespace.name,
            resource_group_name=self.resource_group.name
        )

        # hubs = [traffic_hub, population_hub, weather_hub]

        # self.create_auth_rule(hubs, namespace=namespace)        
