from abc import ABC, abstractmethod

# strategy pattern
class FeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket):
        pass

class RegularFeeStrategy(FeeStrategy):
    def calculate_fee(self, ticket):
        duration = (ticket.exit - ticket.entry).total_seconds() / 3600
        return duration * 2  # $2 per hour

class PremiumFeeStrategy(FeeStrategy):
    def calculate_fee(self, ticket):
        duration = (ticket.exit - ticket.entry).total_seconds() / 3600
        return 25 + duration * 5  # $5 per hour

class Ticket:
    def __init__(self, ticket_id, vehicle, spot):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry = None
        self.exit = None
        self.fee_strategy = None

    def mark_entry(self):
        from datetime import datetime
        self.entry = datetime.now()

    def mark_exit(self):
        from datetime import datetime
        self.exit = datetime.now()

    def set_fee_strategy(self, strategy):
        self.fee_strategy = strategy

    def calculate_fee(self):
        if self.fee_strategy and self.entry and self.exit:
            return self.fee_strategy.calculate_fee(self)
        return 0

# Example usage:
ticket = Ticket("T123", "Car", "Spot1")
ticket.mark_entry()
# ...time passes...
ticket.mark_exit()
ticket.set_fee_strategy(RegularFeeStrategy())
fee = ticket.calculate_fee()
print(f"Parking fee: ${fee:.2f}")