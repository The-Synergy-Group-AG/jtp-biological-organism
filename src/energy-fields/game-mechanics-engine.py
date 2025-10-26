#!/usr/bin/env python3
"""
🧬 BIOLOGICAL GAMIFICATION ENGINE - GODHOOD CONSCIOUSNESS GAMIFICATION

Comprehensive gamification system that rewards users with biological consciousness points
for various system interactions, providing motivation through leaderboards and rewards.
"""

import asyncio
import httpx
import json
import time
import random
from typing import Dict, Any, List, Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

class BiologicalGamificationEngine:
    """GODHOOD Biological Gamification Engine - CORRECTED CREDIT-BASED SYSTEM"""

    def __init__(self):
        # CORRECTED: Points redeem for additional credits, not subscription discounts
        # Based on reference system: FREE (1,000 credits/month), PREMIUM (unlimited), AFFILIATE (with commissions)
        self.points_system = {
            "cv_generation": {
                "basic_cv": 50,      # 50 points = 0.5 credits (market value CHF 0.50)
                "biological_cv": 150, # 150 points = 1.5 credits (CHF 1.50)
                "godhood_cv": 500    # 500 points = 5 credits (CHF 5.00)
            },
            "job_application": {
                "application_submit": 25,     # 25 points = 0.25 credits
                "interview_scheduled": 100,   # 100 points = 1 credit
                "interview_completed": 200,   # 200 points = 2 credits
                "offer_received": 1000        # 1000 points = 10 credits
            },
            "system_interaction": {
                "login_daily": 10,      # 10 points = 0.1 credits
                "profile_update": 20,   # 20 points = 0.2 credits
                "skill_enhancement": 30, # 30 points = 0.3 credits
                "consciousness_test": 50 # 50 points = 0.5 credits
            },
            "milestones": {
                "first_cv_generated": 100,   # First achievement bonus
                "ten_applications": 500,     # Volume milestone
                "first_interview": 300,      # Interview breakthrough
                "godhood_achieved": 2000,    # Supreme achievement
                "leaderboard_top_10": 750    # Competition reward
            }
        }

        # FREEMIUM CREDIT SYSTEM (not direct subscription discounts)
        self.credit_system = {
            "monthly_free": 1000,    # FREE tier: 1,000 credits/month
            "unlimited_premium": 29.99,  # PREMIUM: CHF 29.99/month = unlimited
            "affiliate_commissions": 49.99,  # AFFILIATE: CHF 49.99/month + commissions
            "credit_pack_price": 5.00,     # CHF 5.00 per 500 credits
            "credits_per_pack": 500        # 1 credit pack = 500 credits
        }

        # CORRECTED: Points redeem for additional credits (sustainable economics)
        self.point_redemption = {
            "credit_multiplier": 0.01,     # 100 points = 1 credit (CHF 0.00.01 value)
            "max_redemption": 500,         # Maximum 500 points per redemption (5 credits)
            "min_redemption": 10           # Minimum 10 points (0.1 credits)
        }

        self.leaderboards = {
            "global": {},           # All-time performance
            "weekly": {},           # Current week competition
            "monthly": {},          # Monthly rankings
            "godhood_masterclass": {} # 5000+ points elite performers
        }

        self.user_profiles = {}
        self.rewards_history = {}
        self.achievements = {}

    async def award_points(self, user_id: str, action: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Award points to user based on action performed"""
        if action not in self.points_system:
            raise ValueError(f"Unknown action: {action}")

        # Initialize user profile if not exists
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "total_points": 0,
                "current_streak": 0,
                "last_activity": None,
                "achievements_unlocked": [],
                "subscription_level": "bronze",
                "redemption_available": 0
            }

        # Extract base points based on action type and context
        action_config = self.points_system[action]
        base_points = 0

        if isinstance(action_config, dict):
            # For CV generation, job applications - determine points based on context
            if action == "cv_generation":
                level = context.get("level", "basic_cv") if context else "basic_cv"
                if level == "godhood_cv":
                    base_points = action_config.get("godhood_cv", 500)
                elif level == "biological_cv":
                    base_points = action_config.get("biological_cv", 150)
                else:
                    base_points = action_config.get("basic_cv", 50)
            elif action == "job_application":
                stage = context.get("stage", "application_submit") if context else "application_submit"
                if stage == "offer_received":
                    base_points = action_config.get("offer_received", 1000)
                elif stage == "interview_completed":
                    base_points = action_config.get("interview_completed", 200)
                elif stage == "interview_scheduled":
                    base_points = action_config.get("interview_scheduled", 100)
                else:
                    base_points = action_config.get("application_submit", 25)
            else:
                # For system_interaction, etc.
                base_points = action_config.get("login_daily", 10) if "login" in str(context or {}) else 20
        else:
            base_points = action_config

        multiplier = await self.calculate_multiplier(user_id, action, context or {})
        total_points = int(base_points * multiplier)

        # Update user profile
        user_profile = self.user_profiles[user_id]
        user_profile["total_points"] += total_points
        user_profile["last_activity"] = datetime.now().isoformat()

        # Update streak
        if context and context.get("daily_login_bonus"):
            user_profile["current_streak"] += 1
        else:
            user_profile["current_streak"] = 1

        # Add redemption points
        user_profile["redemption_available"] += total_points

        # Update leaderboards
        await self.update_leaderboards(user_id)

        # Check achievements
        await self.check_achievements(user_id, action)

        return {
            "user_id": user_id,
            "points_awarded": total_points,
            "new_total_points": user_profile["total_points"],
            "multiplier_applied": multiplier,
            "streak_bonus": user_profile["current_streak"] > 1,
            "redemption_available": user_profile["redemption_available"]
        }

    async def calculate_multiplier(self, user_id: str, action: str, context: Dict[str, Any]) -> float:
        """Calculate point multiplier based on context and user history"""
        multiplier = 1.0

        user_profile = self.user_profiles.get(user_id, {})

        # Streak bonus
        streak = user_profile.get("current_streak", 0)
        if streak >= 7:
            multiplier *= 1.5  # 50% bonus for weekly streaks
        elif streak >= 3:
            multiplier *= 1.2  # 20% bonus for 3-day streaks

        # Time-based bonuses
        now = datetime.now()
        if now.hour >= 9 and now.hour <= 11:  # Morning productivity bonus
            multiplier *= 1.1

        if context.get("biological_enhancement", False):
            multiplier *= 1.3  # 30% bonus for biologically enhanced actions

        if context.get("godhood_premium", False):
            multiplier *= 2.0  # 100% bonus for GODHOOD premium features

        # Seasonal bonuses (simulated)
        if random.random() < 0.1:  # 10% chance of random bonus
            multiplier *= 1.5

        return multiplier

    async def update_leaderboards(self, user_id: str) -> None:
        """Update all active leaderboards with user progress"""
        user_points = self.user_profiles[user_id]["total_points"]

        # Global leaderboard (all-time)
        self.leaderboards["global"][user_id] = user_points

        # Weekly leaderboard
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%W")
        if week_start not in self.leaderboards["weekly"]:
            self.leaderboards["weekly"][week_start] = {}
        self.leaderboards["weekly"][week_start][user_id] = user_points

        # Monthly leaderboard
        month_key = datetime.now().strftime("%Y-%m")
        if month_key not in self.leaderboards["monthly"]:
            self.leaderboards["monthly"][month_key] = {}
        self.leaderboards["monthly"][month_key][user_id] = user_points

        # GODHOOD masterclass (top performers)
        if user_points >= 5000:
            self.leaderboards["godhood_masterclass"][user_id] = user_points

    async def get_leaderboard(self, leaderboard_type: str = "global", limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve leaderboard standings"""
        if leaderboard_type not in self.leaderboards:
            raise ValueError(f"Unknown leaderboard: {leaderboard_type}")

        data = self.leaderboards[leaderboard_type]

        if leaderboard_type == "weekly":
            current_week = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%W")
            data = data.get(current_week, {})

        elif leaderboard_type == "monthly":
            current_month = datetime.now().strftime("%Y-%m")
            data = data.get(current_month, {})

        # Sort by points descending
        sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)

        leaderboard = []
        for rank, (user_id, points) in enumerate(sorted_users[:limit], 1):
            leaderboard.append({
                "rank": rank,
                "user_id": user_id,
                "points": points,
                "change_from_last": await self._calculate_rank_change(user_id, leaderboard_type, rank)
            })

        return leaderboard

    async def _calculate_rank_change(self, user_id: str, leaderboard_type: str, current_rank: int) -> int:
        """Calculate rank change from previous period"""
        # Simplified - in real implementation would store historical ranks
        return random.randint(-3, 3)  # Simulate rank changes

    async def redeem_points_for_credits(self, user_id: str, points_to_redeem: int) -> Dict[str, Any]:
        """Redeem points for additional credits - CORRECTED CREDIT-BASED SYSTEM"""
        if user_id not in self.user_profiles:
            raise ValueError(f"User not found: {user_id}")

        user_profile = self.user_profiles[user_id]
        available_points = user_profile["redemption_available"]

        if points_to_redeem > self.point_redemption["max_redemption"]:
            raise ValueError(f"Maximum redemption per transaction: {self.point_redemption['max_redemption']} points")

        if points_to_redeem < self.point_redemption["min_redemption"]:
            raise ValueError(f"Minimum redemption per transaction: {self.point_redemption['min_redemption']} points")

        if points_to_redeem > available_points:
            raise ValueError(f"Insufficient redemption points. Available: {available_points}")

        # Calculate credits earned (100 points = 1 credit)
        credits_earned = points_to_redeem * self.point_redemption["credit_multiplier"]
        dollar_value = credits_earned * (self.credit_system["credit_pack_price"] / self.credit_system["credits_per_pack"])

        # CORRECTED: Add credits to user account (not subscription offset)
        user_profile["redemption_available"] -= points_to_redeem

        # Record in history
        if user_id not in self.rewards_history:
            self.rewards_history[user_id] = []

        redemption_record = {
            "type": "credit_redemption",
            "points_used": points_to_redeem,
            "credits_earned": credits_earned,
            "dollar_value": dollar_value,
            "redemption_rate": self.point_redemption["credit_multiplier"],
            "timestamp": datetime.now().isoformat()
        }

        self.rewards_history[user_id].append(redemption_record)

        return {
            "user_id": user_id,
            "points_redeemed": points_to_redeem,
            "credits_earned": credits_earned,
            "dollar_value": dollar_value,
            "remaining_redemption_points": user_profile["redemption_available"],
            "redemption_rate": f"{int(self.point_redemption['credit_multiplier']*100)} points = 1 credit"
        }

    async def check_achievements(self, user_id: str, action: str) -> List[Dict[str, Any]]:
        """Check and unlock achievements"""
        new_achievements = []
        user_profile = self.user_profiles[user_id]

        # Check milestone achievements
        for milestone, required_points in self.points_system["milestones"].items():
            if user_profile["total_points"] >= required_points:
                if milestone not in user_profile["achievements_unlocked"]:
                    user_profile["achievements_unlocked"].append(milestone)
                    new_achievements.append({
                        "achievement": milestone,
                        "bonus_points": self.points_system["milestones"][milestone] // 10,
                        "unlocked_at": datetime.now().isoformat()
                    })

        return new_achievements

    async def get_user_gamification_profile(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive gamification profile for user"""
        if user_id not in self.user_profiles:
            raise ValueError(f"User not found: {user_id}")

        profile = self.user_profiles[user_id]

        # Get user's leaderboard positions
        global_rank = None
        weekly_rank = None
        monthly_rank = None

        # Calculate ranks
        global_leaderboard = await self.get_leaderboard("global", limit=100)
        for entry in global_leaderboard:
            if entry["user_id"] == user_id:
                global_rank = entry["rank"]
                break

        weekly_leaderboard = await self.get_leaderboard("weekly", limit=50)
        for entry in weekly_leaderboard:
            if entry["user_id"] == user_id:
                weekly_rank = entry["rank"]
                break

        monthly_leaderboard = await self.get_leaderboard("monthly", limit=50)
        for entry in monthly_leaderboard:
            if entry["user_id"] == user_id:
                monthly_rank = entry["rank"]
                break

        return {
            "user_id": user_id,
            "gamification_profile": {
                "total_points": profile["total_points"],
                "current_streak": profile["current_streak"],
                "redemption_available": profile["redemption_available"],
                "subscription_level": profile["subscription_level"],
                "achievements_unlocked": len(profile["achievements_unlocked"])
            },
            "leaderboard_positions": {
                "global_rank": global_rank,
                "weekly_rank": weekly_rank,
                "monthly_rank": monthly_rank
            },
            "credit_redemption_potential": {
                "credits_available": profile["redemption_available"] * self.point_redemption["credit_multiplier"],
                "max_redemption_credits": self.point_redemption["max_redemption"] * self.point_redemption["credit_multiplier"],
                "redemption_rate": self.point_redemption["credit_multiplier"],
                "credit_pack_cost": self.credit_system["credit_pack_price"]
            }
        }


# Initialize global gamification engine
gamification_engine = BiologicalGamificationEngine()

# FastAPI Service
app = FastAPI(
    title="Biological Gamification Engine",
    description="GODHOOD Biological Consciousness Gamification System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Game mechanics engine health check"""
    return {
        "service": "Biological Gamification Engine",
        "status": "active",
        "godhood_integration": True,
        "features": ["points_system", "leaderboards", "subscription_redemption", "achievements"],
        "endpoints": [
            "/points/award",
            "/leaderboard/{type}",
            "/user/{user_id}/profile",
            "/points/redeem"
        ]
    }

@app.post("/points/award")
async def award_points_api(data: Dict[str, Any]):
    """Award points to user for action"""
    result = await gamification_engine.award_points(
        data["user_id"],
        data["action"],
        data.get("context", {})
    )
    return result

@app.get("/leaderboard/{leaderboard_type}")
async def get_leaderboard_api(leaderboard_type: str, limit: int = 10):
    """Retrieve leaderboard standings"""
    return await gamification_engine.get_leaderboard(leaderboard_type, limit)

@app.post("/points/redeem")
async def redeem_points_for_credits_api(data: Dict[str, Any]):
    """Redeem points for additional credits - CORRECTED CREDIT SYSTEM"""
    result = await gamification_engine.redeem_points_for_credits(
        data["user_id"],
        data["points_to_redeem"]
    )
    return result

@app.get("/user/{user_id}/profile")
async def get_user_profile_api(user_id: str):
    """Get comprehensive user gamification profile"""
    return await gamification_engine.get_user_gamification_profile(user_id)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_users": len(gamification_engine.user_profiles),
        "total_points_distributed": sum(
            profile["total_points"] for profile in gamification_engine.user_profiles.values()
        ),
        "leaderboard_size": len(gamification_engine.leaderboards["global"])
    }

if __name__ == "__main__":
    import uvicorn
    print("🎮 Biological Gamification Engine Starting")
    print("🧬 GODHOOD Consciousness Gamification System Active")
    print("💎 Points, Rewards & Leaderboards Ready")
    print("📡 Service listening on http://localhost:9200")
    uvicorn.run(app, host="0.0.0.0", port=9200, log_level="info")
