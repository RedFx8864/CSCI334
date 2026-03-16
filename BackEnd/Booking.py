class Booking:
    nextId = 1
    def __init__(self, bookingId, duration, date, startTime):
        self.bookingId = bookingId
        self.duration = duration
        self.date = date
        self.startTime = startTime
        
    @classmethod
    def createBooking(cls, duration, date, startTime):
        bookingId = f"booking{cls.nextId}"
        cls.nextId += 1
        return cls(bookingId, duration, date, startTime)