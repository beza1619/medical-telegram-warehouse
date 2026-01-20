from api import schemas
from api.database import get_db, test_connection
from typing import List
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import sqlite3
import pandas as pd
from typing import List, Optional
import json
from datetime import datetime

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="API for Ethiopian Medical Telegram Data Analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect('medical_warehouse.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

@app.get("/", response_class=HTMLResponse)
async def root():
    """API Homepage"""
    return """
    <html>
        <head>
            <title>Medical Telegram Analytics API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #2c3e50; }
                .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }
                code { background: #e8f4fc; padding: 2px 6px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>🩺 Medical Telegram Analytics API</h1>
            <p>API for analyzing Ethiopian medical Telegram channels data.</p>
            
            <div class="endpoint">
                <h3>📊 Available Endpoints:</h3>
                <ul>
                    <li><code>GET /api/reports/top-products</code> - Most mentioned products</li>
                    <li><code>GET /api/channels/{channel_name}/activity</code> - Channel activity</li>
                    <li><code>GET /api/search/messages?query=product</code> - Search messages</li>
                    <li><code>GET /api/reports/visual-content</code> - Image usage stats</li>
                    <li><code>GET /api/summary</code> - Overall summary</li>
                </ul>
            </div>
            
            <p>📚 Interactive documentation: <a href="/docs">/docs</a></p>
            <p>📈 Alternative docs: <a href="/redoc">/redoc</a></p>
        </body>
    </html>
    """

@app.get("/api/summary")
async def get_summary():
    """Get overall data summary"""
    conn = get_db_connection()
    
    summary_query = """
    SELECT 
        COUNT(*) as total_messages,
        COUNT(DISTINCT channel_name) as total_channels,
        SUM(has_media) as messages_with_images,
        AVG(views) as avg_views,
        MAX(views) as max_views,
        MIN(message_date) as earliest_date,
        MAX(message_date) as latest_date
    FROM raw_telegram_messages
    """
    
    cursor = conn.cursor()
    cursor.execute(summary_query)
    summary = dict(cursor.fetchone())
    conn.close()
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "data": summary
    }

@app.get("/api/reports/top-products")
async def top_products(limit: int = Query(10, description="Number of top products to return")):
    """
    Get most frequently mentioned products across all channels.
    
    Returns products with their mention count and average price.
    """
    conn = get_db_connection()
    
    # Extract product names and prices
    query = """
    WITH product_extract AS (
        SELECT 
            message_id,
            channel_name,
            message_text,
            views,
            -- Simple product name extraction
            CASE 
                WHEN message_text LIKE '%NIDO%' THEN 'NIDO'
                WHEN message_text LIKE '%VITAMIN%' THEN 'VITAMIN'
                WHEN message_text LIKE '%OLIVE OIL%' THEN 'OLIVE OIL'
                WHEN message_text LIKE '%COCONUT%' THEN 'COCONUT OIL'
                WHEN message_text LIKE '%MELATONIN%' THEN 'MELATONIN'
                WHEN message_text LIKE '%Ashwagandha%' THEN 'ASHWAGANDHA'
                ELSE 'OTHER'
            END as product_category,
            -- Extract price using regex (simplified)
            CAST(
                COALESCE(
                    NULLIF(SUBSTR(message_text, INSTR(message_text, 'Price') + 6, 10), ''),
                    '0'
                ) AS INTEGER
            ) as extracted_price
        FROM raw_telegram_messages
        WHERE message_text IS NOT NULL AND TRIM(message_text) != ''
    )
    SELECT 
        product_category as product_name,
        COUNT(*) as mention_count,
        AVG(views) as avg_views,
        AVG(CASE WHEN extracted_price > 0 THEN extracted_price END) as avg_price,
        MIN(CASE WHEN extracted_price > 0 THEN extracted_price END) as min_price,
        MAX(CASE WHEN extracted_price > 0 THEN extracted_price END) as max_price
    FROM product_extract
    GROUP BY product_category
    HAVING product_category != 'OTHER'
    ORDER BY mention_count DESC
    LIMIT ?
    """
    
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="No products found")
    
    return {
        "status": "success",
        "limit": limit,
        "total_products": len(df),
        "products": df.to_dict(orient='records')
    }

@app.get("/api/channels/{channel_name}/activity")
async def channel_activity(channel_name: str):
    """
    Get posting activity and statistics for a specific channel.
    
    - channel_name: Name of the Telegram channel (e.g., lobelia4cosmetics)
    """
    conn = get_db_connection()
    
    # Validate channel exists
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM raw_telegram_messages WHERE channel_name = ?", (channel_name,))
    channel_exists = cursor.fetchone()['count'] > 0
    
    if not channel_exists:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Channel '{channel_name}' not found in database")
    
    # Get channel statistics
    stats_query = """
    SELECT 
        COUNT(*) as total_posts,
        AVG(views) as avg_views,
        MAX(views) as max_views,
        SUM(has_media) as posts_with_images,
        ROUND(SUM(has_media) * 100.0 / COUNT(*), 2) as image_percentage,
        MIN(message_date) as first_post_date,
        MAX(message_date) as last_post_date
    FROM raw_telegram_messages
    WHERE channel_name = ?
    """
    
    stats_df = pd.read_sql_query(stats_query, conn, params=(channel_name,))
    
    # Get daily activity
    daily_query = """
    SELECT 
        DATE(message_date) as post_date,
        COUNT(*) as post_count,
        AVG(views) as avg_views,
        SUM(has_media) as images_count
    FROM raw_telegram_messages
    WHERE channel_name = ?
    GROUP BY DATE(message_date)
    ORDER BY post_date DESC
    """
    
    daily_df = pd.read_sql_query(daily_query, conn, params=(channel_name,))
    
    conn.close()
    
    return {
        "status": "success",
        "channel": channel_name,
        "statistics": stats_df.to_dict(orient='records')[0],
        "daily_activity": daily_df.to_dict(orient='records'),
        "activity_days": len(daily_df)
    }

@app.get("/api/search/messages")
async def search_messages(
    query: str = Query(..., description="Search keyword"),
    limit: int = Query(20, description="Maximum number of results"),
    channel: Optional[str] = Query(None, description="Filter by channel name")
):
    """
    Search for messages containing specific keywords.
    
    - query: Text to search for
    - limit: Maximum results to return
    - channel: Optional channel filter
    """
    conn = get_db_connection()
    
    # Build query with optional channel filter
    sql_base = """
    SELECT 
        message_id,
        channel_name,
        message_date,
        CASE 
            WHEN LENGTH(message_text) > 100 
            THEN SUBSTR(message_text, 1, 100) || '...' 
            ELSE message_text 
        END as message_preview,
        views,
        forwards,
        has_media,
        image_path
    FROM raw_telegram_messages
    WHERE message_text LIKE ?
    """
    
    params = [f"%{query}%"]
    
    if channel:
        sql_base += " AND channel_name = ?"
        params.append(channel)
    
    sql_base += " ORDER BY views DESC LIMIT ?"
    params.append(limit)
    
    df = pd.read_sql_query(sql_base, conn, params=params)
    conn.close()
    
    return {
        "status": "success",
        "search_query": query,
        "channel_filter": channel,
        "result_count": len(df),
        "limit": limit,
        "results": df.to_dict(orient='records')
    }

@app.get("/api/reports/visual-content")
async def visual_content_stats():
    """
    Get statistics about image usage across channels.
    
    Compares engagement for posts with vs without images.
    """
    conn = get_db_connection()
    
    query = """
    SELECT 
        channel_name,
        COUNT(*) as total_posts,
        SUM(has_media) as posts_with_images,
        COUNT(*) - SUM(has_media) as posts_without_images,
        ROUND(SUM(has_media) * 100.0 / COUNT(*), 2) as image_percentage,
        ROUND(AVG(CASE WHEN has_media = 1 THEN views END), 2) as avg_views_with_images,
        ROUND(AVG(CASE WHEN has_media = 0 THEN views END), 2) as avg_views_without_images,
        ROUND(
            (AVG(CASE WHEN has_media = 1 THEN views END) - 
             AVG(CASE WHEN has_media = 0 THEN views END)) * 100.0 / 
            AVG(CASE WHEN has_media = 0 THEN views END), 2
        ) as engagement_difference_percent
    FROM raw_telegram_messages
    GROUP BY channel_name
    ORDER BY image_percentage DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="No visual content data available")
    
    return {
        "status": "success",
        "analysis": "Image usage and engagement comparison",
        "channels": df.to_dict(orient='records')
    }
@app.get("/health", response_model=schemas.APIResponse)
async def health_check():
    """Health check endpoint"""
    return schemas.APIResponse(
        status="success",
        message="Medical Telegram Analytics API is running",
        data={
            "api_status": "running",
            "endpoints": 6,
            "version": "1.0.0"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
