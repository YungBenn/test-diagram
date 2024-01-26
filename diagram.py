from diagrams import Diagram, Cluster
from diagrams.aws.compute import AppRunner
from diagrams.onprem.database import Mongodb, Postgresql
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Kong
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.elastic.elasticsearch import Elasticsearch

with Diagram("Tech Shop Design System", show=False):
    kong = Kong("API Gateway")

    with Cluster("Auth Service"):
        auth_service = AppRunner("Auth Service")
        auth_service - [
            Postgresql("Auth DB"),
            Redis("Token")
        ]

    with Cluster("Product Service"):
        product_service = AppRunner("Product Service")
        product_db = Mongodb("Product DB")
        product_service - product_db
    
    with Cluster("Search Service"):
        search_service = AppRunner("Search Service")
        search_db = Elasticsearch("Search ES")
        search_service - search_db

    product_db >> Kafka("Message") >> search_db

    kong >> [
        auth_service,
        product_service,
        search_service
    ]
