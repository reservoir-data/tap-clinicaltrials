"""Stream type classes for tap-clinicaltrials."""

# ruff: noqa: ERA001

from __future__ import annotations

import typing as t

from requests_cache import CachedSession
from singer_sdk import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class Studies(RESTStream[str]):
    """Studies stream."""

    url_base = "https://clinicaltrials.gov/api"

    name = "studies"
    path = "/v2/studies"

    next_page_token_jsonpath = "$.nextPageToken"  # noqa: S105
    records_jsonpath = "$.studies[*]"

    primary_keys: t.ClassVar[list[str]] = ["nctId"]
    replication_key = "lastUpdateSubmitDate"
    is_sorted = True

    exclude_fields = (
        ("properties", "nctId"),
        ("properties", "lastUpdateSubmitDate"),
    )

    @property
    def requests_session(self) -> requests.Session:
        """Get requests session."""
        return CachedSession(cache_name="clinicaltrials", backend="sqlite", expire_after=3600)

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of parameters to use in the request URL.

        Args:
            context: Optional context dictionary.
            next_page_token: Optional token for fetching the next page of results.
        """
        params: dict[str, t.Any] = {
            "pageSize": 1000,
            "sort": "protocolSection.statusModule.lastUpdateSubmitDate:asc",
            "format": "json",  # Support CSV?
        }

        if next_page_token:
            params["pageToken"] = next_page_token

        if start_date := self.get_starting_replication_key_value(context):
            params["filter.advanced"] = f"AREA[protocolSection.statusModule.lastUpdateSubmitDate]RANGE[{start_date}, MAX]"

        # TODO(edgarrmondragon): Support native field selection
        # https://github.com/edgarrmondragon/tap-clinicaltrials/issues/1
        # fields = [".".join(field[1::2]) for field, selected in self.mask.items() if selected and field and field not in self.exclude_fields]
        # fields.extend(
        #     [
        #         ("protocolSection.identificationModule.nctId"),
        #         ("protocolSection.statusModule.lastUpdateSubmitDate"),
        #     ]
        # )
        # params["fields"] = ",".join(fields)

        if condition := self.config.get("condition"):
            params["query.cond"] = condition

        if sponsor := self.config.get("sponsor"):
            params["query.spons"] = sponsor

        return params

    def post_process(
        self,
        row: dict[str, t.Any],
        context: Context | None = None,  # noqa: ARG002
    ) -> dict[str, t.Any] | None:
        """Return a modified data row."""
        row["nctId"] = row["protocolSection"]["identificationModule"]["nctId"]
        row["lastUpdateSubmitDate"] = row["protocolSection"]["statusModule"]["lastUpdateSubmitDate"]
        return row
