import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import  Any
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# --- Credits System Models ---


class UserProfile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, unique=True, index=True
    )
    credits_balance: int = Field(default=0, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    user: Optional["User"] = Relationship()


class CreditTransaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_profile_id: uuid.UUID = Field(
        foreign_key="userprofile.id", nullable=False, index=True
    )
    amount: int = Field(nullable=False)
    transaction_type: str = Field(max_length=32, nullable=False)  # 'deduct' or 'add'
    description: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    user_profile: Optional["UserProfile"] = Relationship()


class AICredits(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    allotted: int = Field(default=0, nullable=False)
    used: int = Field(default=0, nullable=False)
    reset_in_days: int = Field(default=30, nullable=False, alias="resetindays")
    credits_available: int = Field(default=0, nullable=False, description="Current available credits (allotted - used + any top-ups)")
    credits_topped_up: int = Field(default=0, nullable=False, description="Amount of credits last topped up")
    time_topped_up: datetime | None = Field(default=None, description="Timestamp of last top-up")
    subscription_id: uuid.UUID = Field(
        foreign_key="userprofilesubscription.id", nullable=False, index=True, alias="subscriptionid"
    )


class LeadCredits(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    allotted: int = Field(default=0, nullable=False)
    used: int = Field(default=0, nullable=False)
    reset_in_days: int = Field(default=30, nullable=False, alias="resetindays")
    credits_available: int = Field(default=0, nullable=False, description="Current available credits (allotted - used + any top-ups)")
    credits_topped_up: int = Field(default=0, nullable=False, description="Amount of credits last topped up")
    time_topped_up: datetime | None = Field(default=None, description="Timestamp of last top-up")
    subscription_id: uuid.UUID = Field(
        foreign_key="userprofilesubscription.id", nullable=False, index=True, alias="subscriptionid"
    )


class SkipTraceCredits(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    allotted: int = Field(default=0, nullable=False)
    used: int = Field(default=0, nullable=False)
    reset_in_days: int = Field(default=30, nullable=False, alias="resetindays")
    credits_available: int = Field(default=0, nullable=False, description="Current available credits (allotted - used + any top-ups)")
    credits_topped_up: int = Field(default=0, nullable=False, description="Amount of credits last topped up")
    time_topped_up: datetime | None = Field(default=None, description="Timestamp of last top-up")
    subscription_id: uuid.UUID = Field(
        foreign_key="userprofilesubscription.id", nullable=False, index=True, alias="subscriptionid"
    )

# --- Moved to vapi/schemas.py ---
# class AssistantOverrides(BaseModel): ...
# class Assistant(BaseModel): ...
# class CreateCallRequest(BaseModel): ...