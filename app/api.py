from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional, Tuple

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from distributed_websocket import WebSocketManager
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body, Depends, Path
from fastapi.websockets import WebSocket
from pokerengine.card import Cards
from pokerengine.evaluation import get_evaluation_result
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api_protect import api_protect
from core.depends import get_redis, get_scheduler, get_session, get_websocket_manager
from requests import GetUserRequest, RememberUserRequest, TakeBonusRequest
from schemas import ApplicationResponse
from schemas.orm import User
from store import create_balance, create_user, get_user_by_id, take_bonus
from ws import websocket_handler

router = APIRouter()


@router.websocket(path="/ws{user_id}")
async def main_websocket_handler(
    websocket: WebSocket,
    manager: WebSocketManager = Depends(get_websocket_manager),
    redis: Redis = Depends(get_redis),
    scheduler: AsyncIOScheduler = Depends(get_scheduler),
    user_id: Optional[str] = Path(...),
) -> None:
    connection = await manager.new_connection(websocket=websocket, conn_id=user_id)

    try:
        await websocket_handler(
            connection=connection, manager=manager, redis=redis, scheduler=scheduler
        )
    except Exception:
        manager.remove_connection(connection)


@router.post(
    path="/getEvaluationResult",
    response_model=ApplicationResponse[List[Tuple[str, int]]],
    status_code=status.HTTP_200_OK,
)
async def get_evaluation_result_handler(
    board: List[str] = Body(...),
    hands: List[str] = Body(...),
    players: List[int] = Body(...),
) -> Dict[str, Any]:
    return {
        "ok": True,
        "result": [
            (str(result), index)
            for result, index in get_evaluation_result(
                cards=Cards(board=board, hands=hands), players=players
            )
        ],
    }


@router.post(
    path="/getUser",
    response_model=ApplicationResponse[User],
    status_code=status.HTTP_200_OK,
)
async def get_user_handler(
    session: AsyncSession = Depends(get_session),
    request: GetUserRequest = Body(...),
) -> Dict[str, Any]:
    user = await get_user_by_id(session=session, user_id=request.user_id)
    if not user:
        raise HTTPException(
            detail="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return {
        "ok": True,
        "result": user,
    }


@router.post(
    path="/rememberUser",
    dependencies=[Depends(api_protect)],
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def remember_user_handler(
    session: AsyncSession = Depends(get_session),
    request: RememberUserRequest = Body(...),
) -> Dict[str, Any]:
    await create_user(session=session, user_id=request.user_id)
    await create_balance(session=session, user_id=request.user_id)

    return {
        "ok": True,
        "result": True,
    }


@router.post(
    path="/takeBonus",
    dependencies=[Depends(api_protect)],
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def take_bonus_handler(
    session: AsyncSession = Depends(get_session),
    request: TakeBonusRequest = Body(...),
) -> Dict[str, Any]:
    user = await get_user_by_id(session=session, user_id=request.user_id)
    if not user:
        raise HTTPException(
            detail="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if (
        user.balance.last_time_claimed_bonus
        and user.balance.last_time_claimed_bonus
        + datetime.timedelta(hours=user.balance.bonus_increment_time_hours)
        > datetime.datetime.now()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    await take_bonus(
        session=session,
        balance_id=user.balance.id,
        bonus_increment_time_hours=user.balance.bonus_increment_time_hours,
    )
    return {
        "ok": True,
        "result": True,
    }
