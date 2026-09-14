from __future__ import annotations
from enum import Enum
import re
from dataclasses import dataclass, field
from typing import Mapping
from urllib.parse import urlparse


class AdapterConfigError(ValueError):
    """Raised when a target adapter configuration is invalid."""


def _validate_http_url(name: str, value: str | None) -> None:
    if value is None:
        return

    parsed = urlparse(value)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise AdapterConfigError(
            f"{name} must be a valid http/https URL. Got: {value!r}"
        )


@dataclass(frozen=True)
class TargetMetadata:
    key: str
    name: str
    description: str = ""
    adapter_version: str = "1.0"

    def __post_init__(self) -> None:
        if not self.key:
            raise AdapterConfigError("Target metadata key cannot be empty.")

        if not re.fullmatch(r"[a-z0-9_-]+", self.key):
            raise AdapterConfigError(
                "Target metadata key may contain only lowercase letters, "
                "numbers, hyphens, and underscores."
            )

        if not self.name.strip():
            raise AdapterConfigError("Target metadata name cannot be empty.")


@dataclass(frozen=True)
class TargetEnvironment:
    storefront_url: str
    api_url: str | None = None
    dashboard_url: str | None = None

    def __post_init__(self) -> None:
        _validate_http_url("storefront_url", self.storefront_url)
        _validate_http_url("api_url", self.api_url)
        _validate_http_url("dashboard_url", self.dashboard_url)

# enum start
class LocatorType(str, Enum):
    ROLE = "role"
    LABEL = "label"
    TEXT = "text"
    TEST_ID = "test_id"
    PLACEHOLDER = "placeholder"
    CSS = "css"

class GraphQLOperationType(str, Enum):
    QUERY = "query"
    MUTATION = "mutation"

class WorkflowAction(str, Enum):
    NAVIGATE = "navigate"
    CLICK = "click"
    FILL = "fill"
    SELECT = "select"


class AssertionType(str, Enum):
    VISIBLE = "visible"
    HIDDEN = "hidden"
    TEXT_CONTAINS = "text_contains"
    URL_CONTAINS = "url_contains"


class EvidenceType(str, Enum):
    SCREENSHOT = "screenshot"
    DOM = "dom"
    NETWORK = "network"
    CONSOLE = "console"

# enum end

@dataclass(frozen=True)
class AssertionConfig:
    assertion_type: AssertionType
    expected_text_key: str | None = None
    expected_value: str | None = None

    def __post_init__(self) -> None:
        if self.assertion_type == AssertionType.TEXT_CONTAINS:
            if not self.expected_text_key and not self.expected_value:
                raise AdapterConfigError(
                    "TEXT_CONTAINS assertion requires "
                    "expected_text_key or expected_value."
                )

        if self.assertion_type == AssertionType.URL_CONTAINS:
            if not self.expected_value:
                raise AdapterConfigError(
                    "URL_CONTAINS assertion requires expected_value."
                )

@dataclass(frozen=True)
class WorkflowStepConfig:
    """
    Generic description of one workflow step.

    The adapter describes intent.
    Playwright executes it later.
    """

    action: WorkflowAction

    route_name: str | None = None
    selector_name: str | None = None

    value: str | None = None
    value_from: str | None = None

    assertion: AssertionConfig | None = None

    evidence: tuple[EvidenceType, ...] = ()

    def __post_init__(self) -> None:
        if self.action == WorkflowAction.NAVIGATE:
            if not self.route_name:
                raise AdapterConfigError(
                    "NAVIGATE action requires route_name."
                )

        if self.action in {
            WorkflowAction.CLICK,
            WorkflowAction.FILL,
            WorkflowAction.SELECT,
        }:
            if not self.selector_name:
                raise AdapterConfigError(
                    f"{self.action.value.upper()} action "
                    "requires selector_name."
                )

        if self.action in {
            WorkflowAction.FILL,
            WorkflowAction.SELECT,
        }:
            if not self.value and not self.value_from:
                raise AdapterConfigError(
                    f"{self.action.value.upper()} action requires "
                    "value or value_from."
                )

            if self.value and self.value_from:
                raise AdapterConfigError(
                    "Use either value or value_from, not both."
                )

@dataclass(frozen=True)
class LocatorConfig:
    """
    Generic description of how to locate an element.

    The adapter describes the locator.
    Playwright will interpret it later.
    """

    by: LocatorType

    # Used by label, text, test_id, placeholder and css
    value: str | None = None

    # Used by role locators
    role: str | None = None
    name: str | None = None

    exact: bool = True

    def __post_init__(self) -> None:
        if self.by == LocatorType.ROLE:
            if not self.role or not self.name:
                raise AdapterConfigError(
                    "Role locator requires both 'role' and 'name'."
                )

        elif not self.value:
            raise AdapterConfigError(
                f"{self.by.value} locator requires a value."
            )

@dataclass(frozen=True)
class GraphQLOperationConfig:
    """
    Metadata describing a GraphQL operation used by a target.

    This does not contain the GraphQL document yet.
    P06 will own executable API operations.
    """

    operation_name: str
    operation_type: GraphQLOperationType
    purpose: str
    runtime_verified: bool = False

    def __post_init__(self) -> None:
        if not self.operation_name.strip():
            raise AdapterConfigError(
                "GraphQL operation name cannot be empty."
            )

        if not self.purpose.strip():
            raise AdapterConfigError(
                f"GraphQL operation {self.operation_name!r} "
                "must have a purpose."
            )

@dataclass(frozen=True)
class VisualCheckpointConfig:
    """
    Describes a screenshot/evidence checkpoint for a target.

    expected_components are semantic UI component names.
    Later OpenCV/YOLO/OCR can use this metadata.
    """

    route_name: str
    expected_components: tuple[str, ...] = ()
    full_page: bool = True
    viewport_profile: str = "desktop"

    def __post_init__(self) -> None:
        if not self.route_name.strip():
            raise AdapterConfigError(
                "Visual checkpoint route_name cannot be empty."
            )

        if not self.viewport_profile.strip():
            raise AdapterConfigError(
                "Visual checkpoint viewport_profile cannot be empty."
            )

        if any(not component.strip() for component in self.expected_components):
            raise AdapterConfigError(
                "Expected component names cannot be empty."
            )

@dataclass(frozen=True)
class TargetAdapterConfig:
    metadata: TargetMetadata
    environment: TargetEnvironment
    routes: Mapping[str, str] = field(default_factory=dict)
    selectors: Mapping[str, LocatorConfig] = field(default_factory=dict)
    test_data: Mapping[str, Mapping[str, str]] = field(default_factory=dict)
    expected_text: Mapping[str, str] = field(default_factory=dict)
    graphql_operations: Mapping[str, GraphQLOperationConfig] = field(default_factory=dict)
    visual_checkpoints: Mapping[str, VisualCheckpointConfig] = field(default_factory=dict)
    workflows: Mapping[str, tuple[WorkflowStepConfig, ...]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, route in self.routes.items():
            if not name.strip():
                raise AdapterConfigError("Route name cannot be empty.")

            if not route.startswith("/"):
                raise AdapterConfigError(
                    f"Route {name!r} must start with '/'. Got: {route!r}"
                )

        for checkpoint_name, checkpoint in self.visual_checkpoints.items():
            if not checkpoint_name.strip():
                raise AdapterConfigError(
                    "Visual checkpoint name cannot be empty."
                )

            if checkpoint.route_name not in self.routes:
                raise AdapterConfigError(
                    f"Visual checkpoint {checkpoint_name!r} references "
                    f"unknown route {checkpoint.route_name!r}."
                )
            
        for workflow_name, steps in self.workflows.items():
            if not workflow_name.strip():
                raise AdapterConfigError(
                    "Workflow name cannot be empty."
                )

            if not steps:
                raise AdapterConfigError(
                    f"Workflow {workflow_name!r} must contain at least one step."
                )

            for index, step in enumerate(steps, start=1):
                if (
                    step.route_name is not None
                    and step.route_name not in self.routes
                ):
                    raise AdapterConfigError(
                        f"Workflow {workflow_name!r} step {index} "
                        f"references unknown route {step.route_name!r}."
                    )

                if (
                    step.selector_name is not None
                    and step.selector_name not in self.selectors
                ):
                    raise AdapterConfigError(
                        f"Workflow {workflow_name!r} step {index} "
                        f"references unknown selector "
                        f"{step.selector_name!r}."
                    )

                if step.value_from is not None:
                    parts = step.value_from.split(".")

                    if len(parts) != 2:
                        raise AdapterConfigError(
                            f"Workflow {workflow_name!r} step {index} "
                            f"has invalid test-data reference "
                            f"{step.value_from!r}. "
                            "Expected format: 'group.key'."
                        )

                    group_name, value_name = parts

                    if group_name not in self.test_data:
                        raise AdapterConfigError(
                            f"Workflow {workflow_name!r} step {index} "
                            f"references unknown test-data group "
                            f"{group_name!r}."
                        )

                    if value_name not in self.test_data[group_name]:
                        raise AdapterConfigError(
                            f"Workflow {workflow_name!r} step {index} "
                            f"references unknown test-data value "
                            f"{step.value_from!r}."
                        )

                if (
                    step.assertion is not None
                    and step.assertion.expected_text_key is not None
                    and step.assertion.expected_text_key
                    not in self.expected_text
                ):
                    raise AdapterConfigError(
                        f"Workflow {workflow_name!r} step {index} "
                        f"references unknown expected-text key "
                        f"{step.assertion.expected_text_key!r}."
                    )

    def route(self, name: str) -> str:
        try:
            return self.routes[name]
        except KeyError as exc:
            raise AdapterConfigError(
                f"Route {name!r} is not defined for adapter "
                f"{self.metadata.key!r}."
            ) from exc

    def selector(self, name: str) -> LocatorConfig:
        try:
            return self.selectors[name]
        except KeyError as exc:
            raise AdapterConfigError(
                f"Selector {name!r} is not defined for adapter "
                f"{self.metadata.key!r}."
            ) from exc

    def expectation(self, name: str) -> str:
        try:
            return self.expected_text[name]
        except KeyError as exc:
            raise AdapterConfigError(
                f"Expected text {name!r} is not defined for adapter "
                f"{self.metadata.key!r}."
            ) from exc

    def url_for(self, route_name: str) -> str:
        base = self.environment.storefront_url.rstrip("/")
        route = self.route(route_name)

        return f"{base}{route}"

    def graphql_operation(self, name: str,) -> GraphQLOperationConfig:
        try:
            return self.graphql_operations[name]
        except KeyError as exc:
            raise AdapterConfigError(
                f"GraphQL operation {name!r} is not defined "
                f"for adapter {self.metadata.key!r}."
            ) from exc

    def visual_checkpoint(self,name: str,) -> VisualCheckpointConfig:
        try:
            return self.visual_checkpoints[name]
        except KeyError as exc:
            raise AdapterConfigError(
                f"Visual checkpoint {name!r} is not defined "
                f"for adapter {self.metadata.key!r}."
            ) from exc

    def workflow(self,name: str,) -> tuple[WorkflowStepConfig, ...]:
        try:
            return self.workflows[name]
        except KeyError as exc:
            raise AdapterConfigError(
                f"Workflow {name!r} is not defined "
                f"for adapter {self.metadata.key!r}."
            ) from exc

    def test_value(self, reference: str) -> str:
        parts = reference.split(".")

        if len(parts) != 2:
            raise AdapterConfigError(
                f"Invalid test-data reference {reference!r}. "
                "Expected format: 'group.key'."
            )

        group_name, value_name = parts

        try:
            return self.test_data[group_name][value_name]
        except KeyError as exc:
            raise AdapterConfigError(
                f"Test-data reference {reference!r} "
                f"is not defined for adapter "
                f"{self.metadata.key!r}."
            ) from exc