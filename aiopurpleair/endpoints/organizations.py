"""Define an API endpoint for requests related to organizations."""

from __future__ import annotations

from aiopurpleair.endpoints import APIEndpointsBase
from aiopurpleair.models.organizations import GetOrganizationResponse


class OrganizationsEndpoints(APIEndpointsBase):
    """Define the organizations API manager object."""

    async def async_get_organization(self) -> GetOrganizationResponse:
        """Get organization information.

        Returns:
            An API response payload in the form of a Pydantic model.
        """
        response: GetOrganizationResponse = await self._async_request(
            "get",
            "/organization",
            GetOrganizationResponse,
        )
        return response
