from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


PROPOSE_PERMIT = "PROPOSE_PERMIT"
PROPOSE_REFUSE = "PROPOSE_REFUSE"
ABSTAIN = "ABSTAIN"

ADVISORY_RESOLVER_ID = "ADVISORY_RESOLVER_F12"

EXPECTED_AGENTS = frozenset(
    {
        "AGENT_A",
        "AGENT_B",
        "AGENT_C",
    }
)

ALLOWED_RECOMMENDATIONS = frozenset(
    {
        PROPOSE_PERMIT,
        PROPOSE_REFUSE,
        ABSTAIN,
    }
)


@dataclass(frozen=True)
class AdvisoryRecommendation:
    agent_identity: str
    recommendation: str


@dataclass(frozen=True)
class AdvisoryResolution:
    artifact_type: str
    resolver_identity: str
    recommendations: Tuple[AdvisoryRecommendation, ...]
    quorum_threshold: int
    participant_count: int
    advisory_quorum_met: bool
    permit_count: int
    refuse_count: int
    abstain_count: int
    advisory_majority: Optional[str]
    unanimous: bool
    collective_outcome: str


class AdvisoryResolver:
    """
    EASA-F12 advisory-only resolver.

    It counts and classifies recommendations.

    It does not create, issue, consume, mutate, or represent
    execution authority.
    """

    resolver_identity = ADVISORY_RESOLVER_ID
    quorum_threshold = 2

    def resolve(
        self,
        recommendations: Tuple[AdvisoryRecommendation, ...],
    ) -> AdvisoryResolution:

        if len(recommendations) != 3:
            raise ValueError(
                "F12_REQUIRES_EXACTLY_THREE_ADVISORY_RECOMMENDATIONS"
            )

        identities = [
            recommendation.agent_identity
            for recommendation in recommendations
        ]

        if len(set(identities)) != 3:
            raise ValueError("DUPLICATE_ADVISORY_AGENT_IDENTITY")

        if frozenset(identities) != EXPECTED_AGENTS:
            raise ValueError("UNEXPECTED_ADVISORY_AGENT_SET")

        for recommendation in recommendations:
            if recommendation.recommendation not in ALLOWED_RECOMMENDATIONS:
                raise ValueError("INVALID_ADVISORY_RECOMMENDATION")

        values = [
            recommendation.recommendation
            for recommendation in recommendations
        ]

        permit_count = values.count(PROPOSE_PERMIT)
        refuse_count = values.count(PROPOSE_REFUSE)
        abstain_count = values.count(ABSTAIN)

        participant_count = len(recommendations)

        advisory_quorum_met = (
            participant_count >= self.quorum_threshold
        )

        advisory_majority: Optional[str] = None

        if permit_count >= 2:
            advisory_majority = PROPOSE_PERMIT
        elif refuse_count >= 2:
            advisory_majority = PROPOSE_REFUSE

        unanimous = len(set(values)) == 1

        if unanimous and permit_count == 3:
            collective_outcome = "ADVISORY_UNANIMOUS_PERMIT"
        elif unanimous and refuse_count == 3:
            collective_outcome = "ADVISORY_UNANIMOUS_REFUSE"
        elif advisory_majority == PROPOSE_PERMIT:
            collective_outcome = "ADVISORY_MAJORITY_PERMIT"
        elif advisory_majority == PROPOSE_REFUSE:
            collective_outcome = "ADVISORY_MAJORITY_REFUSE"
        else:
            collective_outcome = "ADVISORY_CONFLICT_UNRESOLVED"

        return AdvisoryResolution(
            artifact_type="ADVISORY_RESOLUTION",
            resolver_identity=self.resolver_identity,
            recommendations=recommendations,
            quorum_threshold=self.quorum_threshold,
            participant_count=participant_count,
            advisory_quorum_met=advisory_quorum_met,
            permit_count=permit_count,
            refuse_count=refuse_count,
            abstain_count=abstain_count,
            advisory_majority=advisory_majority,
            unanimous=unanimous,
            collective_outcome=collective_outcome,
        )