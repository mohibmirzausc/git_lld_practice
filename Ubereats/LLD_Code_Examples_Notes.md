# Food Delivery System LLD - Code Examples & Deep Analysis

## 1. Builder Pattern Implementation - Restaurant Creation

### The Code
```python
class RestaurantBuilder:
	def __init__(self) -> None:
		self.name: str = ""
		self.menu: Dict[str, float] = {}

	def set_name(self, name: str):
		self.name = name
		return self  # Method chaining

	def add_menu_item(self, name: str, price: float):
		self.menu[name.lower()] = round(float(price), 2)
		return self  # Method chaining

	def build(self):
		if not self.name or not self.menu:
			raise ValueError("Builder is missing components!")
		return Restaurant(self)

# Usage
restaurant = RestaurantBuilder() \
	.set_name("Stirred Roasters") \
	.add_menu_item("Matcha", 5.573) \
	.add_menu_item("Espresso Latte", 6.702) \
	.build()
```

### Why This Code is Strong
**Problem Solved**: Creating complex objects with validation without telescoping constructors.

**Key Strengths**:
1. **Method Chaining**: `return self` enables fluent interface
2. **Validation at Build**: Ensures object is complete before creation
3. **Type Safety**: Clear parameter types prevent errors
4. **Immutable Result**: Restaurant receives deep copy of menu
5. **Extensible**: Easy to add new restaurant properties

**Learning**: Builder pattern prevents invalid object states and makes complex creation readable. The validation at `build()` time ensures we never have incomplete restaurants in our system.

---

## 2. Restaurant Entity with Immutable Menu

### The Code
```python
class Restaurant:
    def __init__(self, builder: 'RestaurantBuilder') -> None:
        self.name = builder.name
        self.menu = copy.deepcopy(builder.menu)  # Defensive copy
    
    def get_name(self):
        return self.name
    
    def get_items(self):
        return self.menu.keys()
    
    def get_item_price(self, item_name: str) -> float:
        item_name = item_name.lower()
        if not self.menu.get(item_name):
            raise ValueError(f"Menu of {self.name} doesn't contain item {item_name}")
        
        return self.menu[item_name]
    
    def __str__(self) -> str:
        s = f"{self.name.capitalize()} offers: \n"
        s += "==============\n"
        for item_name, price in self.menu.items():
            s += f"{item_name}: {price}\n"
        s += "==============\n"
        return s
```

### Why This Code is Strong
**Problem Solved**: Immutable restaurant data with clear error handling for invalid menu access.

**Key Strengths**:
1. **Deep Copy Protection**: Menu can't be modified after creation
2. **Case Insensitive Lookup**: User-friendly item searching
3. **Descriptive Errors**: Clear feedback when items don't exist
4. **String Representation**: Readable display format
5. **Encapsulation**: Internal data protected through methods

**Learning**: Deep copying prevents external modification of critical business data. Case-insensitive lookups improve user experience while maintaining data consistency.

---

## 3. Order Builder with Complex Validation

### The Code
```python
class OrderBuilder:
    def __init__(self) -> None:
        self.customer: Customer = None
        self.restaurant: Restaurant = None
        self.items_ordered: Dict[str, int] = {}
        self.price = 0

    def set_customer(self, customer: Customer):
        if not isinstance(customer, Customer):
            raise TypeError("Must provide valid Customer instance")
        self.customer = customer
        return self

    def set_restaurant(self, restaurant: Restaurant):
        if not isinstance(restaurant, Restaurant):
            raise TypeError("Must provide valid Restaurant instance")
        self.restaurant = restaurant
        return self

    def order_item(self, name: str, amount: int):
        if not self.restaurant:
            raise ValueError("Cannot order if restaurant isn't set!")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Validate item exists
        if name.lower() not in self.restaurant.get_items():
            available_items = ", ".join(self.restaurant.get_items())
            raise ValueError(f"Item '{name}' not available. Available: {available_items}")

        # Calculate price and add to order
        item_price = self.restaurant.get_item_price(name.lower())
        self.price += item_price * amount

        # Handle multiple quantities of same item
        if name.lower() in self.items_ordered:
            self.items_ordered[name.lower()] += amount
        else:
            self.items_ordered[name.lower()] = amount

        return self

    def build(self):
        if not self.customer or not self.restaurant or not self.items_ordered:
            raise ValueError("Order build incomplete!")
        return Order(self)
```

### Why This Code is Strong
**Problem Solved**: Multi-step order creation with comprehensive validation at each step.

**Key Strengths**:
1. **Type Validation**: Runtime checks prevent wrong object types
2. **Business Rule Enforcement**: Can't order non-existent items
3. **Quantity Accumulation**: Handles multiple orders of same item
4. **Price Calculation**: Automatic total computation
5. **Helpful Error Messages**: Tells user what items are available

**Learning**: Validation at each step prevents error propagation. Accumulating quantities shows understanding of real-world ordering behavior.

---

## 4. Order Entity with Status Management

### The Code
```python
class Order:
    def __init__(self, order_builder: 'OrderBuilder') -> None:
        self.customer = order_builder.customer
        self.restaurant = order_builder.restaurant
        self.items_ordered: Dict[str, int] = copy.deepcopy(order_builder.items_ordered)
        self.price = order_builder.price
        self.order_status = OrderStatus.ACCEPTED
        self.delivery_status = None
        self.driver = None
        self.order_id = None
        self.payment_transaction_id = None
        self.created_at = datetime.now()

    def set_driver(self, driver: Driver):
        if not isinstance(driver, Driver):
            raise TypeError("Must provide valid Driver instance")
        self.driver = driver
        self.delivery_status = DeliveryStatus.ASSIGNED

    def set_order_id(self, order_id: str):
        if self.order_id:
            raise ValueError("Order ID already set")
        self.order_id = order_id

    def set_payment_transaction_id(self, transaction_id: str):
        self.payment_transaction_id = transaction_id

    def get_total_price(self) -> float:
        return round(self.price, 2)

    def get_order_summary(self) -> str:
        items_str = ", ".join([f"{item}(x{qty})" for item, qty in self.items_ordered.items()])
        return f"Items: {items_str}, Total: ${self.get_total_price()}"

    def progress_status(self):
        """Restaurant progresses order status"""
        if self.order_status == OrderStatus.ACCEPTED:
            self.order_status = OrderStatus.PREPARING
        elif self.order_status == OrderStatus.PREPARING:
            self.order_status = OrderStatus.READY
        elif self.order_status == OrderStatus.READY:
            self.order_status = OrderStatus.PICKED_UP
```

### Why This Code is Strong
**Problem Solved**: Immutable order data with controlled state transitions and payment tracking.

**Key Strengths**:
1. **Immutable Collections**: Deep copy prevents external modification
2. **Status Progression**: Logical workflow from accepted to picked up
3. **Payment Tracking**: Links orders to payment transactions
4. **Type Safety**: Validates driver assignment
5. **Audit Trail**: Creation timestamp for tracking

**Learning**: Orders are complex entities that need careful state management. The progression method ensures orders follow proper workflow sequence.

---

## 5. User Hierarchy with Polymorphism

### The Code
```python
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, id: str, type: UserType) -> None:
        self.id = id
        self.type = type
        self.messages: List[str] = []
        self.created_at = datetime.now()

    def get_id(self):
        return self.id
    
    def get_type(self):
        return self.type
    
    def receive_notification(self, msg: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_msg = f"[{timestamp}] {msg}"
        print(f"{self.id} received: {formatted_msg}")
        self.messages.append(formatted_msg)

    def get_notification_history(self) -> List[str]:
        return self.messages.copy()

class Customer(User):
    def __init__(self, id: str) -> None:
        super().__init__(id, UserType.CUSTOMER)
        self.past_orders: List['Order'] = []
        self.preferred_restaurants: Set[str] = set()

    def add_completed_order(self, order: 'Order'):
        self.past_orders.append(order)
        self.preferred_restaurants.add(order.restaurant.get_name())

    def get_order_history(self) -> List['Order']:
        return self.past_orders.copy()

class Driver(User):
    def __init__(self, id: str) -> None:
        super().__init__(id, UserType.DRIVER)
        self.driver_status: DriverStatus = DriverStatus.AWAITING_ORDER
        self.current_order_id: str = None
        self.total_deliveries: int = 0

    def set_driver_status(self, driver_status: DriverStatus):
        if not isinstance(driver_status, DriverStatus):
            raise TypeError("Invalid driver status type")
        self.driver_status = driver_status

    def assign_order(self, order_id: str):
        if self.driver_status != DriverStatus.AWAITING_ORDER:
            raise ValueError("Driver not available for new orders")
        self.current_order_id = order_id
        self.driver_status = DriverStatus.ON_DELIVERY

    def complete_delivery(self):
        self.current_order_id = None
        self.driver_status = DriverStatus.AWAITING_ORDER
        self.total_deliveries += 1
```

### Why This Code is Strong
**Problem Solved**: Common behavior across user types while maintaining role-specific functionality.

**Key Strengths**:
1. **Shared Interface**: All users receive notifications uniformly
2. **Role-Specific Data**: Each type has relevant attributes
3. **Notification History**: Timestamped message tracking
4. **Driver State Management**: Prevents double assignment
5. **Customer Preferences**: Tracks ordering patterns

**Learning**: Abstract base classes enable polymorphism while allowing specialization. The notification system works universally while each subclass maintains its specific data.

---

## 6. Enum-Based State Management

### The Code
```python
from enum import Enum

class OrderStatus(Enum):
    ACCEPTED = "Accepted"
    PREPARING = "Preparing"
    READY = "Ready for Pickup"
    PICKED_UP = "Picked Up"

class DeliveryStatus(Enum):
    ASSIGNED = "Driver Assigned"
    PICKED_UP = "Picked Up"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"

class DriverStatus(Enum):
    OFF_DUTY = "Off Duty"
    AWAITING_ORDER = "Awaiting Order"
    ON_DELIVERY = "On Delivery"

class PaymentStatus(Enum):
    PENDING = "Pending"
    PROCESSED = "Processed"
    FAILED = "Failed"
    REFUNDED = "Refunded"

# State transition validation
class StatusValidator:
    ORDER_TRANSITIONS = {
        OrderStatus.ACCEPTED: [OrderStatus.PREPARING],
        OrderStatus.PREPARING: [OrderStatus.READY],
        OrderStatus.READY: [OrderStatus.PICKED_UP],
        OrderStatus.PICKED_UP: []
    }

    DELIVERY_TRANSITIONS = {
        DeliveryStatus.ASSIGNED: [DeliveryStatus.PICKED_UP],
        DeliveryStatus.PICKED_UP: [DeliveryStatus.OUT_FOR_DELIVERY],
        DeliveryStatus.OUT_FOR_DELIVERY: [DeliveryStatus.DELIVERED],
        DeliveryStatus.DELIVERED: []
    }

    @classmethod
    def is_valid_order_transition(cls, current: OrderStatus, new: OrderStatus) -> bool:
        return new in cls.ORDER_TRANSITIONS.get(current, [])

    @classmethod
    def is_valid_delivery_transition(cls, current: DeliveryStatus, new: DeliveryStatus) -> bool:
        return new in cls.DELIVERY_TRANSITIONS.get(current, [])
```

### Why This Code is Strong
**Problem Solved**: Type-safe status management with enforced business rule transitions.

**Key Strengths**:
1. **Type Safety**: Enums prevent invalid string values
2. **State Machine Logic**: Clear valid transition mapping
3. **Centralized Validation**: Single source of truth for rules
4. **Readable Values**: Human-friendly enum descriptions
5. **IDE Support**: Auto-completion and refactoring

**Learning**: Enums combined with validator classes create robust state machines that prevent invalid business state transitions.

---

## 7. Singleton Service with Thread Safety

### The Code
```python
import threading
from typing import Dict, Optional

class FoodDeliveryService:
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._initialized = True
                    self.drivers: Dict[str, Driver] = {}
                    self.customers: Dict[str, Customer] = {}
                    self.restaurants: Dict[str, Restaurant] = {}
                    self.active_orders: Dict[str, Order] = {}
                    self.completed_orders: Dict[str, Order] = {}
                    self.driver_assignments: Dict[str, str] = {}
                    self._order_counter = 0
                    self.payment_processor = PaymentProcessor()

    def _generate_order_id(self) -> str:
        with self._lock:
            self._order_counter += 1
            return f"ORDER_{self._order_counter:06d}"

    def add_user(self, user: User):
        if isinstance(user, Driver):
            self.drivers[user.get_id()] = user
        elif isinstance(user, Customer):
            self.customers[user.get_id()] = user

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants[restaurant.get_name().lower()] = restaurant

    def get_available_drivers(self) -> List[Driver]:
        return [driver for driver in self.drivers.values() 
                if driver.get_driver_status() == DriverStatus.AWAITING_ORDER]

    def get_customer_orders(self, customer_id: str) -> List[Order]:
        customer = self.customers.get(customer_id)
        if not customer:
            return []
        return customer.get_order_history()
```

### Why This Code is Strong
**Problem Solved**: Thread-safe single source of truth for all system state.

**Key Strengths**:
1. **Double-Checked Locking**: Prevents race conditions
2. **Lazy Initialization**: Creates instance only when needed
3. **Thread-Safe ID Generation**: Atomic counter operations
4. **Type-Based Registration**: Automatic user categorization
5. **Query Methods**: Easy access to system state

**Learning**: Singleton ensures system consistency but requires careful thread safety. The service acts as the central registry for all system entities.

---

## 8. Payment Processing Integration

### The Code
```python
class PaymentMethod:
    def __init__(self, type: str, details: Dict[str, str]):
        self.type = type  # "CARD" or "WALLET"
        self.details = details

class PaymentResult:
    def __init__(self, success: bool, transaction_id: str = None, error_message: str = None):
        self.success = success
        self.transaction_id = transaction_id
        self.error_message = error_message
        self.timestamp = datetime.now()

class PaymentProcessor:
    def __init__(self):
        self.processed_payments: Dict[str, PaymentResult] = {}
        self._transaction_counter = 0

    def _generate_transaction_id(self) -> str:
        self._transaction_counter += 1
        return f"TXN_{self._transaction_counter:08d}"

    def charge(self, amount: float, payment_method: PaymentMethod, customer_id: str) -> PaymentResult:
        if amount <= 0:
            return PaymentResult(False, error_message="Invalid amount")

        transaction_id = self._generate_transaction_id()

        # Simulate payment processing
        try:
            if payment_method.type == "CARD":
                success = self._process_card_payment(amount, payment_method.details)
            elif payment_method.type == "WALLET":
                success = self._process_wallet_payment(amount, payment_method.details, customer_id)
            else:
                return PaymentResult(False, error_message="Unsupported payment method")

            result = PaymentResult(success, transaction_id)
            self.processed_payments[transaction_id] = result
            return result

        except Exception as e:
            return PaymentResult(False, error_message=str(e))

    def refund(self, transaction_id: str) -> PaymentResult:
        original_payment = self.processed_payments.get(transaction_id)
        if not original_payment or not original_payment.success:
            return PaymentResult(False, error_message="Invalid transaction for refund")

        refund_id = self._generate_transaction_id()
        refund_result = PaymentResult(True, refund_id)
        self.processed_payments[refund_id] = refund_result
        return refund_result

    def _process_card_payment(self, amount: float, card_details: Dict[str, str]) -> bool:
        # Simulate card validation
        required_fields = ["number", "cvv", "expiry"]
        return all(field in card_details for field in required_fields)

    def _process_wallet_payment(self, amount: float, wallet_details: Dict[str, str], customer_id: str) -> bool:
        # Simulate wallet balance check
        wallet_balance = float(wallet_details.get("balance", "0"))
        return wallet_balance >= amount
```

### Why This Code is Strong
**Problem Solved**: Handles payment processing with validation, error handling, and refund capability.

**Key Strengths**:
1. **Payment Method Abstraction**: Supports multiple payment types
2. **Transaction Tracking**: Every payment gets unique ID
3. **Error Handling**: Graceful failure with specific messages
4. **Refund Capability**: Supports order cancellation scenarios
5. **Validation Logic**: Checks payment method requirements

**Learning**: Payment processing requires careful error handling and transaction tracking. The abstraction allows easy addition of new payment methods.

---

## 9. Complete Order Placement Flow

### The Code
```python
def place_order(self, order: Order, payment_method: PaymentMethod) -> 'OrderResult':
    """Complete order placement with payment processing and notifications"""
    try:
        # Step 1: Validate order
        if not self._validate_order(order):
            return OrderResult(success=False, reason="Invalid order data")

        # Step 2: Generate order ID
        order_id = self._generate_order_id()
        order.set_order_id(order_id)

        # Step 3: Process payment
        payment_result = self.payment_processor.charge(
            amount=order.get_total_price(),
            payment_method=payment_method,
            customer_id=order.customer.get_id()
        )

        if not payment_result.success:
            return OrderResult(
                success=False, 
                reason=f"Payment failed: {payment_result.error_message}"
            )

        # Step 4: Link payment to order
        order.set_payment_transaction_id(payment_result.transaction_id)

        # Step 5: Add to active orders
        self.active_orders[order_id] = order

        # Step 6: Notify restaurant
        restaurant_msg = f"New order {order_id}: {order.get_order_summary()}"
        self._notify_restaurant_staff(order.restaurant, restaurant_msg)

        # Step 7: Notify customer
        customer_msg = f"Order {order_id} confirmed! Total: ${order.get_total_price()}"
        order.customer.receive_notification(customer_msg)

        # Step 8: Log successful order
        self._log_order_placement(order)

        return OrderResult(
            success=True, 
            order_id=order_id, 
            payment_id=payment_result.transaction_id
        )

    except Exception as e:
        # Critical: Rollback payment if order fails
        if 'payment_result' in locals() and payment_result.success:
            rollback_result = self.payment_processor.refund(payment_result.transaction_id)
            if not rollback_result.success:
                # Log critical error - payment charged but order failed
                self._log_critical_error(f"Payment rollback failed: {payment_result.transaction_id}")

        raise OrderProcessingException(f"Order placement failed: {str(e)}")

def _validate_order(self, order: Order) -> bool:
    """Comprehensive order validation"""
    if not order.customer or not order.restaurant:
        return False
    
    if not order.items_ordered:
        return False
    
    if order.get_total_price() <= 0:
        return False
    
    # Validate all items exist in restaurant menu
    for item_name in order.items_ordered.keys():
        if item_name not in order.restaurant.get_items():
            return False
    
    return True

class OrderResult:
    def __init__(self, success: bool, order_id: str = None, payment_id: str = None, reason: str = None):
        self.success = success
        self.order_id = order_id
        self.payment_id = payment_id
        self.reason = reason
        self.timestamp = datetime.now()
```

### Why This Code is Strong
**Problem Solved**: End-to-end order flow with error handling, rollbacks, and comprehensive validation.

**Key Strengths**:
1. **Transaction Consistency**: Rollback payment on order failure
2. **Step-by-Step Processing**: Clear workflow progression
3. **Comprehensive Validation**: Multi-level order checking
4. **Error Recovery**: Handles partial failures gracefully
5. **Audit Logging**: Tracks successful and failed operations

**Learning**: Complex business operations need careful error handling and rollback logic to maintain data consistency across multiple systems.

---

## 10. Driver Assignment and Delivery Management

### The Code
```python
def assign_driver(self, order_id: str, driver_id: str = None) -> bool:
    """Assign driver to ready order - auto or manual assignment"""
    order = self.active_orders.get(order_id)
    if not order:
        raise ValueError(f"Order {order_id} not found")

    if order.order_status != OrderStatus.READY:
        raise InvalidStateException("Cannot assign driver to order that's not ready")

    # Auto-assign if no specific driver requested
    if not driver_id:
        driver = self._find_available_driver()
        if not driver:
            return False
        driver_id = driver.get_id()
    else:
        driver = self.drivers.get(driver_id)
        if not driver:
            raise ValueError(f"Driver {driver_id} not found")

    # Validate driver availability
    if driver.get_driver_status() != DriverStatus.AWAITING_ORDER:
        return False

    # Make assignment
    order.set_driver(driver)
    driver.assign_order(order_id)
    self.driver_assignments[order_id] = driver_id

    # Notify both parties
    driver_msg = f"New delivery: {order.restaurant.get_name()} to {order.customer.get_id()}"
    driver.receive_notification(driver_msg)

    customer_msg = f"Driver {driver_id} assigned to order {order_id}"
    order.customer.receive_notification(customer_msg)

    return True

def update_delivery_status(self, order_id: str, driver_id: str, new_status: DeliveryStatus) -> bool:
    """Driver updates delivery status with business logic"""
    order = self.active_orders.get(order_id)
    
    # Authorization check
    if not order or self.driver_assignments.get(order_id) != driver_id:
        raise UnauthorizedException("Driver not authorized for this order")

    # Validate status transition
    if not StatusValidator.is_valid_delivery_transition(order.delivery_status, new_status):
        raise InvalidTransitionException(
            f"Cannot transition from {order.delivery_status.value} to {new_status.value}"
        )

    # Update status
    old_status = order.delivery_status
    order.delivery_status = new_status

    # Handle status-specific logic
    if new_status == DeliveryStatus.PICKED_UP:
        order.order_status = OrderStatus.PICKED_UP
        customer_msg = "Your order has been picked up!"
        order.customer.receive_notification(customer_msg)

    elif new_status == DeliveryStatus.OUT_FOR_DELIVERY:
        estimated_time = self._calculate_delivery_eta(order)
        customer_msg = f"Order out for delivery! ETA: {estimated_time} minutes"
        order.customer.receive_notification(customer_msg)

    elif new_status == DeliveryStatus.DELIVERED:
        self._complete_delivery(order_id)

    return True

def _complete_delivery(self, order_id: str):
    """Complete delivery and clean up resources"""
    order = self.active_orders.pop(order_id)
    driver = order.driver

    # Update driver availability
    driver.complete_delivery()

    # Move to completed orders
    self.completed_orders[order_id] = order

    # Update customer history
    order.customer.add_completed_order(order)

    # Clean up assignment tracking
    self.driver_assignments.pop(order_id, None)

    # Final notifications
    order.customer.receive_notification("Order delivered successfully!")
    driver.receive_notification("Delivery completed. Ready for next order.")

def _find_available_driver(self) -> Optional[Driver]:
    """Find available driver using simple round-robin"""
    available_drivers = self.get_available_drivers()
    if not available_drivers:
        return None
    
    # Simple algorithm - can be enhanced with location, ratings, etc.
    return available_drivers[0]
```

### Why This Code is Strong
**Problem Solved**: Complete delivery workflow with authorization, validation, and resource cleanup.

**Key Strengths**:
1. **Authorization Checks**: Only assigned drivers can update orders
2. **Auto-Assignment**: System can find available drivers automatically
3. **State Validation**: Prevents invalid status transitions
4. **Resource Cleanup**: Proper cleanup when deliveries complete
5. **Business Logic**: ETA calculation and customer updates

**Learning**: Delivery management requires careful authorization and state management. The cleanup logic ensures system resources are properly managed as orders complete.

---

## 11. Order Cancellation with Refunds

### The Code
```python
def cancel_order(self, order_id: str, requester_id: str, reason: str) -> 'CancellationResult':
    """Cancel order with refund logic based on current status"""
    order = self.active_orders.get(order_id)
    if not order:
        return CancellationResult(False, "Order not found")

    # Authorization - only customer or admin can cancel
    if requester_id != order.customer.get_id() and not self._is_admin(requester_id):
        return CancellationResult(False, "Not authorized to cancel this order")

    # Determine refund eligibility
    refund_eligible = order.order_status in [OrderStatus.ACCEPTED, OrderStatus.PREPARING]
    refund_amount = order.get_total_price() if refund_eligible else 0

    try:
        # Process refund if eligible
        if refund_eligible and order.payment_transaction_id:
            refund_result = self.payment_processor.refund(order.payment_transaction_id)
            if not refund_result.success:
                return CancellationResult(False, "Refund processing failed")

        # Release driver if assigned
        if order.driver:
            driver = order.driver
            driver.complete_delivery()  # This frees up the driver
            driver_msg = f"Order {order_id} cancelled. You're now available for new orders."
            driver.receive_notification(driver_msg)
            self.driver_assignments.pop(order_id, None)

        # Remove from active orders
        self.active_orders.pop(order_id)

        # Notify customer
        if refund_eligible:
            customer_msg = f"Order cancelled. Refund of ${refund_amount} processed."
        else:
            customer_msg = f"Order cancelled. No refund (order was {order.order_status.value})."
        
        order.customer.receive_notification(customer_msg)

        # Log cancellation
        self._log_cancellation(order_id, reason, refund_amount)

        return CancellationResult(True, "Order cancelled successfully", refund_amount)

    except Exception as e:
        return CancellationResult(False, f"Cancellation failed: {str(e)}")

class CancellationResult:
    def __init__(self, success: bool, message: str, refund_amount: float = 0):
        self.success = success
        self.message = message
        self.refund_amount = refund_amount
        self.timestamp = datetime.now()
```

### Why This Code is Strong
**Problem Solved**: Handles order cancellation with business rules for refunds and resource cleanup.

**Key Strengths**:
1. **Authorization Logic**: Controls who can cancel orders
2. **Refund Rules**: Business logic for when refunds apply
3. **Resource Cleanup**: Frees up assigned drivers
4. **Status-Based Logic**: Different handling based on order progress
5. **Comprehensive Notifications**: All parties informed of cancellation

**Learning**: Cancellation requires understanding of business rules around refunds and the cascading effects on other system resources like driver assignments.

---

## 12. Restaurant Status Updates

### The Code
```python
def update_restaurant_status(self, order_id: str, new_status: OrderStatus, restaurant_id: str) -> bool:
    """Restaurant updates order preparation status"""
    order = self.active_orders.get(order_id)
    if not order:
        raise ValueError(f"Order {order_id} not found")

    # Authorization - only the restaurant can update their orders
    if order.restaurant.get_name().lower() != restaurant_id.lower():
        raise UnauthorizedException("Restaurant not authorized for this order")

    # Validate status transition
    if not StatusValidator.is_valid_order_transition(order.order_status, new_status):
        raise InvalidTransitionException(
            f"Cannot transition from {order.order_status.value} to {new_status.value}"
        )

    # Update status
    old_status = order.order_status
    order.order_status = new_status

    # Handle status-specific business logic
    if new_status == OrderStatus.PREPARING:
        prep_time = self._estimate_preparation_time(order)
        customer_msg = f"Your order is being prepared. Estimated time: {prep_time} minutes"
        order.customer.receive_notification(customer_msg)

    elif new_status == OrderStatus.READY:
        order.customer.receive_notification("Your order is ready for pickup!")
        
        # Trigger driver assignment for ready orders
        assignment_success = self.assign_driver(order_id)
        if not assignment_success:
            # No drivers available - notify customer
            order.customer.receive_notification("Looking for available driver...")
            self._queue_for_driver_assignment(order_id)

    return True

def _estimate_preparation_time(self, order: Order) -> int:
    """Estimate preparation time based on items ordered"""
    base_time = 15  # Base 15 minutes
    item_count = sum(order.items_ordered.values())
    
    # Add 3 minutes per additional item
    additional_time = max(0, item_count - 1) * 3
    
    return base_time + additional_time

def _queue_for_driver_assignment(self, order_id: str):
    """Queue order for driver assignment when drivers become available"""
    if not hasattr(self, 'pending_assignments'):
        self.pending_assignments = []
    
    self.pending_assignments.append(order_id)

def check_pending_assignments(self):
    """Check for orders waiting for driver assignment"""
    if not hasattr(self, 'pending_assignments'):
        return

    available_drivers = self.get_available_drivers()
    if not available_drivers:
        return

    # Assign drivers to waiting orders
    while self.pending_assignments and available_drivers:
        order_id = self.pending_assignments.pop(0)
        if order_id in self.active_orders:  # Order might have been cancelled
            driver = available_drivers.pop(0)
            self.assign_driver(order_id, driver.get_id())
```

### Why This Code is Strong
**Problem Solved**: Restaurant workflow management with automatic driver assignment and queue handling.

**Key Strengths**:
1. **Authorization Control**: Only restaurants can update their orders
2. **Business Logic**: Preparation time estimation based on order complexity
3. **Automatic Triggers**: Ready status triggers driver assignment
4. **Queue Management**: Handles driver shortage scenarios
5. **Customer Communication**: Proactive status updates

**Learning**: Restaurant status updates have cascading effects throughout the system. The queue mechanism handles resource constraints gracefully.

---

## Abstract Base Class with Polymorphism

### The Code
```python
from abc import ABC, abstractmethod
from enums import UserType

class User(ABC):
    def __init__(self, id: str, type: UserType) -> None:
        self.id = id
        self.type = type
        self.messages: List[str] = []

    def receive_notification(self, msg: str):
        print(f"{self.id} received a notification: ", msg)
        self.messages.append(msg)

class Customer(User):
    def __init__(self, id: str) -> None:
        super().__init__(id, UserType.CUSTOMER)
        self.past_orders: List['Order'] = []

class Driver(User):
    def __init__(self, id: str) -> None:
        super().__init__(id, UserType.DRIVER)
        self.driver_status: DriverStatus = DriverStatus.AWAITING_ORDER

    def set_driver_status(self, driver_status: DriverStatus):
        self.driver_status = driver_status
```

### Why This Code is Strong
**Problem Solved**: Common behavior across user types while maintaining type-specific functionality.

**Key Strengths**:
1. **Shared Behavior**: All users can receive notifications
2. **Type Safety**: Enum prevents invalid user types
3. **Extensibility**: Easy to add new user types (Admin, Restaurant Owner)
4. **Polymorphism**: Can treat all users uniformly for notifications
5. **Domain-Specific Properties**: Each subclass has relevant attributes

**Learning**: Abstract base classes provide a contract while allowing specialization. The notification system works for any user type, demonstrating the power of inheritance for shared functionality.

---

## Service Layer - Complete Order Flow Implementation

### The Code
```python
class FoodDeliveryService:
    def __init__(self):
        self.payment_processor = PaymentProcessor()
        self.notification_service = NotificationService()
        self.drivers: Dict[str, Driver] = {}
        self.customers: Dict[str, Customer] = {}
        self.restaurants: Dict[str, Restaurant] = {}
        self.active_orders: Dict[str, Order] = {}
        self.completed_orders: Dict[str, Order] = {}
        self.driver_assignments: Dict[str, str] = {}  # order_id -> driver_id

    def place_order(self, order: Order, payment_method: PaymentMethod) -> OrderResult:
        """Complete order placement with payment processing"""
        try:
            # Step 1: Validate order
            if not self._validate_order(order):
                return OrderResult(success=False, reason="Invalid order")

            # Step 2: Process payment first
            payment_result = self.payment_processor.charge(
                amount=order.get_total_price(),
                payment_method=payment_method,
                customer_id=order.customer.get_id()
            )

            if not payment_result.success:
                return OrderResult(success=False, reason="Payment failed")

            # Step 3: Confirm order and set payment reference
            order.set_payment_transaction_id(payment_result.transaction_id)
            order.set_order_id(self._generate_order_id())
            self.active_orders[order.order_id] = order

            # Step 4: Notify restaurant
            restaurant_msg = f"New order {order.order_id}: {order.get_order_summary()}"
            self._notify_restaurant(order.restaurant, restaurant_msg)

            # Step 5: Notify customer
            customer_msg = f"Order {order.order_id} confirmed. Payment processed: ${order.get_total_price()}"
            order.customer.receive_notification(customer_msg)

            return OrderResult(success=True, order_id=order.order_id, payment_id=payment_result.transaction_id)

        except Exception as e:
            # Rollback payment if it was processed
            if 'payment_result' in locals() and payment_result.success:
                self.payment_processor.refund(payment_result.transaction_id)
            raise OrderProcessingException(f"Order placement failed: {str(e)}")

    def update_restaurant_status(self, order_id: str, new_status: OrderStatus) -> bool:
        """Restaurant updates preparation status"""
        order = self.active_orders.get(order_id)
        if not order:
            return False

        # Validate status progression
        if not self._is_valid_status_transition(order.order_status, new_status):
            return False

        old_status = order.order_status
        order.order_status = new_status

        # Handle status-specific logic
        if new_status == OrderStatus.PREPARING:
            estimated_time = self._calculate_prep_time(order)
            msg = f"Your order is being prepared. Estimated time: {estimated_time} minutes"
            order.customer.receive_notification(msg)

        elif new_status == OrderStatus.READY:
            # Trigger driver assignment
            self._auto_assign_driver(order_id)
            order.customer.receive_notification("Your order is ready for pickup!")

        return True

    def assign_driver(self, order_id: str, driver_id: str) -> bool:
        """Assign available driver to ready order"""
        order = self.active_orders.get(order_id)
        driver = self.drivers.get(driver_id)

        if not order or not driver:
            return False

        # Validate preconditions
        if order.order_status != OrderStatus.READY:
            raise InvalidStateException("Cannot assign driver to order that's not ready")

        if driver.get_driver_status() != DriverStatus.AWAITING_ORDER:
            return False

        # Make assignment
        order.set_driver(driver)
        driver.set_driver_status(DriverStatus.ON_DELIVERY)
        self.driver_assignments[order_id] = driver_id

        # Initialize delivery tracking
        order.delivery_status = DeliveryStatus.ASSIGNED

        # Notify both parties with actionable information
        driver_msg = f"New delivery: {order.restaurant.get_name()} → Customer {order.customer.get_id()}"
        driver.receive_notification(driver_msg)

        customer_msg = f"Driver {driver_id} assigned. Track your order: {order_id}"
        order.customer.receive_notification(customer_msg)

        return True

    def update_delivery_status(self, order_id: str, driver_id: str, new_status: DeliveryStatus) -> bool:
        """Driver updates delivery status with validation"""
        order = self.active_orders.get(order_id)

        # Verify driver authorization
        if not order or self.driver_assignments.get(order_id) != driver_id:
            raise UnauthorizedException("Driver not authorized for this order")

        old_status = order.delivery_status
        order.delivery_status = new_status

        # Handle status-specific business logic
        if new_status == DeliveryStatus.PICKED_UP:
            order.order_status = OrderStatus.PICKED_UP
            order.customer.receive_notification("Your order has been picked up by the driver!")

        elif new_status == DeliveryStatus.OUT_FOR_DELIVERY:
            estimated_arrival = self._calculate_delivery_time(order)
            msg = f"Your order is out for delivery! Estimated arrival: {estimated_arrival}"
            order.customer.receive_notification(msg)

        elif new_status == DeliveryStatus.DELIVERED:
            self._complete_order(order_id)

        return True

    def _complete_order(self, order_id: str):
        """Complete order and clean up resources"""
        order = self.active_orders.pop(order_id)
        driver = order.driver

        # Update driver availability
        driver.set_driver_status(DriverStatus.AWAITING_ORDER)

        # Move to completed orders
        self.completed_orders[order_id] = order

        # Add to customer history
        order.customer.past_orders.append(order)

        # Final notifications
        order.customer.receive_notification("Order delivered successfully! Thank you for using our service.")

        # Clean up assignment tracking
        self.driver_assignments.pop(order_id, None)

    def cancel_order(self, order_id: str, reason: str) -> bool:
        """Cancel order with refund if applicable"""
        order = self.active_orders.get(order_id)
        if not order:
            return False

        # Check if refund is applicable
        if order.order_status in [OrderStatus.ACCEPTED, OrderStatus.PREPARING]:
            refund_result = self.payment_processor.refund(order.payment_transaction_id)
            if refund_result.success:
                order.customer.receive_notification(f"Order cancelled. Refund processed: ${order.get_total_price()}")
            else:
                order.customer.receive_notification("Order cancelled. Refund failed - contact support.")

        # Release driver if assigned
        if order.driver:
            order.driver.set_driver_status(DriverStatus.AWAITING_ORDER)
            self.driver_assignments.pop(order_id, None)

        # Remove from active orders
        self.active_orders.pop(order_id)

        return True
```

### Why This Service Layer is Strong

**Problem Solved**: Coordinates complex business workflows across multiple entities while maintaining data consistency.

**Key Strengths**:

1. **Transaction Management**: Payment processed first, with rollback on failure
2. **State Validation**: Prevents invalid state transitions
3. **Error Handling**: Comprehensive exception handling with cleanup
4. **Authorization**: Drivers can only update their assigned orders
5. **Business Logic Encapsulation**: All workflow logic in one place
6. **Resource Management**: Proper cleanup when orders complete
7. **Notification Coordination**: Relevant parties informed at each step

**Learning**: The service layer acts as the orchestrator, ensuring business rules are followed while coordinating between entities. Notice how payment failures trigger rollbacks, and how driver assignments are validated before execution.

---

## Order Builder with Validation

### The Code
```python
class OrderBuilder:
    def __init__(self) -> None:
        self.customer: Customer = None
        self.restaurant: Restaurant = None
        self.items_ordered: Dict[str, int] = {}
        self.price = 0

    def set_customer(self, customer: Customer):
        if not isinstance(customer, Customer):
            raise TypeError("Must provide valid Customer instance")
        self.customer = customer
        return self

    def set_restaurant(self, restaurant: Restaurant):
        if not isinstance(restaurant, Restaurant):
            raise TypeError("Must provide valid Restaurant instance")
        self.restaurant = restaurant
        return self

    def order_item(self, name: str, amount: int):
        if not self.restaurant:
            raise ValueError("Cannot order if restaurant isn't set!")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Validate item exists
        if name.lower() not in self.restaurant.get_items():
            available_items = ", ".join(self.restaurant.get_items())
            raise ValueError(f"Item '{name}' not available. Available: {available_items}")

        # Calculate price and add to order
        item_price = self.restaurant.get_item_price(name.lower())
        self.price += item_price * amount

        # Handle multiple quantities of same item
        if name.lower() in self.items_ordered:
            self.items_ordered[name.lower()] += amount
        else:
            self.items_ordered[name.lower()] = amount

        return self

    def build(self):
        # Comprehensive validation
        if not self.customer:
            raise ValueError("Order must have a customer")
        if not self.restaurant:
            raise ValueError("Order must have a restaurant")
        if not self.items_ordered:
            raise ValueError("Order must have at least one item")

        return Order(self)

# Usage demonstrating validation
try:
    order = OrderBuilder() \
        .set_customer(customer) \
        .set_restaurant(restaurant) \
        .order_item("matcha", 2) \
        .order_item("muffin", 1) \
        .build()
except ValueError as e:
    print(f"Order creation failed: {e}")
```

### Why This Code is Strong

**Problem Solved**: Prevents creation of invalid orders while providing clear error messages.

**Key Strengths**:
1. **Incremental Validation**: Each step validates its preconditions
2. **Type Safety**: Runtime type checking prevents wrong object types
3. **Business Rule Enforcement**: Can't order items that don't exist
4. **Clear Error Messages**: Specific feedback about what's wrong
5. **Quantity Handling**: Properly accumulates multiple items
6. **Price Calculation**: Automatically tracks total cost

**Learning**: Builder pattern with validation ensures that by the time `build()` is called, all business rules have been satisfied. The early validation prevents cascading errors later in the system.

---

## Enum-Based State Management

### The Code
```python
from enum import Enum

class OrderStatus(Enum):
    ACCEPTED = "Accepted"
    PREPARING = "Preparing"
    READY = "Ready for Pickup"
    PICKED_UP = "Picked Up"

class DeliveryStatus(Enum):
    ASSIGNED = "Driver Assigned"
    PICKED_UP = "Picked Up"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"

# State transition validation
def _is_valid_status_transition(current: OrderStatus, new: OrderStatus) -> bool:
    """Enforce valid state transitions"""
    valid_transitions = {
        OrderStatus.ACCEPTED: [OrderStatus.PREPARING],
        OrderStatus.PREPARING: [OrderStatus.READY],
        OrderStatus.READY: [OrderStatus.PICKED_UP],
        OrderStatus.PICKED_UP: []  # Terminal state for restaurant
    }
    return new in valid_transitions.get(current, [])

# Usage in service layer
def update_restaurant_status(self, order_id: str, new_status: OrderStatus) -> bool:
    order = self.active_orders.get(order_id)
    if not order:
        return False

    if not self._is_valid_status_transition(order.order_status, new_status):
        raise InvalidTransitionException(
            f"Cannot transition from {order.order_status.value} to {new_status.value}"
        )

    order.order_status = new_status
    return True
```

### Why This Code is Strong

**Problem Solved**: Prevents invalid state transitions and provides type-safe status management.

**Key Strengths**:
1. **Type Safety**: Enums prevent typos and invalid values
2. **State Machine Logic**: Clear definition of valid transitions
3. **Business Rule Enforcement**: Can't skip steps in the workflow
4. **Readable Code**: Enum values are human-readable
5. **IDE Support**: Auto-completion and refactoring support

**Learning**: Enums combined with validation functions create a robust state machine. This prevents bugs where orders might skip preparation or drivers try to deliver unready orders.

---

## Singleton Service with Thread Safety

### The Code
```python
import threading

class FoodDeliveryService:
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if not cls._instance:
            with cls._lock:  # Thread-safe singleton
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._initialized = True
                    self.drivers: Dict[str, Driver] = {}
                    self.customers: Dict[str, Customer] = {}
                    self.restaurants: Dict[str, Restaurant] = {}
                    self.active_orders: Dict[str, Order] = {}
                    self._order_counter = 0

    def _generate_order_id(self) -> str:
        """Thread-safe order ID generation"""
        with self._lock:
            self._order_counter += 1
            return f"ORDER_{self._order_counter:06d}"

# Usage - always returns same instance
service1 = FoodDeliveryService()
service2 = FoodDeliveryService()
assert service1 is service2  # Same instance
```

### Why This Code is Strong

**Problem Solved**: Ensures single source of truth for system state while being thread-safe.

**Key Strengths**:
1. **Thread Safety**: Double-checked locking prevents race conditions
2. **Lazy Initialization**: Only creates instance when needed
3. **Memory Efficiency**: One instance serves entire application
4. **State Consistency**: All components share same service state
5. **ID Generation**: Thread-safe unique ID creation

**Learning**: Singleton pattern ensures system consistency but requires careful thread safety consideration. The double-checked locking pattern is a classic solution for thread-safe singletons.

---

## Comprehensive Error Handling

### The Code
```python
class OrderProcessingException(Exception):
    def __init__(self, message: str, order_id: str = None, error_code: str = None):
        super().__init__(message)
        self.order_id = order_id
        self.error_code = error_code

class PaymentException(Exception):
    def __init__(self, message: str, transaction_id: str = None):
        super().__init__(message)
        self.transaction_id = transaction_id

# Usage in service methods
def place_order(self, order: Order, payment_method: PaymentMethod) -> OrderResult:
    try:
        # Payment processing
        payment_result = self.payment_processor.charge(
            amount=order.get_total_price(),
            payment_method=payment_method
        )

        if not payment_result.success:
            raise PaymentException(
                f"Payment failed: {payment_result.error_message}",
                transaction_id=payment_result.transaction_id
            )

        # Order processing
        order.set_payment_transaction_id(payment_result.transaction_id)
        self.active_orders[order.order_id] = order

        return OrderResult(success=True, order_id=order.order_id)

    except PaymentException as e:
        # Log payment specific error
        self.logger.error(f"Payment failed for customer {order.customer.get_id()}: {e}")
        return OrderResult(success=False, reason="Payment processing failed")

    except Exception as e:
        # Rollback any partial state
        if 'payment_result' in locals() and payment_result.success:
            self.payment_processor.refund(payment_result.transaction_id)

        raise OrderProcessingException(
            f"Order placement failed: {str(e)}",
            order_id=getattr(order, 'order_id', None),
            error_code="ORDER_PLACEMENT_FAILED"
        )
```

### Why This Code is Strong

**Problem Solved**: Provides specific error information while maintaining system consistency through rollbacks.

**Key Strengths**:
1. **Specific Exceptions**: Different error types for different failure modes
2. **Error Context**: Includes relevant IDs and error codes
3. **Rollback Logic**: Maintains system consistency on failures
4. **Logging Integration**: Structured error information for debugging
5. **User-Friendly Messages**: Clear feedback to calling code

**Learning**: Good error handling provides specific information about what went wrong while ensuring the system remains in a consistent state. Rollback logic is crucial for operations that span multiple systems.

---

## Key Interview Insights

When discussing this code in an interview, emphasize:

1. **Design Decisions**: Why you chose Builder over telescoping constructors
2. **State Management**: How enums prevent invalid transitions
3. **Error Handling**: The importance of rollback logic in distributed operations
4. **Thread Safety**: Why singleton needs careful implementation
5. **Validation Strategy**: How early validation prevents cascading failures

This codebase demonstrates understanding of enterprise-level concerns: consistency, reliability, maintainability, and scalability. 