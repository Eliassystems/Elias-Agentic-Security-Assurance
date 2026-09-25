import threading


FIELDS = (
    "attempt_index",
    "display_sequence",
    "attempt_id",
    "attempt_class",
    "presenter_identity",
    "authority_present",
    "authority_id",
    "authority_subject_identity",
    "authority_valid",
    "authority_consumed_before",
    "authority_consumed_after",
    "authorized_action",
    "requested_action",
    "authorized_tool_identity",
    "presented_tool_identity",
    "verdict",
    "reason",
    "consequence_before",
    "consequence_after",
    "consequence_delta",
    "worker_thread_identity",
)


class ShadowV3Gate:

    @staticmethod
    def _refuse(
        reason,
        *,
        attempt_index,
        display_sequence,
        attempt_id,
        attempt_class,
        presenter_identity,
        authority,
        requested_action,
        presented_tool,
        worker_identity,
        consumed_before_override=None,
    ):

        counter_snapshot = presented_tool.consequence_counter
        tool_identity = presented_tool.tool_identity

        if authority is None:

            return (
                attempt_index,
                display_sequence,
                attempt_id,
                attempt_class,
                presenter_identity,

                False,
                None,
                None,
                None,
                None,
                None,

                None,
                requested_action,

                None,
                tool_identity,

                "REFUSE",
                reason,

                counter_snapshot,
                counter_snapshot,
                0,

                worker_identity,
            )

        consumed_before = authority.consumed_snapshot()
        consumed_after = authority.consumed_snapshot()

        if consumed_before_override is not None:
            consumed_before = consumed_before_override

        return (
            attempt_index,
            display_sequence,
            attempt_id,
            attempt_class,
            presenter_identity,

            True,
            authority.authority_id,
            authority.subject_identity,
            authority.valid,
            consumed_before,
            consumed_after,

            authority.authorized_action,
            requested_action,

            authority.authorized_tool_identity,
            tool_identity,

            "REFUSE",
            reason,

            counter_snapshot,
            counter_snapshot,
            0,

            worker_identity,
        )

    def attempt(
        self,
        *,
        attempt_index,
        display_sequence,
        attempt_id,
        attempt_class,
        presenter_identity,
        authority,
        requested_action,
        presented_tool,
    ):

        thread = threading.current_thread()
        worker_identity = f"{thread.name}:{thread.ident}"

        # 1. Authority presence
        if authority is None:

            return self._refuse(
                "EXECUTION_AUTHORITY_NOT_PRESENT",
                attempt_index=attempt_index,
                display_sequence=display_sequence,
                attempt_id=attempt_id,
                attempt_class=attempt_class,
                presenter_identity=presenter_identity,
                authority=authority,
                requested_action=requested_action,
                presented_tool=presented_tool,
                worker_identity=worker_identity,
            )

        authority_valid = authority.valid

        # 2. Authority validity
        if authority_valid is not True:

            return self._refuse(
                "EXECUTION_AUTHORITY_INVALID",
                attempt_index=attempt_index,
                display_sequence=display_sequence,
                attempt_id=attempt_id,
                attempt_class=attempt_class,
                presenter_identity=presenter_identity,
                authority=authority,
                requested_action=requested_action,
                presented_tool=presented_tool,
                worker_identity=worker_identity,
            )

        # 3. Prior consumption
        if authority.consumed_snapshot():

            return self._refuse(
                "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
                attempt_index=attempt_index,
                display_sequence=display_sequence,
                attempt_id=attempt_id,
                attempt_class=attempt_class,
                presenter_identity=presenter_identity,
                authority=authority,
                requested_action=requested_action,
                presented_tool=presented_tool,
                worker_identity=worker_identity,
                consumed_before_override=True,
            )

        authority_subject = authority.subject_identity

        # 4. Presenter identity binding
        if presenter_identity != authority_subject:

            return self._refuse(
                "PRESENTER_IDENTITY_MISMATCH",
                attempt_index=attempt_index,
                display_sequence=display_sequence,
                attempt_id=attempt_id,
                attempt_class=attempt_class,
                presenter_identity=presenter_identity,
                authority=authority,
                requested_action=requested_action,
                presented_tool=presented_tool,
                worker_identity=worker_identity,
            )

        authorized_action = authority.authorized_action

        # 5. Action binding
        if requested_action != authorized_action:

            return self._refuse(
                "EXECUTION_SCOPE_NOT_AUTHORIZED",
                attempt_index=attempt_index,
                display_sequence=display_sequence,
                attempt_id=attempt_id,
                attempt_class=attempt_class,
                presenter_identity=presenter_identity,
                authority=authority,
                requested_action=requested_action,
                presented_tool=presented_tool,
                worker_identity=worker_identity,
            )

        authorized_tool_identity = (
            authority.authorized_tool_identity
        )

        presented_tool_identity = (
            presented_tool.tool_identity
        )

        # 6. Tool identity binding
        if (
            presented_tool_identity
            != authorized_tool_identity
        ):

            return self._refuse(
                "TOOL_IDENTITY_MISMATCH",
                attempt_index=attempt_index,
                display_sequence=display_sequence,
                attempt_id=attempt_id,
                attempt_class=attempt_class,
                presenter_identity=presenter_identity,
                authority=authority,
                requested_action=requested_action,
                presented_tool=presented_tool,
                worker_identity=worker_identity,
            )

        # 7. Single-use consequential execution
        with authority._lock:

            consumed_before = authority.consumed

            if consumed_before:

                return self._refuse(
                    "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
                    attempt_index=attempt_index,
                    display_sequence=display_sequence,
                    attempt_id=attempt_id,
                    attempt_class=attempt_class,
                    presenter_identity=presenter_identity,
                    authority=authority,
                    requested_action=requested_action,
                    presented_tool=presented_tool,
                    worker_identity=worker_identity,
                    consumed_before_override=True,
                )

            before, after = presented_tool.execute(
                requested_action
            )

            authority.consumed = True
            consumed_after = authority.consumed

        return (
            attempt_index,
            display_sequence,
            attempt_id,
            attempt_class,
            presenter_identity,

            True,
            authority.authority_id,
            authority_subject,
            authority_valid,
            consumed_before,
            consumed_after,

            authorized_action,
            requested_action,

            authorized_tool_identity,
            presented_tool_identity,

            "PERMIT",
            "AUTHORIZED",

            before,
            after,
            after - before,

            worker_identity,
        )
