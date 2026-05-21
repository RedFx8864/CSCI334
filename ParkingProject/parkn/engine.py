import math
from .models import Recommendation

class RecommendationEngine:
    
    # Recommends the best available parking spot for a user.
    
    # Scoring (higher = better):
    #    60% proximity  — closer to entry (1,1) = higher score
    #    40% availability — spot with fewest past bookings = higher score
    

    ENTRY_X = 1
    ENTRY_Y = 1

    def __init__(self, user, zone, date, startTime, duration, availableSpots):
        self.user = user
        self.zone = zone
        self.date = date
        self.startTime = startTime
        self.duration = duration
        self.availableSpots = availableSpots

    def _distance_score(self, spot):
        """Closer to entry point (1,1) = higher score."""
        distance = math.sqrt(
            (spot.xCoord - self.ENTRY_X) ** 2 +
            (spot.yCoord - self.ENTRY_Y) ** 2
        )
        # avoid division by zero if spot is exactly at entry
        return 1 / (1 + distance)

    def _popularity_score(self, spot):
        
        # Spots booked less often in the past score higher.
        # Less popular = more likely to be available in future too.
        
        bookingCount = spot.bookings.count()
        return 1 / (1 + bookingCount)

    def _compute_score(self, spot):
        return (
            0.60 * self._distance_score(spot) +
            0.40 * self._popularity_score(spot)
        )

    def _build_reason(self, spot, score):
        parts = []
        
        # check if it's the closest spot
        allDistances = [
            math.sqrt(
                (s.xCoord - self.ENTRY_X) ** 2 +
                (s.yCoord - self.ENTRY_Y) ** 2
            )
            for s in self.availableSpots
        ]
        spotDistance = math.sqrt(
            (spot.xCoord - self.ENTRY_X) ** 2 +
            (spot.yCoord - self.ENTRY_Y) ** 2
        )
        if spotDistance == min(allDistances):
            parts.append("closest to entrance")

        # check if it's the least booked spot
        allBookingCounts = [s.bookings.count() for s in self.availableSpots]
        if spot.bookings.count() == min(allBookingCounts):
            parts.append("least frequently booked")

        return ", ".join(parts) if parts else f"best overall score ({score:.2f})"

    def recommend(self):
        """
        Returns a saved Recommendation instance,
        or None if there are no available spots.
        """
        if not self.availableSpots:
            return None

        # score every available spot and pick the best
        bestSpot = max(self.availableSpots, key=self._compute_score)
        bestScore = self._compute_score(bestSpot)
        reason = self._build_reason(bestSpot, bestScore)

        rec = Recommendation.objects.create(
            user=self.user,
            parkingSpot=bestSpot,
            zone=self.zone,
            date=self.date,
            startTime=self.startTime,
            duration=self.duration,
            score=bestScore,
            reason=reason,
        )
        return rec