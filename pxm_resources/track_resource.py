import fastapi

from pxm_commons.errors import PxmServiceError
from pxm_models.models import Track
from pxm_services import track_service

router = fastapi.APIRouter(prefix='/track', tags=['Track'])


@router.get('/', response_model=list[Track])
async def get_top_tracks() -> list[Track]:
    try:
        top_tracks: list[Track] = list()

        for track in track_service.get_top_tracks():
            top_tracks.append(
                Track(
                    id=track.pid,
                    name=track.title,
                )
            )
        return top_tracks
    except PxmServiceError:
        # TODO: Log the error
        return []
