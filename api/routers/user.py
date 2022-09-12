from fastapi import APIRouter

router = APIRouter()


@router.get("/{room_id}/users")
async def list_users():
  pass

@router.post("/{room_id}/users")
async def create_user():
  pass

@router.put("/{room_id}/users/{user_id}")
async def update_users():
  pass

@router.delete("/{room_id}/users/{user_id}")
async def delete_user():
  pass