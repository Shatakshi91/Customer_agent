# 05 — API Specification

**Project:** AI-Powered E-commerce Customer Support Agent  
**Document:** API Specification  
**Version:** 1.1  
**Status:** Revised Draft — Pending Cross-Document Consistency Review and User Approval  
**Base URL (Development):** `http://localhost:8000/api/v1`  
**API Style:** REST  
**Data Format:** JSON  
**Authentication:** JWT Access Token + Rotating Refresh Token Cookie  
**Backend:** Python, FastAPI

---

# 1. Introduction

## 1.1 Purpose

This document defines the API contracts for the AI-Powered E-commerce Customer Support Agent.

It specifies:

- API endpoint paths.
- HTTP methods.
- Authentication requirements.
- Role and permission requirements.
- Request and response formats.
- HTTP status codes.
- Validation rules.
- Error-handling conventions.
- Pagination.
- AI chat streaming.
- Postman testing requirements.

## 1.2 API Design Principles

The API shall follow these principles:

1. Use REST conventions.
2. Use meaningful resource names.
3. Use appropriate HTTP methods.
4. Validate every incoming request.
5. Apply authentication to protected endpoints.
6. Apply resource-level authorization.
7. Return consistent JSON responses.
8. Use pagination for collection endpoints.
9. Use transactions for critical business operations.
10. Use idempotency protection for sensitive operations.
11. Never trust customer identity supplied by the LLM.
12. Never expose internal database errors or sensitive information.

## 1.3 Base URL

Development:

```text
http://localhost:8000/api/v1
```

Production:

```text
https://your-domain.com/api/v1
```

The production domain will be selected during deployment.

## 1.4 API Versioning

All application endpoints shall use:

```text
/api/v1/
```

Breaking API changes shall be introduced through a new API version when required.

## 1.5 Content Types

| Operation | Content-Type |
|---|---|
| Standard JSON request | application/json |
| JSON response | application/json |
| Document upload | multipart/form-data |
| AI streaming | text/event-stream |
| File download | Appropriate file media type |

---

# 2. Authentication and Authorization

## 2.1 Authentication Mechanism

The application shall use:

- JWT access tokens.
- Rotating refresh tokens.
- Secure HttpOnly refresh-token cookies.
- Password hashing.
- Token revocation.
- Refresh-token reuse detection.

## 2.2 Access Token Usage

Protected API requests shall include:

```http
Authorization: Bearer <access_token>
```

The access token shall contain only necessary identity and authorization context, such as:

- User identifier.
- Business identifier.
- Token identifier.
- Issued-at timestamp.
- Expiration timestamp.

The backend shall verify token validity and current account status.

Sensitive permission decisions shall not rely solely on stale role claims inside a token. The backend shall enforce current permissions.

## 2.3 Refresh Token

The refresh token shall be stored in a cookie configured with:

```text
HttpOnly
Secure (in production)
SameSite (appropriate deployment policy)
Path restricted to refresh/logout endpoints where practical
```

Cookie-based refresh requests shall implement CSRF protection.

## 2.4 Logout

Logout shall revoke the refresh-token session and clear the cookie.

## 2.5 Business Context

The MVP shall use one configured demo business.

The server shall determine the business context from trusted configuration and authenticated context.

Clients shall not submit arbitrary business IDs to choose which business's records they can access.

## 2.6 Role-Based Access Control

The backend shall enforce permissions on every protected endpoint.

| Role | General API Access |
|---|---|
| Customer | Own profile, conversations, orders, tickets and requests |
| Support Agent | Authorized assigned tickets, conversations and permitted customer context |
| Administrator | User, role, knowledge-base, product, order and administrative operations |
| Business Owner | Business oversight, configuration, authorized administration and analytics |

The exact permissions shall follow the role-permission matrix in `04_Database_Design.md`.

## 2.7 Ownership Rule

Customers shall only access their own resources.

If a customer requests another customer's order, ticket, refund or conversation, the API shall return:

```http
404 Not Found
```

This avoids revealing the existence of another customer's resource.

---

# 3. Standard API Response Format

## 3.1 Successful Response

Example:

```json
{
  "success": true,
  "message": "Request completed successfully",
  "data": {
    "id": "7f6d5a31-1d52-4f8b-8e5a-0a1a5b3a6f01"
  },
  "request_id": "req_123456"
}
```

The `data` object shall contain the endpoint-specific response.

## 3.2 Error Response

Example:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The provided input is invalid",
    "details": [
      {
        "field": "email",
        "message": "Enter a valid email address"
      }
    ]
  },
  "request_id": "req_123456"
}
```

Error responses shall not expose:

- SQL statements.
- Database stack traces.
- Internal file paths.
- Secret values.
- Raw internal provider errors.

## 3.3 Standard HTTP Status Codes

| Status | Meaning | Example |
|---|---|---|
| 200 | OK | Successful retrieval or update |
| 201 | Created | New ticket created |
| 202 | Accepted | Background job accepted |
| 204 | No Content | Successful deletion or logout |
| 400 | Bad Request | Invalid operation |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permission |
| 404 | Not Found | Resource missing or ownership concealed |
| 409 | Conflict | Duplicate or incompatible operation |
| 413 | Payload Too Large | Upload exceeds limit |
| 415 | Unsupported Media Type | Unsupported file type |
| 422 | Unprocessable Entity | Input validation failure |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected application error |
| 503 | Service Unavailable | Temporary dependency failure |

---

# 4. Pagination, Filtering and Sorting

## 4.1 Pagination

Collection endpoints shall use pagination.

Example:

```http
GET /api/v1/tickets?page=1&page_size=20
```

Parameters:

| Parameter | Type | Default | Description |
|---|---|---:|---|
| page | Integer | 1 | Page number |
| page_size | Integer | 20 | Records per page |
| sort_by | String | created_at | Sort field |
| sort_order | String | desc | asc or desc |

The backend shall enforce a maximum page size.

## 4.2 Paginated Response

```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total_items": 100,
      "total_pages": 5
    }
  },
  "request_id": "req_123456"
}
```

## 4.3 Filtering

Examples:

```http
GET /api/v1/tickets?status=OPEN
```

```http
GET /api/v1/orders?status=SHIPPED
```

Only explicitly supported filters shall be accepted.

---

# 5. Authentication APIs

Base path:

```text
/api/v1/auth
```

## 5.1 Register Customer

**Endpoint**

```http
POST /api/v1/auth/register
```

**Authentication:** Public

**Request**

```json
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "password": "StrongPassword123"
}
```

**Success: 201 Created**

```json
{
  "success": true,
  "message": "Registration successful",
  "data": {
    "user_id": "UUID",
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "role": "CUSTOMER"
  }
}
```

**Validation**

- Name is required.
- Email must be valid.
- Email must be unique within the business.
- Password must satisfy the configured password policy.
- Role shall be assigned by the backend, not accepted from the customer.

## 5.2 Login

**Endpoint**

```http
POST /api/v1/auth/login
```

**Authentication:** Public

**Request**

```json
{
  "email": "rahul@example.com",
  "password": "StrongPassword123"
}
```

**Success: 200 OK**

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "ACCESS_TOKEN",
    "token_type": "bearer",
    "expires_in": 900,
    "user": {
      "id": "UUID",
      "name": "Rahul Sharma",
      "email": "rahul@example.com",
      "role": "CUSTOMER"
    }
  }
}
```

The response shall also set the refresh-token cookie.

The example expiration value is illustrative and shall be configured.

## 5.3 Refresh Access Token

**Endpoint**

```http
POST /api/v1/auth/refresh
```

**Authentication:** Valid refresh cookie and CSRF protection as applicable.

**Request:** Refresh cookie is sent automatically by the browser.

**Success: 200 OK**

```json
{
  "success": true,
  "message": "Token refreshed",
  "data": {
    "access_token": "NEW_ACCESS_TOKEN",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

The backend shall rotate the refresh token and update the cookie.

If refresh-token reuse is detected, the affected token family shall be revoked according to the security policy.

## 5.4 Logout

**Endpoint**

```http
POST /api/v1/auth/logout
```

**Authentication:** Refresh session; CSRF protection as applicable.

**Success: 204 No Content**

The backend shall revoke the refresh session and clear the cookie.

## 5.5 Current User

**Endpoint**

```http
GET /api/v1/auth/me
```

**Authentication:** Required

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "id": "UUID",
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "roles": ["CUSTOMER"],
    "permissions": []
  }
}
```

## 5.6 Change Password

**Endpoint**

```http
POST /api/v1/auth/change-password
```

**Authentication:** Required

**Request**

```json
{
  "current_password": "OldPassword123",
  "new_password": "NewStrongPassword456"
}
```

**Success: 200 OK**

```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

The backend shall apply password policy checks and the configured session-revocation policy.

---

# 6. Customer APIs

Base path:

```text
/api/v1/customers
```

## 6.1 Get Own Profile

```http
GET /api/v1/customers/me
```

**Authentication:** Customer

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "id": "UUID",
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "phone": "9999999999"
  }
}
```

## 6.2 Update Own Profile

```http
PATCH /api/v1/customers/me
```

**Authentication:** Customer

**Request**

```json
{
  "name": "Rahul Kumar",
  "phone": "9999999999"
}
```

**Success: 200 OK**

```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": "UUID",
    "name": "Rahul Kumar",
    "phone": "9999999999"
  }
}
```

Only permitted fields shall be editable.

## 6.3 Request Account Deletion

```http
POST /api/v1/customers/me/deletion-requests
```

**Authentication:** Customer

**Request**

```json
{
  "reason": "I no longer need this account"
}
```

**Success: 201 Created**

```json
{
  "success": true,
  "message": "Account deletion request submitted",
  "data": {
    "request_id": "UUID",
    "status": "PENDING"
  }
}
```

The backend shall apply the configured password re-entry or other verification requirement for this sensitive account-security action.

## 6.4 View Account Deletion Request

```http
GET /api/v1/customers/me/deletion-requests
```

**Authentication:** Customer

Returns the customer's own deletion request history.

---

# 7. Product APIs

Base path:

```text
/api/v1/products
```

## 7.1 List Products

```http
GET /api/v1/products?page=1&page_size=20
```

**Authentication:** Customer or authorized staff

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "UUID",
        "name": "Wireless Headphones",
        "price": 1999.00,
        "availability": "IN_STOCK"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total_items": 1,
      "total_pages": 1
    }
  }
}
```

## 7.2 Get Product Details

```http
GET /api/v1/products/{product_id}
```

**Authentication:** Customer or authorized staff

**Success: 200 OK**

Returns verified product information.

## 7.3 Check Product Availability

```http
GET /api/v1/products/{product_id}/availability
```

**Authentication:** Customer or authorized staff

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "product_id": "UUID",
    "availability": "IN_STOCK",
    "available_quantity": 12
  }
}
```

Exact inventory fields returned to customers shall follow the business privacy policy.

## 7.4 Create Product

```http
POST /api/v1/products
```

**Authentication:** Administrator or authorized owner

**Request**

```json
{
  "name": "Wireless Headphones",
  "description": "Bluetooth headphones",
  "price": 1999.00,
  "stock_quantity": 12
}
```

**Success: 201 Created**

Returns the created product.

## 7.5 Update Product

```http
PATCH /api/v1/products/{product_id}
```

**Authentication:** Administrator or authorized owner

## 7.6 Delete or Deactivate Product

```http
DELETE /api/v1/products/{product_id}
```

**Authentication:** Administrator or authorized owner

The backend shall preserve historical order references. Where deletion would violate business-data integrity, the product shall be deactivated instead.

---

# 8. Order APIs

Base path:

```text
/api/v1/orders
```

## 8.1 List Own Orders

```http
GET /api/v1/orders/me?page=1&page_size=20
```

**Authentication:** Customer

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "UUID",
        "order_number": "ORD-10001",
        "order_status": "SHIPPED",
        "payment_status": "PAID",
        "order_date": "2026-11-10T10:00:00Z",
        "estimated_delivery": "2026-11-15"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total_items": 1,
      "total_pages": 1
    }
  }
}
```

## 8.2 Get Order Details

```http
GET /api/v1/orders/{order_id}
```

**Authentication:** Customer or authorized staff

The backend shall enforce ownership or staff permissions.

## 8.3 Get Order by Order Number

```http
GET /api/v1/orders/number/{order_number}
```

**Authentication:** Customer or authorized staff

The backend shall validate the authenticated customer's ownership.

## 8.4 Get Order Tracking

```http
GET /api/v1/orders/{order_id}/tracking
```

**Authentication:** Customer or authorized staff

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "order_number": "ORD-10001",
    "current_status": "SHIPPED",
    "estimated_delivery": "2026-11-15",
    "tracking_events": [
      {
        "status": "ORDER_PLACED",
        "description": "Order placed successfully",
        "occurred_at": "2026-11-10T10:00:00Z"
      },
      {
        "status": "SHIPPED",
        "description": "Order shipped",
        "occurred_at": "2026-11-12T08:30:00Z"
      }
    ]
  }
}
```

Only recorded tracking events shall be returned.

## 8.5 Administrative Order List

```http
GET /api/v1/admin/orders?page=1&page_size=20
```

**Authentication:** Administrator or authorized owner

Supports approved filters, sorting and pagination.

## 8.6 Update Order Information

```http
PATCH /api/v1/admin/orders/{order_id}
```

**Authentication:** Administrator or authorized owner

Only explicitly permitted order fields may be changed.

Every administrative change shall generate an audit record.

---

# 9. Refund APIs

Base path:

```text
/api/v1/refunds
```

## 9.1 Check Refund Eligibility

```http
POST /api/v1/refunds/eligibility
```

**Authentication:** Customer

**Request**

```json
{
  "order_id": "UUID",
  "order_item_ids": ["UUID"]
}
```

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "eligible": true,
    "reason": "Order satisfies the configured refund policy",
    "eligible_amount": 1999.00,
    "requires_human_approval": true
  }
}
```

The response is illustrative. Actual eligibility shall be calculated by backend policy logic.

If no active refund policy exists, the system shall not claim eligibility.

## 9.2 Create Refund Request

```http
POST /api/v1/refunds
```

**Authentication:** Customer

**Headers**

```http
Idempotency-Key: <unique-client-generated-key>
```

**Request**

```json
{
  "order_id": "UUID",
  "order_item_ids": ["UUID"],
  "reason": "Product damaged",
  "customer_confirmation": true
}
```

**Success: 201 Created**

```json
{
  "success": true,
  "message": "Refund request submitted for review",
  "data": {
    "refund_id": "UUID",
    "status": "PENDING_APPROVAL",
    "requires_human_approval": true
  }
}
```

The backend shall re-check eligibility during request creation. A previous eligibility response shall not be treated as permanent authorization.

## 9.3 List Own Refund Requests

```http
GET /api/v1/refunds/me?page=1&page_size=20
```

**Authentication:** Customer

## 9.4 Get Refund Details

```http
GET /api/v1/refunds/{refund_id}
```

**Authentication:** Customer or authorized staff

Ownership and permissions shall be checked.

## 9.5 Review Refund Request

```http
POST /api/v1/admin/refunds/{refund_id}/review
```

**Authentication:** Authorized administrator or support role with refund-review permission

**Request**

```json
{
  "decision": "APPROVE",
  "review_note": "Verified according to the refund policy"
}
```

**Success: 200 OK**

```json
{
  "success": true,
  "message": "Refund request reviewed",
  "data": {
    "refund_id": "UUID",
    "status": "APPROVED"
  }
}
```

The system shall prevent the same authorized user from making conflicting or duplicate final decisions.

Actual payment refund execution is outside the MVP.

## 9.6 Refund Policy Administration

```http
GET /api/v1/admin/refund-policies
```

```http
POST /api/v1/admin/refund-policies
```

```http
PATCH /api/v1/admin/refund-policies/{policy_id}
```

**Authentication:** Administrator or authorized owner

Policies shall be versioned and audited.

---

# 10. Cancellation APIs

Base path:

```text
/api/v1/cancellations
```

## 10.1 Check Cancellation Eligibility

```http
POST /api/v1/cancellations/eligibility
```

**Authentication:** Customer

**Request**

```json
{
  "order_id": "UUID"
}
```

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "eligible_for_review": true,
    "reason": "Order can be submitted for cancellation review"
  }
}
```

This does not guarantee cancellation approval.

## 10.2 Submit Cancellation Request

```http
POST /api/v1/cancellations
```

**Authentication:** Customer

**Headers**

```http
Idempotency-Key: <unique-client-generated-key>
```

**Request**

```json
{
  "order_id": "UUID",
  "reason": "Ordered by mistake",
  "customer_confirmation": true
}
```

**Success: 201 Created**

```json
{
  "success": true,
  "message": "Cancellation request submitted",
  "data": {
    "request_id": "UUID",
    "status": "PENDING_REVIEW"
  }
}
```

The backend shall re-check cancellation conditions when creating the request.

## 10.3 List Own Cancellation Requests

```http
GET /api/v1/cancellations/me
```

**Authentication:** Customer

## 10.4 Review Cancellation Request

```http
POST /api/v1/admin/cancellations/{request_id}/review
```

**Authentication:** Authorized staff

**Request**

```json
{
  "decision": "APPROVE",
  "review_note": "Approved after order verification"
}
```

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "request_id": "UUID",
    "status": "APPROVED"
  }
}
```

Approval and actual cancellation execution shall be separate operations governed by business policy.

No AI endpoint shall automatically execute cancellation.

---

# 11. Conversation APIs

Base path:

```text
/api/v1/conversations
```

## 11.1 Create Conversation

```http
POST /api/v1/conversations
```

**Authentication:** Customer

**Request**

```json
{
  "subject": "Order delivery issue"
}
```

**Success: 201 Created**

```json
{
  "success": true,
  "data": {
    "conversation_id": "UUID",
    "status": "ACTIVE"
  }
}
```

The backend shall attach the authenticated customer as a conversation participant.

## 11.2 List Own Conversations

```http
GET /api/v1/conversations/me?page=1&page_size=20
```

**Authentication:** Customer

## 11.3 Get Conversation

```http
GET /api/v1/conversations/{conversation_id}
```

**Authentication:** Authorized conversation participant or staff

## 11.4 Get Conversation Messages

```http
GET /api/v1/conversations/{conversation_id}/messages?page=1&page_size=50
```

**Authentication:** Authorized conversation participant or staff

Internal staff notes shall not be returned through customer-facing message endpoints.

## 11.5 Submit Message Feedback

```http
POST /api/v1/conversations/{conversation_id}/messages/{message_id}/feedback
```

**Authentication:** Customer or authorized participant

**Request**

```json
{
  "rating": 5,
  "feedback": "The answer was helpful"
}
```

**Success: 201 Created**

```json
{
  "success": true,
  "message": "Feedback submitted"
}
```

The backend shall verify that the message belongs to the conversation and that the requester is authorized to submit feedback.

---

# 12. AI Chat APIs

Base path:

```text
/api/v1/chat
```

## 12.1 Send Chat Message — Non-Streaming

```http
POST /api/v1/chat/message
```

**Authentication:** Customer

**Request**

```json
{
  "conversation_id": "UUID",
  "message": "Where is my order ORD-10001?"
}
```

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "conversation_id": "UUID",
    "user_message_id": "UUID",
    "assistant_message_id": "UUID",
    "response": "Your order has been shipped.",
    "intent": "ORDER_TRACKING",
    "sources": [],
    "requires_human_support": false
  }
}
```

The backend shall:

1. Authenticate the customer.
2. Verify conversation access.
3. Save the incoming message.
4. Load permitted conversation context.
5. Classify intent.
6. Retrieve information or invoke approved tools.
7. Validate tool output.
8. Generate the response.
9. Save the assistant response.
10. Return the response.

## 12.2 Streaming Chat

```http
POST /api/v1/chat/stream
```

**Authentication:** Customer

**Content-Type:** application/json

**Accept:** text/event-stream

**Request**

```json
{
  "conversation_id": "UUID",
  "message": "Explain your return policy"
}
```

The endpoint shall stream Server-Sent Events (SSE).

Example:

```text
event: message_start
data: {"conversation_id":"UUID"}

event: token
data: {"content":"Our"}

event: token
data: {"content":" return"}

event: token
data: {"content":" policy"}

event: message_complete
data: {"message_id":"UUID"}

event: done
data: {}
```

For an error:

```text
event: error
data: {"code":"AI_PROVIDER_UNAVAILABLE","message":"The assistant is temporarily unavailable"}
```

The server shall save the message and final response according to the conversation persistence rules.

The client shall support interrupted streams and appropriate retry behavior without creating duplicate business operations.

## 12.3 Chat Limitations

- The LLM shall not directly query the database.
- Tool calls shall be restricted to approved backend functions.
- Customer identity shall come from authenticated context.
- Sensitive operations shall require explicit confirmation.
- Refund processing shall require human approval.
- Cancellation execution shall require human review.
- Unsupported facts shall not be fabricated.

---

# 13. Support Ticket APIs

Base path:

```text
/api/v1/tickets
```

## 13.1 Create Ticket

```http
POST /api/v1/tickets
```

**Authentication:** Customer or authorized staff

**Request**

```json
{
  "conversation_id": "UUID",
  "subject": "Delivery issue",
  "description": "My order has not arrived",
  "category": "DELIVERY",
  "priority": "MEDIUM"
}
```

**Success: 201 Created**

```json
{
  "success": true,
  "data": {
    "ticket_id": "UUID",
    "ticket_number": "TKT-10001",
    "status": "OPEN",
    "priority": "MEDIUM"
  }
}
```

The backend shall verify conversation ownership or staff authorization.

## 13.2 List Own Tickets

```http
GET /api/v1/tickets/me?page=1&page_size=20
```

**Authentication:** Customer

## 13.3 Get Ticket Details

```http
GET /api/v1/tickets/{ticket_id}
```

**Authentication:** Ticket owner or authorized staff

## 13.4 Update Ticket Status

```http
PATCH /api/v1/tickets/{ticket_id}/status
```

**Authentication:** Authorized support staff

**Request**

```json
{
  "status": "IN_PROGRESS"
}
```

The backend shall validate permitted status transitions.

## 13.5 Assign Ticket

```http
POST /api/v1/tickets/{ticket_id}/assign
```

**Authentication:** Authorized support manager or administrator

**Request**

```json
{
  "assignee_id": "UUID"
}
```

## 13.6 Add Internal Note

```http
POST /api/v1/tickets/{ticket_id}/notes
```

**Authentication:** Authorized support staff

**Request**

```json
{
  "note": "Customer contacted the shipping provider"
}
```

**Success: 201 Created**

```json
{
  "success": true,
  "message": "Internal note added"
}
```

Internal notes shall never appear in customer-facing conversation responses.

## 13.7 Ticket Activity

```http
GET /api/v1/tickets/{ticket_id}/activities
```

**Authentication:** Authorized staff or ticket owner, with customer-safe filtering

## 13.8 Reopen Ticket

```http
POST /api/v1/tickets/{ticket_id}/reopen
```

**Authentication:** Ticket owner or authorized staff

The backend shall validate reopening rules.

## 13.9 Escalate Ticket

```http
POST /api/v1/tickets/{ticket_id}/escalate
```

**Authentication:** Authorized customer or staff workflow

The backend shall record the escalation event and preserve conversation context.

---

# 14. Knowledge Base APIs

Base path:

```text
/api/v1/knowledge-base
```

## 14.1 Upload Document

```http
POST /api/v1/knowledge-base/documents
```

**Authentication:** Support Agent, Administrator or Owner

**Content-Type:** multipart/form-data

**Form fields**

```text
file: policy.pdf
title: Return Policy
description: Company return policy
```

**Success: 202 Accepted**

```json
{
  "success": true,
  "message": "Document accepted for processing",
  "data": {
    "document_id": "UUID",
    "job_id": "UUID",
    "status": "PROCESSING"
  }
}
```

The API shall validate:

- File extension.
- File content type.
- File size.
- File content.
- User permission.

The upload endpoint shall not trust the filename extension alone.

## 14.2 Add Website URL

```http
POST /api/v1/knowledge-base/websites
```

**Authentication:** Support Agent, Administrator or Owner

**Request**

```json
{
  "url": "https://example.com/return-policy",
  "title": "Return Policy"
}
```

**Success: 202 Accepted**

```json
{
  "success": true,
  "data": {
    "document_id": "UUID",
    "job_id": "UUID",
    "status": "PROCESSING"
  }
}
```

The backend shall validate URL safety and apply approved crawling restrictions.

## 14.3 List Documents

```http
GET /api/v1/knowledge-base/documents?page=1&page_size=20
```

**Authentication:** Authorized staff

## 14.4 Get Document Details

```http
GET /api/v1/knowledge-base/documents/{document_id}
```

**Authentication:** Authorized staff

## 14.5 Replace Document

```http
PUT /api/v1/knowledge-base/documents/{document_id}
```

**Authentication:** Administrator or Owner

**Content-Type:** multipart/form-data

The replacement shall trigger a background ingestion workflow.

Old indexed content shall be deactivated safely after successful replacement according to the indexing strategy.

## 14.6 Delete Document

```http
DELETE /api/v1/knowledge-base/documents/{document_id}
```

**Authentication:** Administrator or Owner

The backend shall prevent deleted or inactive content from appearing in future retrieval.

## 14.7 Search Knowledge Base

```http
POST /api/v1/knowledge-base/search
```

**Authentication:** Authorized staff or approved internal service context

**Request**

```json
{
  "query": "What is the return policy?",
  "top_k": 5
}
```

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "results": [
      {
        "document_id": "UUID",
        "document_title": "Return Policy",
        "chunk_id": "UUID",
        "content": "Customers may return eligible products...",
        "page_number": 2,
        "score": 0.87
      }
    ]
  }
}
```

The search result shall be filtered by business context and document access rules.

---

# 15. Background Job APIs

Base path:

```text
/api/v1/jobs
```

## 15.1 Get Job Status

```http
GET /api/v1/jobs/{job_id}
```

**Authentication:** Authorized user who initiated the job or authorized administrator

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "job_id": "UUID",
    "job_type": "DOCUMENT_INGESTION",
    "status": "PROCESSING",
    "attempt_count": 1,
    "created_at": "2026-11-13T10:00:00Z"
  }
}
```

## 15.2 Retry Failed Job

```http
POST /api/v1/admin/jobs/{job_id}/retry
```

**Authentication:** Administrator or authorized owner

The backend shall only retry eligible failed jobs and shall prevent unsafe duplicate processing.

---

# 16. Notification APIs

Base path:

```text
/api/v1/notifications
```

## 16.1 List Notifications

```http
GET /api/v1/notifications?page=1&page_size=20
```

**Authentication:** Authenticated user

The backend shall return only notifications belonging to the authenticated user.

## 16.2 Mark Notification as Read

```http
PATCH /api/v1/notifications/{notification_id}/read
```

**Authentication:** Notification owner

## 16.3 Mark All Notifications as Read

```http
POST /api/v1/notifications/read-all
```

**Authentication:** Authenticated user

---

# 17. Administration APIs

Base path:

```text
/api/v1/admin
```

All endpoints in this section require the relevant administrative permission.

## 17.1 List Users

```http
GET /api/v1/admin/users?page=1&page_size=20
```

## 17.2 Get User

```http
GET /api/v1/admin/users/{user_id}
```

## 17.3 Update User

```http
PATCH /api/v1/admin/users/{user_id}
```

Permitted updates shall include only approved account fields.

## 17.4 Deactivate User

```http
POST /api/v1/admin/users/{user_id}/deactivate
```

## 17.5 Activate User

```http
POST /api/v1/admin/users/{user_id}/activate
```

## 17.6 List Roles

```http
GET /api/v1/admin/roles
```

## 17.7 Update Role Permissions

```http
PUT /api/v1/admin/roles/{role_id}/permissions
```

**Request**

```json
{
  "permission_ids": [
    "UUID",
    "UUID"
  ]
}
```

The backend shall prevent privilege escalation and unauthorized modification of protected roles.

## 17.8 Audit Logs

```http
GET /api/v1/admin/audit-logs?page=1&page_size=50
```

Supports approved filters such as:

- Actor.
- Action.
- Target type.
- Date range.
- Outcome.

Audit logs shall be read-only through ordinary administrative APIs.

## 17.9 AI Configuration

```http
GET /api/v1/admin/ai-config
```

```http
PATCH /api/v1/admin/ai-config
```

**Authentication:** Authorized administrator or owner

Only non-secret configuration values shall be returned.

API keys shall never be exposed in responses.

---

# 18. Analytics APIs

Base path:

```text
/api/v1/analytics
```

## 18.1 Dashboard Overview

```http
GET /api/v1/analytics/overview
```

**Authentication:** Business Owner or authorized administrator

**Success: 200 OK**

```json
{
  "success": true,
  "data": {
    "total_tickets": 250,
    "open_tickets": 35,
    "resolved_tickets": 180,
    "escalated_tickets": 20,
    "ai_handled_conversations": 150,
    "human_handled_conversations": 100
  }
}
```

These values are illustrative.

## 18.2 Ticket Statistics

```http
GET /api/v1/analytics/tickets?from=2026-11-01&to=2026-11-13
```

## 18.3 Resolution Metrics

```http
GET /api/v1/analytics/resolution
```

## 18.4 Common Query Categories

```http
GET /api/v1/analytics/query-categories
```

Analytics responses shall be scoped to the authorized business.

---

# 19. API Security Requirements

## 19.1 Input Validation

All request bodies, query parameters, path parameters and uploaded files shall be validated.

Pydantic schemas shall be used for backend request validation.

## 19.2 SQL Injection Prevention

The application shall use SQLAlchemy parameterized operations or safely parameterized SQL.

User input shall never be concatenated directly into SQL statements.

## 19.3 Cross-Site Request Forgery

Cookie-authenticated state-changing requests shall use CSRF protection.

## 19.4 Cross-Origin Resource Sharing

CORS shall allow only configured frontend origins.

Wildcard origins shall not be used with credentialed requests.

## 19.5 File Upload Security

The system shall:

- Limit upload size.
- Validate actual content.
- Restrict supported formats.
- Generate safe storage names.
- Prevent path traversal.
- Store uploaded files outside publicly executable locations.
- Restrict URL ingestion to safe destinations.

## 19.6 Rate Limiting

Rate limits shall apply to:

- Login.
- Registration.
- Password changes.
- Chat.
- File uploads.
- Sensitive operations.

## 19.7 Idempotency

Refund and cancellation request creation shall support an `Idempotency-Key`.

The backend shall ensure that repeated submissions with the same key and equivalent request do not create duplicate operations.

The key shall be scoped to the authenticated user and operation.

A repeated key with a different request payload shall be rejected with a conflict response.

## 19.8 AI Tool Security

AI tools shall:

- Use backend-authenticated identity.
- Validate all inputs.
- Check permissions.
- Check business rules.
- Avoid arbitrary database access.
- Return structured results.
- Record sensitive operations.

---

# 20. API Error Codes

The following application error codes shall be used consistently.

| Error Code | Meaning |
|---|---|
| INVALID_CREDENTIALS | Incorrect login credentials |
| AUTHENTICATION_REQUIRED | Valid authentication is missing |
| TOKEN_EXPIRED | Access token has expired |
| TOKEN_REVOKED | Token has been revoked |
| PERMISSION_DENIED | Required permission is missing |
| RESOURCE_NOT_FOUND | Resource does not exist or access is concealed |
| VALIDATION_ERROR | Request validation failed |
| DUPLICATE_RESOURCE | Duplicate resource |
| IDEMPOTENCY_CONFLICT | Same key used with different payload |
| REFUND_NOT_ELIGIBLE | Refund policy conditions not satisfied |
| REFUND_REQUIRES_APPROVAL | Human approval required |
| CANCELLATION_NOT_ELIGIBLE | Cancellation conditions not satisfied |
| DOCUMENT_PROCESSING_FAILED | Document ingestion failed |
| UNSUPPORTED_FILE_TYPE | File format not supported |
| FILE_TOO_LARGE | Upload exceeds configured limit |
| AI_PROVIDER_UNAVAILABLE | AI provider unavailable |
| AI_INSUFFICIENT_CONTEXT | Evidence is insufficient |
| RATE_LIMIT_EXCEEDED | Request limit exceeded |
| INTERNAL_SERVER_ERROR | Unexpected server error |

The API shall map each code to an appropriate HTTP status.

---

# 21. Postman Testing Strategy

Postman shall be used to validate the API before frontend integration.

## 21.1 Environment Variables

Create a Postman environment named:

`Ecommerce-AI-Local`

Configure:

| Variable | Example |
|---|---|
| base_url | http://localhost:8000/api/v1 |
| access_token | Empty initially |
| customer_id | Empty initially |
| conversation_id | Empty initially |
| order_id | Empty initially |
| refund_id | Empty initially |
| ticket_id | Empty initially |
| job_id | Empty initially |

Sensitive token values shall not be committed to a shared public collection.

## 21.2 Recommended Collection Structure

```text
Ecommerce AI Support API
│
├── 01 Authentication
│   ├── Register
│   ├── Login
│   ├── Get Current User
│   ├── Refresh Token
│   └── Logout
│
├── 02 Customer
│   ├── Get Profile
│   ├── Update Profile
│   └── Account Deletion Request
│
├── 03 Products
│   ├── List Products
│   ├── Get Product
│   └── Check Availability
│
├── 04 Orders
│   ├── List Own Orders
│   ├── Get Order
│   └── Get Tracking
│
├── 05 Refunds
│   ├── Check Eligibility
│   ├── Create Request
│   ├── Get Refund
│   └── Review Refund
│
├── 06 Cancellations
│   ├── Check Eligibility
│   ├── Create Request
│   └── Review Request
│
├── 07 Conversations and Chat
│   ├── Create Conversation
│   ├── List Conversations
│   ├── Send Message
│   ├── Stream Message
│   └── Submit Feedback
│
├── 08 Tickets
│   ├── Create Ticket
│   ├── List Tickets
│   ├── Update Status
│   ├── Assign Ticket
│   └── Add Internal Note
│
├── 09 Knowledge Base
│   ├── Upload Document
│   ├── Add Website
│   ├── List Documents
│   ├── Replace Document
│   └── Delete Document
│
├── 10 Background Jobs
│   ├── Get Job Status
│   └── Retry Failed Job
│
├── 11 Notifications
│   ├── List Notifications
│   └── Mark as Read
│
└── 12 Administration and Analytics
    ├── Manage Users
    ├── Manage Roles
    ├── Audit Logs
    └── Analytics Overview
```

## 21.3 Authentication Test

Test sequence:

1. Register a customer.
2. Log in.
3. Capture the access token.
4. Call `/auth/me`.
5. Verify the returned identity.
6. Refresh the access token.
7. Verify refresh-token rotation.
8. Log out.
9. Attempt to use the revoked refresh session.

Expected result: each operation follows its defined authentication behavior.

## 21.4 Authorization Test

Create two customers:

- Customer A.
- Customer B.

Test:

1. Authenticate as Customer A.
2. Retrieve Customer A's order.
3. Confirm successful access.
4. Attempt to retrieve Customer B's order.
5. Confirm `404 Not Found`.
6. Repeat for tickets, refunds and conversations.

Expected result: Customer A cannot access Customer B's protected records.

## 21.5 Refund Test

Test:

1. Submit an eligibility request for an eligible order.
2. Submit an eligibility request for an ineligible order.
3. Submit an eligibility request when no active policy exists.
4. Create a confirmed refund request.
5. Repeat the same request with the same idempotency key.
6. Verify duplicate prevention.
7. Review the refund using an authorized staff account.
8. Attempt review using an unauthorized customer account.

Expected result: backend policy enforcement and human approval work correctly.

## 21.6 Cancellation Test

Test:

1. Check cancellation eligibility.
2. Create a confirmed cancellation request.
3. Verify pending-review status.
4. Attempt duplicate submission.
5. Review the request as authorized staff.
6. Attempt review as an unauthorized user.

Expected result: no cancellation is executed automatically by the AI.

## 21.7 RAG Test

Test:

1. Upload a PDF.
2. Receive the document ID and job ID.
3. Check job status.
4. Wait for successful indexing.
5. Search the knowledge base.
6. Verify source metadata.
7. Ask a related question through chat.
8. Verify that the response is grounded in retrieved content.
9. Replace the document.
10. Verify obsolete chunks are no longer searchable.

## 21.8 Ticket Test

Test:

1. Create a ticket.
2. Retrieve ticket details.
3. Assign it to a support agent.
4. Add an internal note.
5. Verify the note is visible to authorized staff.
6. Verify the note is not visible to the customer.
7. Update ticket status.
8. Reopen the ticket according to configured rules.

## 21.9 Background Job Test

Test:

1. Submit a document ingestion job.
2. Retrieve its status.
3. Simulate a processing failure.
4. Verify failure status.
5. Retry an eligible job.
6. Verify completion.
7. Verify that the job is not processed concurrently by multiple workers.

---

# 22. API Testing Checklist

| Test | Expected Result |
|---|---|
| Valid customer registration | 201 |
| Duplicate email registration | 409 |
| Invalid login | 401 |
| Valid login | 200 |
| Missing access token | 401 |
| Expired access token | 401 |
| Customer accesses own order | 200 |
| Customer accesses another customer's order | 404 |
| Unauthorized admin endpoint | 403 or 404 according to resource-disclosure policy |
| Invalid request body | 422 |
| Unsupported file upload | 415 |
| Oversized file | 413 |
| Eligible refund request | Created after confirmation |
| Ineligible refund request | Rejected |
| Refund without active policy | Fails safely |
| Duplicate refund submission | No duplicate request |
| Cancellation request | Pending review |
| AI unsupported question | Clarification or escalation |
| Knowledge-base upload | Background job created |
| Document ingestion failure | Failure recorded |
| Unauthorized document deletion | 403 |
| Internal note viewed by customer | Not returned |
| Logout followed by refresh | Rejected |
| Rate limit exceeded | 429 |

---

# 23. API Documentation and OpenAPI

FastAPI shall generate OpenAPI documentation.

Development documentation shall be available at:

```text
http://localhost:8000/docs
```

Alternative documentation:

```text
http://localhost:8000/redoc
```

The API documentation shall include:

- Endpoint descriptions.
- Request schemas.
- Response schemas.
- Authentication requirements.
- Error responses.
- Example payloads.

OpenAPI documentation shall be updated whenever API contracts change.

---

# 24. Implementation Notes

1. Endpoint definitions are logical contracts; implementation must follow the final database schema and approved permission matrix.
2. Exact Pydantic schemas shall be defined during backend development.
3. API endpoints shall be tested individually before frontend integration.
4. Sensitive business operations shall use explicit database transaction boundaries.
5. Idempotency shall be implemented before enabling refund and cancellation request creation.
6. Customer-facing endpoints shall not expose internal notes or restricted staff information.
7. Streaming responses shall handle client disconnection and provider errors.
8. File ingestion shall be asynchronous and tracked through persistent jobs.
9. The API shall not expose real payment-processing functionality in the MVP.
10. Every API shall be included in automated tests.

---

# 25. Dependencies on Other Documents

| Document | Filename | Dependency |
|---|---|---|
| Business Requirements | 01_BRD.md | Business rules and scope |
| Software Requirements | 02_SRS.md | Functional requirements |
| Technical Architecture | 03_Technical_Architecture.md | Component responsibilities |
| Database Design | 04_Database_Design.md | Tables, constraints and relationships |
| API Specification | 05_API_Specification.md | API contracts |
| Project Folder Structure | 06_Project_Folder_Structure.md | Router and module organization |
| Development Roadmap | 07_Development_Roadmap.md | Implementation sequence |
| Testing Strategy | 08_Testing_Strategy.md | Detailed automated testing |

---

# 26. Approval Status

**Document:** 05_API_Specification.md  
**Version:** 1.1  
**Status:** Revised Draft — Pending Cross-Document Consistency Review and User Approval

This document defines the proposed API contracts. Endpoint implementation shall begin only after all eight project documents have been revised, cross-checked and approved.