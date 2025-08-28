from enum import Enum

class UserType(Enum):
    CUSTOMER = "Customer"
    DRIVER = "Driver"

class OrderStatus(Enum):
    ACCEPTED = "Accepted"
    PREPARING = "Preparing"
    READY = "Ready for Pickup"
    PICKED_UP = "Picked Up"

class DeliveryStatus(Enum):
    PICKED_UP = "Picked Up"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"

class DriverStatus(Enum):
    OFF_DUTY = "Off Duty"
    AWAITING_ORDER = "Awaiting Order"
    ON_DELIVERY = "On Delivery"
