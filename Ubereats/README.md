# LLD Problem: Food Delivery System

You are tasked with designing a **Food Delivery System** similar to UberEats or DoorDash.

---

## Core Requirements

### 1. User Roles
- **Customer**
  - Browse restaurants
  - Place orders
  - Track order status
  - Make payments
- **Restaurant**
  - Manage menu items
  - Receive orders
  - Update preparation status
- **Delivery Agent**
  - Accept delivery requests
  - Update live location
  - Mark delivery as complete
- **Admin**
  - Manage restaurants, customers, and delivery agents

---

### 2. Order Flow
- Customer selects items from a restaurant’s menu and places an order.
- Restaurant accepts the order and updates status:
  - `Accepted → Preparing → Ready for Pickup`
- Delivery Agent is assigned and updates status:
  - `Picked Up → Out for Delivery → Delivered`
- Customer can track order in real time.

---

### 3. Payment
- Customer pays when placing the order (support Wallet or Card).
- System should handle refunds if the order is canceled before preparation starts.

---

### 4. Notifications
- Customers, Restaurants, and Delivery Agents should receive notifications when the order status changes.

---

## Non-Functional Requirements
- System should be **scalable** (handle thousands of simultaneous orders).
- **Real-time** order tracking should be supported.
- Support **basic reporting** for Admin:
  - Daily completed orders
  - Revenue per restaurant

---

## What to Design
- Identify **Classes** (with attributes and methods).
- Define **Relationships**:
  - Customer → Order → Restaurant → DeliveryAgent
- Sketch **Core APIs**:
  - `placeOrder`
  - `updateOrderStatus`
  - `assignDeliveryAgent`
  - `makePayment`
- Consider **Scalability & Extensibility**:
  - Adding coupons
  - Scheduled deliveries
  - Ratings & reviews

---

## Deliverables
- UML class diagram (entities and relationships)
- API design (endpoints and request/response flows)
- Discussion on scalability and extensibility
