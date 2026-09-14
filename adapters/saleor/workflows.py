from adapters.base import (
    AssertionConfig,
    AssertionType,
    EvidenceType,
    WorkflowAction,
    WorkflowStepConfig,
)


WORKFLOWS = {
    "auth.invalid_login": (
        WorkflowStepConfig(
            action=WorkflowAction.NAVIGATE,
            route_name="login",
            evidence=(
                EvidenceType.SCREENSHOT,
            ),
        ),

        WorkflowStepConfig(
            action=WorkflowAction.FILL,
            selector_name="auth.email",
            value_from="invalid_login.email",
        ),

        WorkflowStepConfig(
            action=WorkflowAction.FILL,
            selector_name="auth.password",
            value_from="invalid_login.password",
        ),

        WorkflowStepConfig(
            action=WorkflowAction.CLICK,
            selector_name="auth.submit",
            assertion=AssertionConfig(
                assertion_type=AssertionType.TEXT_CONTAINS,
                expected_text_key="auth.invalid_credentials",
            ),
            evidence=(
                EvidenceType.SCREENSHOT,
                EvidenceType.DOM,
                EvidenceType.NETWORK,
            ),
        ),
    ),
}