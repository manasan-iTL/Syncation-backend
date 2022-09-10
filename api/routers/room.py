from fastapi import APIRouter

router = APIRouter()


@router.get("/rooms")
async def list_rooms():
  pass

@router.post("/rooms")
async def create_room():
  pass

@router.put("/rooms/{room_id}")
async def update_room():
  pass

@router.delete("/rooms/{room_id}")
async def delete_room():
  pass