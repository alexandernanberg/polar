from typing import Annotated

from fastapi import Depends, Path
from pydantic import (
    UUID4,
)

from polar.authz.service import AccessType, Authz
from polar.exceptions import ResourceNotFound, Unauthorized
from polar.kit.db.postgres import AsyncSession
from polar.models import LicenseKey
from polar.openapi import APITag
from polar.postgres import get_db_session
from polar.routing import APIRouter

from .. import auth
from ..schemas.license_key import LicenseKeyRead, LicenseKeyValidate
from ..service.license_key import license_key as license_key_service

router = APIRouter(prefix="/license-keys", tags=[APITag.documented, APITag.featured])

LK = Annotated[str, Path(description="The license key")]

LicenseKeyNotFound = {
    "description": "License key not found.",
    "model": ResourceNotFound.schema(),
}

###############################################################################
# CRUD
###############################################################################


@router.get(
    "/{id}",
    response_model=LicenseKeyRead,
    responses={404: LicenseKeyNotFound},
)
async def get(
    auth_subject: auth.LicenseKeysRead,
    id: UUID4,
    session: AsyncSession = Depends(get_db_session),
    authz: Authz = Depends(Authz.authz),
) -> LicenseKey:
    """Get a license key."""
    lk = await license_key_service.get_loaded(session, id)
    if not lk:
        raise ResourceNotFound()

    if not await authz.can(auth_subject.subject, AccessType.read, lk):
        raise Unauthorized()

    return lk


###############################################################################
# ACTIVATION & VALIDATION
###############################################################################


@router.post(
    "/validate",
    response_model=LicenseKeyRead,
    responses={404: LicenseKeyNotFound},
)
async def validate(
    license_key: LicenseKeyValidate,
    session: AsyncSession = Depends(get_db_session),
) -> LicenseKey:
    """Validate a license key."""
    return await license_key_service.get_validated(session, license_key)
