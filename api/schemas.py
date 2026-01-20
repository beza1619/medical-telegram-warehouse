"""
Pydantic schemas for FastAPI request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ImageCategory(str, Enum):
    PROMOTIONAL = "promotional"
    PRODUCT_DISPLAY = "product_display"
    LIFESTYLE = "lifestyle"
    OTHER = "other"

class ProductSummary(BaseModel):
    """Schema for product summary response"""
    product_name: str = Field(..., description="Name of the product")
    mention_count: int = Field(..., description="Number of times mentioned")
    avg_price: Optional[float] = Field(None, description="Average price in Birr")
    avg_views: float = Field(..., description="Average number of views")
    min_price: Optional[float] = Field(None, description="Minimum price")
    max_price: Optional[float] = Field(None, description="Maximum price")
    
    class Config:
        schema_extra = {
            "example": {
                "product_name": "NIDO",
                "mention_count": 2,
                "avg_price": 7500.0,
                "avg_views": 158.5,
                "min_price": 7500,
                "max_price": 7500
            }
        }

class ChannelActivity(BaseModel):
    """Schema for channel activity response"""
    channel_name: str = Field(..., description="Name of the Telegram channel")
    total_posts: int = Field(..., description="Total number of posts")
    avg_views: float = Field(..., description="Average views per post")
    max_views: int = Field(..., description="Maximum views on a post")
    posts_with_images: int = Field(..., description="Number of posts with images")
    image_percentage: float = Field(..., description="Percentage of posts with images")
    first_post_date: datetime = Field(..., description="Date of first post")
    last_post_date: datetime = Field(..., description="Date of last post")
    
    class Config:
        schema_extra = {
            "example": {
                "channel_name": "lobelia4cosmetics",
                "total_posts": 10,
                "avg_views": 156.2,
                "max_views": 400,
                "posts_with_images": 10,
                "image_percentage": 100.0,
                "first_post_date": "2026-01-17T06:28:02+00:00",
                "last_post_date": "2026-01-17T06:28:25+00:00"
            }
        }

class MessageSearchResult(BaseModel):
    """Schema for message search results"""
    message_id: int = Field(..., description="Unique message identifier")
    channel_name: str = Field(..., description="Channel where message was posted")
    message_date: datetime = Field(..., description="Date and time of message")
    message_preview: str = Field(..., description="First 100 characters of message")
    views: int = Field(..., description="Number of views")
    has_media: bool = Field(..., description="Whether message has media")
    
    class Config:
        schema_extra = {
            "example": {
                "message_id": 22909,
                "channel_name": "lobelia4cosmetics",
                "message_date": "2026-01-17T06:28:02+00:00",
                "message_preview": "**KIRKLAND **ORGANIC EXTRA VIRGIN OLIVE OIL **...",
                "views": 178,
                "has_media": True
            }
        }

class VisualContentStats(BaseModel):
    """Schema for visual content statistics"""
    channel_name: str = Field(..., description="Channel name")
    total_posts: int = Field(..., description="Total number of posts")
    posts_with_images: int = Field(..., description="Posts with images")
    posts_without_images: int = Field(..., description="Posts without images")
    image_percentage: float = Field(..., description="Percentage of posts with images")
    avg_views_with_images: Optional[float] = Field(None, description="Average views for posts with images")
    avg_views_without_images: Optional[float] = Field(None, description="Average views for posts without images")
    engagement_difference_percent: Optional[float] = Field(None, description="Percentage difference in engagement")
    
    class Config:
        schema_extra = {
            "example": {
                "channel_name": "lobelia4cosmetics",
                "total_posts": 10,
                "posts_with_images": 10,
                "posts_without_images": 0,
                "image_percentage": 100.0,
                "avg_views_with_images": 156.2,
                "avg_views_without_images": None,
                "engagement_difference_percent": None
            }
        }

class ImageDetection(BaseModel):
    """Schema for YOLO image detection results"""
    message_id: int = Field(..., description="Message ID")
    channel_name: str = Field(..., description="Channel name")
    detected_class: str = Field(..., description="Object class detected")
    confidence_score: float = Field(..., ge=0, le=1, description="Detection confidence score")
    image_category: ImageCategory = Field(..., description="Category of image")
    
    class Config:
        schema_extra = {
            "example": {
                "message_id": 22909,
                "channel_name": "lobelia4cosmetics",
                "detected_class": "bottle",
                "confidence_score": 0.85,
                "image_category": "product_display"
            }
        }

class APIResponse(BaseModel):
    """Generic API response schema"""
    status: str = Field(..., description="Response status")
    message: Optional[str] = Field(None, description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "data": {"total_messages": 20},
                "timestamp": "2026-01-17T05:17:20.406487"
            }
        }

class ErrorResponse(BaseModel):
    """Error response schema"""
    status: str = Field("error", description="Error status")
    error: str = Field(..., description="Error description")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "error": "Channel not found",
                "details": {"channel_name": "unknown_channel"},
                "timestamp": "2026-01-17T05:17:20.406487"
            }
        }
