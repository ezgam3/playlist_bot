from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.storage.base_crud import CRUDBase
from app.storage.models import Playlist, Review, User, Event
from app.storage.schemas import (
    PlaylistCreate,
    PlaylistUpdate,
    ReviewCreate,
    ReviewUpdate,
    UserCreate,
    UserUpdate,
    EventCreate,
    EventUpdate,
)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """User CRUD."""

    async def get_by_telegram_id(self, db: AsyncSession, telegram_id: int) -> User | None:
        """Get user by telegram id."""
        query = select(self.model).where(self.model.telegram_id == telegram_id)
        result = await db.scalars(query)
        return result.first()

    async def get_state(self, db: AsyncSession, telegram_id: int) -> str | None:
        """Get user state."""
        query = select(self.model).where(self.model.telegram_id == telegram_id)
        result = await db.scalars(query)
        return result.first().state

    async def change_state(self, db: AsyncSession, telegram_id: int, state: int) -> None:
        """Change user state."""
        query = select(self.model).where(self.model.telegram_id == telegram_id)
        result = await db.scalars(query)
        user = result.first()
        user.state = state
        db.add(user)
        await db.commit()
        await db.refresh(user)


class CRUDPlaylist(CRUDBase[Playlist, PlaylistCreate, PlaylistUpdate]):
    """Playlist CRUD."""

    async def get_by_telegram_id(self, db: AsyncSession, telegram_id: int) -> Playlist:
        """Get playlist by telegram id."""
        query = select(self.model).where(self.model.telegram_id == telegram_id)
        result = await db.scalars(query)
        return result.first()


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    """Review CRUD."""

    async def get_no_review_by_round(
        self, db: AsyncSession, event_id: int, round: int
    ) -> list[Review]:
        """Get people no review by round.

        Args:
            db (AsyncSession): Database session.
            event_id (int): Event row id.
            round (int): Event round.

        Returns:
            list[Review]: List of reviews.
        """
        query = (
            select(self.model)
            .where(self.model.event_id == event_id)
            .where(self.model.round == round)
            .where(self.model.rating == None)  # noqa: E711
        )
        result = await db.scalars(query)
        return result.all()


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    """Event CRUD."""

    async def add_event_member(self, db: AsyncSession, event_id: int, user_id: int) -> None:
        """Add user to event."""
        event = await self.get(db, id=event_id)
        event.members.append(user_id)
        db.add(event)
        await db.commit()
        await db.refresh(event)

    async def change_state(self, db: AsyncSession, event_id: int, state: int) -> None:
        """Change event state."""
        event = await self.get(db, id=event_id)
        event.state = state
        db.add(event)
        await db.commit()
        await db.refresh(event)

    async def change_round(self, db: AsyncSession, event_id: int, round: int) -> None:
        """Change event round."""
        event = await self.get(db, id=event_id)
        event.round = round
        db.add(event)
        await db.commit()
        await db.refresh(event)

    async def change_playlist_queue(
        self, db: AsyncSession, event_id: int, playlist_queue: dict[int, list[int]]
    ) -> None:
        """Change event playlist queue."""
        event = await self.get(db, id=event_id)
        event.playlist_queue = playlist_queue
        db.add(event)
        await db.commit()
        await db.refresh(event)


user = CRUDUser(User)
playlist = CRUDPlaylist(Playlist)
review = CRUDReview(Review)
event = CRUDEvent(Event)
