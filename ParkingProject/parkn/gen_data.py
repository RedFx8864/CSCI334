from .models import HourAvailability
import random
import datetime

class GenData:
    #Calculating data for predicitive system
    def calcAvailability(m, d, h):
        total = 0
        x=random.gauss

        #Occupied parking for the days
        match h:
            case 0:
                total = random.randint(0, 2)
            case 1:
                total = random.randint(0, 3)
            case 2:
                total = random.randint(0, 10)
            case 3:
                total = random.randint(0, 12)
            case 4:
                total = random.randint(0, 15)
            case 5:
                total = random.randint(5, 35)
            case 6:
                total = random.randint(10, 50)
            case 7:
                total = random.randint(20, 65)
            case 8:
                total = random.randint(25, 85)
            case 9:
                total = random.randint(30, 100)
            case 10:
                total = random.randint(50, 100)
            case 11:
                total = random.randint(80, 100)
            case 12:
                total = random.randint(70, 100)     
            case 13:
                total = random.randint(60, 100)
            case 14:
                total = random.randint(50, 100)
            case 15:
                total = random.randint(30, 90)
            case 16:
                total = random.randint(25, 80)
            case 17:
                total = random.randint(20, 70)
            case 18:
                total = random.randint(15, 60)
            case 19:
                total = random.randint(15, 45)
            case 20:
                total = random.randint(0, 40)
            case 21:
                total = random.randint(0, 30)
            case 22:
                total = random.randint(0, 20)
            case 23:
                total = random.randint(0, 10) 

        #Modifiers dependant on day of week
        match d:
            case 3|4:
                x = random.uniform(0.5, 0.9)
                total = (total*x)//1
            case 5|6:
                x = random.uniform(0.2, 0.6)
                total = (total*x)//1
            case _:
                pass

        #Modifiers for uni holidays
        if (m==11) or (m==6):
            x=random.uniform(0.2, 0.9)
            total = (total*x)//1
            
        return total

    #Code runner to store test data in server
    def runner(self):
        m=0
        d=0
        h=0
        while m<11:
            while d<30:
                while h<23:
                    #Catching dates that can't exist
                    try:
                        HourAvailability.createHourAvailability((datetime.datetime((2025), (1+m), (1+d), (h))), (self.calcAvailability(m,d,h)))
                        h=+1
                    except ValueError:
                        h=+1
                        continue
                h=0
                d=+1
            d=0
            m=+1