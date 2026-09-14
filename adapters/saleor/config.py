import os

from adapters.base import (
    TargetAdapterConfig,
    TargetEnvironment,
    TargetMetadata,
)

from .routes import ROUTES
from .selectors import SELECTORS
from .expectations import EXPECTED_TEXT
from .test_data import TEST_DATA
from .graphql import GRAPHQL_OPERATIONS
from .visual import VISUAL_CHECKPOINTS
from .workflows import WORKFLOWS

def load_saleor_config() -> TargetAdapterConfig:
    return TargetAdapterConfig(
        metadata=TargetMetadata(
            key="saleor",
            name="Saleor Storefront",
            description="Saleor reference target for the AI web testing platform.",
        ),
        environment=TargetEnvironment(
            storefront_url=os.getenv(
                "SALEOR_STOREFRONT_URL",
                "http://localhost:3000",
            ),
            api_url=os.getenv(
                "SALEOR_API_URL",
                "http://localhost:8000/graphql/",
            ),
            dashboard_url=os.getenv(
                "SALEOR_DASHBOARD_URL",
                "http://localhost:9000",
            ),
        ),
        routes=ROUTES,
        selectors=SELECTORS,
        test_data=TEST_DATA,
        expected_text=EXPECTED_TEXT,
        graphql_operations=GRAPHQL_OPERATIONS,
        visual_checkpoints=VISUAL_CHECKPOINTS,
        workflows=WORKFLOWS,
    )


SALEOR_CONFIG = load_saleor_config()