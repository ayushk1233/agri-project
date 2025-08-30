# backend/app/services/market_service.py
async def get_mandi_price(crop: str, state: str = None):
    # start with static response for hackathon
    return {"crop": crop, "avg_price": 1800, "currency":"INR", "source":"mock"}
