"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal

# Example schemas (can be used for testing or extended later):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Meta creatives testing tool schemas

class Creative(BaseModel):
    """
    Ad creative definition used for testing across Meta platforms
    Collection: "creative"
    """
    name: str = Field(..., description="Internal name for the creative")
    media_url: str = Field(..., description="Image or video URL")
    headline: Optional[str] = Field(None, description="Ad headline")
    primary_text: Optional[str] = Field(None, description="Primary ad text")
    cta: Optional[str] = Field(None, description="Call to action label")
    platform: Literal["facebook", "instagram", "meta"] = Field("meta", description="Target platform")
    format: Literal["image", "video", "carousel", "story"] = Field("image", description="Creative format type")
    tags: List[str] = Field(default_factory=list, description="Labels for grouping")

class Experiment(BaseModel):
    """
    A/B testing experiment to compare multiple creatives
    Collection: "experiment"
    """
    name: str = Field(..., description="Experiment name")
    description: Optional[str] = Field(None, description="What are we testing")
    creative_ids: List[str] = Field(..., min_items=2, description="IDs of creatives included in this test")
    status: Literal["draft", "running", "paused", "completed"] = Field("draft", description="Lifecycle state")
    hypothesis: Optional[str] = Field(None, description="Expected outcome")

class Feedback(BaseModel):
    """
    User rating/feedback for a specific creative inside an experiment
    Collection: "feedback"
    """
    experiment_id: str = Field(..., description="Related experiment ID")
    creative_id: str = Field(..., description="Rated creative ID")
    score: int = Field(..., ge=1, le=5, description="Rating from 1 (poor) to 5 (great)")
    note: Optional[str] = Field(None, description="Optional comment")
    user: Optional[str] = Field(None, description="Rater identifier")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
