# file: models.py

from sqlmodel import SQLModel, Field
from datetime import datetime

# Database Model: Represents the 'campaigns' table in the database
class Campaign(SQLModel, table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str
    updated_date: datetime = Field(default_factory=datetime.now)
    created_date: datetime = Field(default_factory=datetime.now)

# Pydantic Model for Data Validation (Input)
# Used when creating a new campaign via a POST request
class CampaignCreate(SQLModel):
    name: str
    # Set default values for dates upon creation
    updated_date: datetime = Field(default_factory=datetime.now)
    created_date: datetime = Field(default_factory=datetime.now)

# Pydantic Model for Data Validation (Output)
# Used for the response of listing all campaigns
class CampaignResponse(SQLModel):
    campaigns: list[Campaign]