# 02 — Software Requirements Specification (SRS)

**Project:** AI-Powered E-commerce Customer Support Agent  
**Document:** Software Requirements Specification  
**Version:** 1.1  
**Status:** Revised Draft — Pending Cross-Document Consistency Review and User Approval  
**Architecture:** Python, FastAPI, LangChain, OpenAI, PostgreSQL, pgvector, React, TypeScript

---

# 1. Introduction

## 1.1 Purpose

This document defines the functional and non-functional requirements of the AI-Powered E-commerce Customer Support Agent.

It specifies how customers, support agents, administrators, and business owners interact with the system and how the system processes customer queries, retrieves knowledge, accesses business data, and manages support workflows.

This document serves as the technical reference for backend development, frontend development, database implementation, integration, and testing.

## 1.2 Scope

The system will provide:

- AI-powered customer conversations.
- Knowledge-base question answering using Retrieval-Augmented Generation (RAG).
- Order tracking and product availability.
- Refund eligibility checks and refund requests.
- Order cancellation requests.
- Support ticket creation and management.
- Human escalation.
- Customer and conversation history.
- Role-based access control.
- Knowledge-base administration.
- Notifications and audit logging.
- Administrative dashboards.

## 1.3 Intended Audience

- Project developer.
- Backend developer.
- Frontend developer.
- Database designer.
- QA and testing engineer.
- Project evaluator.

## 1.4 Definitions

| Term | Meaning |
|---|---|
| AI Agent | Application component that interprets customer requests and coordinates responses and tools |
| LLM | Large Language Model |
| RAG | Retrieval-Augmented Generation |
| Embedding | Numerical representation of text used for semantic search |
| Vector Search | Searching for semantically similar content |
| RBAC | Role-Based Access Control |
| JWT | JSON Web Token |
| API | Application Programming Interface |
| P95 | Response-time threshold below which 95% of requests should complete |
| CSRF | Cross-Site Request Forgery |
| Idempotency | Ensuring repeated requests do not accidentally execute an operation multiple times |
| MVP | Minimum Viable Product |

---

# 2. Overall System Description

## 2.1 Product Perspective

The application will use a modular full-stack architecture.

**Backend**
- Python
- FastAPI
- LangChain
- OpenAI API
- SQLAlchemy
- Alembic

**Database**
- PostgreSQL
- pgvector

**Frontend**
- React
- TypeScript
- Tailwind CSS

**Communication**
- REST APIs
- WebSockets for real-time chat and updates
- Polling fallback where WebSockets are unavailable

**Deployment**
- Docker-based development and deployment.

## 2.2 User Classes

| User | Description | Main Responsibilities |
|---|---|---|
| Customer | End user of the e-commerce platform | Ask questions, track orders, request refunds, create tickets |
| Support Agent | Customer support employee | Manage assigned tickets, respond to customers, add internal notes, upload knowledge documents |
| Administrator | System administrator | Manage users, roles, permissions, documents, products, orders and configuration |
| Business Owner | Business-level authority | Oversee support operations, manage business settings, monitor analytics and audit activity |

## 2.3 Operating Environment

The application should support:

- Modern desktop browsers.
- Modern mobile browsers.
- Windows, Linux and macOS development environments.
- Docker-based local services.
- Python backend environment.
- PostgreSQL database environment.

## 2.4 Design Constraints

1. The backend is the authority for all business data.
2. The LLM must not independently approve refunds or cancellations.
3. The system must not reveal one customer's information to another customer.
4. Every sensitive operation must pass backend authorization.
5. AI responses must be grounded in retrieved knowledge or verified business data.
6. External API credentials must be stored securely.
7. The MVP will support one demo business, but the database must be tenant-aware.
8. LangGraph is reserved for an advanced development phase; the MVP uses controlled orchestration with LangChain.

---

# 3. Functional Requirements

Requirements are classified as:

- **Must (P0):** Required for MVP acceptance.
- **Should (P1):** Important enhancement for the advanced phase.
- **Could (P2):** Optional or future capability.

## 3.1 Authentication and Account Management

### FR-AUTH-01 — User Registration

**Priority:** Must (P0)

The system shall allow customers to register using:

- Name.
- Email address.
- Password.
- Required profile information.

The system shall validate input and securely hash passwords before storing them.

Email uniqueness shall be enforced within the business context.

### FR-AUTH-02 — User Login

**Priority:** Must (P0)

The system shall authenticate users using email and password.

After successful authentication, the system shall issue an access token and establish a secure refresh-token mechanism.

### FR-AUTH-03 — Token Management

**Priority:** Must (P0)

The system shall:

- Use short-lived access tokens.
- Store refresh tokens in Secure, HttpOnly cookies.
- Rotate refresh tokens when used.
- Revoke tokens during logout.
- Detect refresh-token reuse.
- Protect cookie-based refresh operations against CSRF.

### FR-AUTH-04 — Password Security

**Priority:** Must (P0)

The system shall:

- Hash passwords using a suitable password-hashing algorithm.
- Never store plaintext passwords.
- Validate password strength.
- Support password changes.
- Require password re-entry for designated sensitive account-security operations.

### FR-AUTH-05 — Role-Based Access Control

**Priority:** Must (P0)

The system shall implement RBAC using roles and explicit permissions.

The backend shall enforce permissions for every protected operation.

Hiding a frontend button or navigation item shall not be considered authorization.

### FR-AUTH-06 — Customer Data Ownership

**Priority:** Must (P0)

Customers shall only access their own:

- Profile.
- Orders.
- Order tracking details.
- Refund requests.
- Support tickets.
- Conversations.
- Personal information.

Requests for another customer's protected resource shall return `404 Not Found` to avoid disclosing whether that resource exists.

### FR-AUTH-07 — Business Context

**Priority:** Must (P0)

The MVP shall operate with one configured demo business.

The business context shall be resolved by the server and shall not be accepted as an arbitrary client-controlled business identifier.

Email uniqueness and resource ownership shall be scoped to the business.

### FR-AUTH-08 — Account Deletion Requests

**Priority:** Must (P0)

Customers shall be able to submit account deletion requests.

The system shall:

- Record the request.
- Track its status.
- Apply the configured retention and deletion policy.
- Preserve records that must legally or operationally be retained.
- Record administrative processing through audit logs.

---

## 3.2 Customer Profile Management

### FR-CUST-01 — View Profile

**Priority:** Must (P0)

Customers shall be able to view their profile information.

### FR-CUST-02 — Update Profile

**Priority:** Must (P0)

Customers shall be able to update permitted profile fields.

The backend shall validate all submitted values.

### FR-CUST-03 — Customer Context

**Priority:** Must (P0)

The system shall retrieve authorized customer context to support relevant conversations.

The AI agent shall not be permitted to access arbitrary customer records.

---

## 3.3 AI Customer Support

### FR-AI-01 — Customer Query Processing

**Priority:** Must (P0)

The system shall accept customer messages through the chat interface.

The AI processing pipeline shall:

1. Receive the message.
2. Validate the authenticated session.
3. Identify the request intent.
4. Determine whether knowledge retrieval or a business tool is required.
5. Retrieve relevant context.
6. Generate a response.
7. Save the conversation and response.
8. Return the response to the customer.

### FR-AI-02 — Basic Intent Classification

**Priority:** Must (P0)

The system shall classify common customer queries into categories such as:

- Order tracking.
- Refund inquiry.
- Cancellation inquiry.
- Product information.
- Shipping information.
- Return policy.
- Payment inquiry.
- General FAQ.
- Complaint.
- Human support request.

If intent is unclear, the agent shall ask a clarification question.

### FR-AI-03 — Controlled Tool Execution

**Priority:** Must (P0)

The agent shall use approved backend tools to perform supported business operations.

Tools shall include:

- Order lookup.
- Product availability lookup.
- Customer information retrieval.
- Refund eligibility check.
- Refund request creation.
- Cancellation request creation.
- Support ticket creation.
- Knowledge-base retrieval.
- Complaint classification.
- Customer information update, where permitted.
- Notification simulation.
- Human escalation.

The LLM shall not directly execute database queries or bypass backend authorization.

### FR-AI-04 — Authenticated Context for Tools

**Priority:** Must (P0)

Customer identity and authorization context shall be derived from the authenticated backend session.

The system shall never trust a customer ID supplied only by the LLM or by an untrusted message.

### FR-AI-05 — Confidence and Insufficient Information

**Priority:** Must (P0)

The system shall apply basic response-quality checks.

When sufficient information is unavailable, the agent shall:

- Ask for clarification.
- Retrieve additional relevant information.
- Explain that it cannot verify the answer.
- Offer escalation to human support.

The system shall not fabricate business information.

### FR-AI-06 — Conversation History

**Priority:** Must (P0)

The system shall save:

- Customer messages.
- AI responses.
- Staff messages.
- Message timestamps.
- Conversation status.
- Relevant tool execution references.
- Message feedback.

The conversation model shall support multiple participants, including customers and staff.

### FR-AI-07 — Conversation Memory

**Priority:** Must (P0)

The system shall maintain session-level conversation context.

The system shall support basic conversation summaries and authorized customer context retrieval.

Historical context shall only be accessed when permitted by the authenticated user's permissions and resource ownership.

Advanced long-term memory optimization is reserved for a later phase.

### FR-AI-08 — Streaming Responses

**Priority:** Must (P0)

The system shall support incremental AI response delivery.

The frontend shall display partial responses as they become available.

If streaming is unavailable, the system shall provide a non-streaming fallback.

### FR-AI-09 — Multilingual Responses

**Priority:** Should (P1)

The advanced phase should support English and Hindi.

The MVP shall prioritize English.

### FR-AI-10 — Advanced Sentiment and Urgency

**Priority:** Should (P1)

The advanced phase should identify:

- Positive sentiment.
- Neutral sentiment.
- Negative sentiment.
- Urgent complaints.
- Potentially dissatisfied customers.

These signals may be used for ticket prioritization.

### FR-AI-11 — LangGraph Orchestration

**Priority:** Should (P1)

The advanced phase may introduce LangGraph for more complex stateful agent workflows.

LangGraph is not a prerequisite for MVP completion.

---

## 3.4 Knowledge Base and RAG

### FR-RAG-01 — Document Upload

**Priority:** Must (P0)

Authorized staff shall be able to upload knowledge-base documents.

Supported formats:

- PDF.
- TXT.
- DOCX.
- CSV.
- XLSX.

### FR-RAG-02 — Website Ingestion

**Priority:** Must (P0)

Authorized staff shall be able to add website URLs.

The ingestion process shall:

- Validate URLs.
- Restrict crawling to approved domains.
- Apply configured crawling limits.
- Extract useful textual content.
- Record the source URL.

### FR-RAG-03 — Document Processing

**Priority:** Must (P0)

Uploaded documents shall pass through the following pipeline:

1. File validation.
2. Text extraction.
3. Text cleaning.
4. Chunking.
5. Embedding generation.
6. Storage of document metadata.
7. Storage of chunks and embeddings.
8. Indexing for retrieval.

### FR-RAG-04 — Hybrid Retrieval

**Priority:** Must (P0)

The system shall use:

- PostgreSQL full-text search.
- pgvector semantic search.
- A configured fusion strategy, initially Reciprocal Rank Fusion (RRF).

The system shall initially use exact vector search.

Index optimization such as HNSW may be evaluated later.

### FR-RAG-05 — Grounded Responses

**Priority:** Must (P0)

The AI shall generate knowledge-base answers using retrieved content.

It shall not present unsupported assumptions as verified company policy.

### FR-RAG-06 — Source Citations

**Priority:** Must (P0)

The system shall provide available source information, including:

- Document name.
- Relevant section.
- Page number where available.
- Website URL where applicable.

### FR-RAG-07 — Document Replacement and Deletion

**Priority:** Must (P0)

The system shall support authorized document replacement and deletion.

Replacement shall ensure that obsolete chunks and embeddings are not used in future retrieval.

Deletion shall remove or deactivate associated searchable content according to the configured retention policy.

### FR-RAG-08 — Knowledge-Base Permissions

**Priority:** Must (P0)

The default permissions shall be:

| Role | Upload | Replace | Delete | View |
|---|---:|---:|---:|---:|
| Customer | No | No | No | No direct administration access |
| Support Agent | Yes | No | No | Yes |
| Administrator | Yes | Yes | Yes | Yes |
| Business Owner | Yes | Yes | Yes | Yes |

The backend shall enforce these restrictions.

### FR-RAG-09 — Retrieval Failure

**Priority:** Must (P0)

If relevant content is not found, the agent shall not invent an answer.

It shall ask for clarification or offer human support.

---

## 3.5 Order Management and Tracking

### FR-ORD-01 — Order Lookup

**Priority:** Must (P0)

Customers shall be able to request order information.

The system shall verify ownership before returning order details.

### FR-ORD-02 — Order Status

**Priority:** Must (P0)

The system shall return verified order information, including:

- Order number.
- Order date.
- Order status.
- Payment status.
- Available delivery estimate.
- Tracking information, when available.

### FR-ORD-03 — Tracking Events

**Priority:** Must (P0)

The system shall maintain order tracking events, such as:

- Order placed.
- Order confirmed.
- Order packed.
- Order shipped.
- Out for delivery.
- Delivered.

Only verified tracking events shall be presented as actual events.

### FR-ORD-04 — Product Availability

**Priority:** Must (P0)

The system shall provide product availability information from the backend database.

The agent shall not guess inventory availability.

### FR-ORD-05 — Order Administration

**Priority:** Must (P0)

Authorized administrators shall be able to view and manage permitted product and order records.

All administrative modifications shall be validated and audited.

---

## 3.6 Refund Management

### FR-REF-01 — Refund Eligibility

**Priority:** Must (P0)

The system shall evaluate refund eligibility using configurable refund policies.

The backend shall verify:

- Order ownership.
- Order status.
- Payment status.
- Existing refund requests.
- Applicable policy.
- Eligible order items and amounts.

### FR-REF-02 — Policy Configuration

**Priority:** Must (P0)

Refund policies shall be configurable and versioned.

Policy configuration shall support:

- Return-window rules.
- Excluded products or categories.
- Eligible order statuses.
- Partial refund rules.
- Other business-specific conditions.

Exact policy values require business confirmation.

If no active policy exists, the system shall fail safely and shall not invent eligibility.

### FR-REF-03 — Refund Request Creation

**Priority:** Must (P0)

After eligibility is established, the system shall ask the customer to confirm the refund request.

Only after confirmation shall the backend create the refund request.

### FR-REF-04 — Human Approval

**Priority:** Must (P0)

Actual refund processing shall require human approval.

The AI agent shall not independently issue a payment refund.

### FR-REF-05 — Refund Status

**Priority:** Must (P0)

Customers shall be able to view their refund request status.

Authorized staff shall be able to review and update permitted refund workflow statuses.

### FR-REF-06 — Refund Audit

**Priority:** Must (P0)

The system shall record important refund actions, including:

- Eligibility evaluation.
- Request creation.
- Customer confirmation.
- Approval or rejection.
- Processing status changes.
- Responsible staff member.

---

## 3.7 Order Cancellation

### FR-CAN-01 — Cancellation Eligibility

**Priority:** Must (P0)

The backend shall check whether an order can be submitted for cancellation review.

### FR-CAN-02 — Cancellation Request

**Priority:** Must (P0)

The customer shall confirm before submitting a cancellation request.

The system shall create a request with a pending-review status.

### FR-CAN-03 — Human Review

**Priority:** Must (P0)

Cancellation shall not be automatically executed by the AI agent.

An authorized staff member shall review and process the request according to the configured business policy.

### FR-CAN-04 — Cancellation Status

**Priority:** Must (P0)

Customers shall be able to view the status of their cancellation request.

---

## 3.8 Support Ticket Management

### FR-TKT-01 — Ticket Creation

**Priority:** Must (P0)

The system shall create a support ticket when:

- The customer requests human support.
- The AI cannot resolve a query.
- A complaint requires human intervention.
- A configured escalation condition is met.

The system shall avoid creating duplicate tickets for the same confirmed action.

### FR-TKT-02 — Ticket Assignment

**Priority:** Must (P0)

Authorized support staff shall be able to assign tickets.

The system shall record assignment history.

### FR-TKT-03 — Ticket Status

**Priority:** Must (P0)

The system shall support:

- Open.
- In Progress.
- Resolved.
- Closed.
- Pending Customer Response.
- Escalated.
- Reopened.

### FR-TKT-04 — Ticket Notes

**Priority:** Must (P0)

Authorized staff shall be able to add internal notes.

Internal notes shall not be exposed to customers.

### FR-TKT-05 — Ticket Activity

**Priority:** Must (P0)

The system shall maintain an activity history containing important ticket events.

### FR-TKT-06 — Ticket Dashboard

**Priority:** Must (P0)

Support agents shall be able to:

- View assigned tickets.
- Filter tickets.
- Search tickets.
- View customer and authorized order information.
- Update ticket status.
- Add internal notes.
- Review conversation history.

### FR-TKT-07 — Escalation

**Priority:** Must (P0)

The system shall support escalation to human staff.

Escalation shall preserve the conversation context and relevant ticket information.

### FR-TKT-08 — Ticket Reopening

**Priority:** Must (P0)

The system shall support reopening eligible resolved or closed tickets according to configured rules.

---

## 3.9 Notifications

### FR-NOT-01 — In-App Notifications

**Priority:** Must (P0)

The system shall generate in-app notifications for relevant events, including:

- Ticket creation.
- Ticket assignment.
- Ticket escalation.
- Ticket status updates.
- Refund status updates.
- Cancellation status updates.

### FR-NOT-02 — Simulated Email Notifications

**Priority:** Must (P0)

The MVP shall support simulated email notifications.

The system shall record notification attempts and statuses.

Actual third-party email delivery integration may be introduced later.

### FR-NOT-03 — Notification History

**Priority:** Must (P0)

Users shall be able to view relevant notification history.

---

## 3.10 Administration and Business Oversight

### FR-ADM-01 — User Management

**Priority:** Must (P0)

Administrators shall be able to manage permitted user accounts.

### FR-ADM-02 — Role and Permission Management

**Priority:** Must (P0)

Authorized administrators shall be able to manage roles and permissions according to the configured security policy.

### FR-ADM-03 — Knowledge-Base Administration

**Priority:** Must (P0)

Authorized administrators shall be able to:

- Upload documents.
- View indexed documents.
- Replace documents.
- Delete documents.
- Review ingestion status.
- Retry failed ingestion jobs.

### FR-ADM-04 — Product and Order Management

**Priority:** Must (P0)

Authorized administrators shall be able to manage permitted product and order records.

### FR-ADM-05 — AI Configuration

**Priority:** Must (P0)

The system shall support controlled configuration of AI model assignments and relevant AI settings.

Secrets and API keys shall not be exposed through frontend configuration responses.

### FR-ADM-06 — Audit Logs

**Priority:** Must (P0)

The system shall record security-sensitive and administrative activities.

Audit records shall include relevant actor, action, target, timestamp and outcome information.

### FR-ADM-07 — Owner Analytics

**Priority:** Must (P0)

The business owner shall have access to basic operational metrics, including:

- Ticket volume.
- Open and resolved tickets.
- Escalation count.
- AI versus human handling.
- Average response time.
- Average resolution time.
- Common query categories.

Advanced analytics and sentiment trends may be enhanced in the advanced phase.

---

## 3.11 Background Processing

### FR-JOB-01 — Background Job Processing

**Priority:** Must (P0)

The system shall support background processing for tasks such as:

- Document ingestion.
- Embedding generation.
- Notification processing.
- Conversation summarization.
- Retryable operations.

### FR-JOB-02 — Persistent Job Storage

**Priority:** Must (P0)

Background jobs shall be stored in PostgreSQL.

A separate lightweight worker process shall claim and execute jobs.

The worker shall use safe job-claiming logic, such as PostgreSQL `FOR UPDATE SKIP LOCKED`, to prevent multiple workers from claiming the same job concurrently.

### FR-JOB-03 — Job Status

**Priority:** Must (P0)

The system shall track job statuses:

- Pending.
- Running.
- Completed.
- Failed.
- Retry Scheduled.

### FR-JOB-04 — Job Failure Handling

**Priority:** Must (P0)

The system shall support:

- Error recording.
- Configurable retry limits.
- Retry delays.
- Final failure status.
- Administrative visibility into failed jobs.

FastAPI BackgroundTasks may be used only for short, non-critical operations. Critical or retryable work shall use persistent jobs.

---

# 4. External Interface Requirements

## 4.1 User Interface

The frontend shall provide separate experiences for each role.

### Customer Portal

- Registration and login.
- AI chat.
- Conversation history.
- Order tracking.
- Refund request status.
- Cancellation request status.
- Support tickets.
- Customer profile.
- Notifications.

### Support Dashboard

- Assigned ticket list.
- Ticket search and filters.
- Conversation details.
- Customer information.
- Authorized order information.
- Internal notes.
- Assignment and status management.
- Escalation controls.

### Administration Dashboard

- User and role management.
- Knowledge-base management.
- Product and order management.
- AI configuration.
- Audit log access.
- Ticket oversight.

### Business Owner Dashboard

- Operational metrics.
- Ticket volume and status.
- Resolution performance.
- AI and human support distribution.
- Common customer query categories.

## 4.2 API Interface

The backend shall expose REST APIs for:

- Authentication.
- Customer profiles.
- Conversations.
- AI chat.
- Knowledge-base documents.
- Orders.
- Refunds.
- Cancellation requests.
- Support tickets.
- Notifications.
- Administration.
- Background jobs.
- Analytics.

The detailed endpoint paths, HTTP methods, request schemas, response schemas and error formats shall be defined in `05_API_Specification.md`.

## 4.3 Database Interface

The application shall access PostgreSQL through SQLAlchemy.

Database schema changes shall be managed using Alembic migrations.

The system shall use pgvector for embedding storage and semantic retrieval.

## 4.4 External AI Interface

The application shall communicate with OpenAI through secure server-side API calls.

The backend shall:

- Protect API credentials.
- Handle provider errors.
- Apply timeouts.
- Record relevant usage and operational metrics.
- Avoid logging sensitive prompt content unnecessarily.

---

# 5. Non-Functional Requirements

## 5.1 Performance

| ID | Requirement | Target |
|---|---|---|
| NFR-PER-01 | Normal API response | P95 below 500 ms |
| NFR-PER-02 | Database-backed API response | P95 below 500 ms for normal indexed queries |
| NFR-PER-03 | AI first-token latency | P95 below 3 seconds where provider conditions permit |
| NFR-PER-04 | Complete AI response | P95 below 10 seconds for typical requests where provider conditions permit |
| NFR-PER-05 | Analytics response | P95 below 2 seconds for typical dashboard queries |

These are provisional engineering targets. They must be measured under a defined test environment and representative workload.

## 5.2 Scalability

**NFR-SCL-01**

The initial system shall target approximately 10–50 concurrent users.

**NFR-SCL-02**

The application shall use modular components so that backend services, workers and database capacity can be scaled independently.

**NFR-SCL-03**

The database design shall support future multi-business operation.

## 5.3 Security

**NFR-SEC-01 — Authentication**

Protected resources shall require valid authentication.

**NFR-SEC-02 — Authorization**

The backend shall enforce RBAC and resource-level access checks.

**NFR-SEC-03 — Password Protection**

Passwords shall be securely hashed.

**NFR-SEC-04 — Token Security**

Refresh tokens shall use secure cookies, rotation, revocation and reuse detection.

**NFR-SEC-05 — CSRF Protection**

Cookie-authenticated state-changing operations shall use appropriate CSRF protection.

**NFR-SEC-06 — Rate Limiting**

The system shall apply rate limits to authentication, chat and sensitive operations.

**NFR-SEC-07 — Data Isolation**

Customers shall not access other customers' resources.

**NFR-SEC-08 — Secure File Upload**

The system shall validate file types, file sizes and uploaded content.

**NFR-SEC-09 — Prompt Injection Defense**

The system shall treat retrieved documents and customer messages as untrusted input.

The LLM shall not be allowed to override backend permissions or execute unauthorized operations.

**NFR-SEC-10 — Secrets Management**

API keys and credentials shall be stored in environment configuration or an appropriate secrets manager, never committed to source control.

**NFR-SEC-11 — Auditability**

Security-sensitive operations shall be recorded.

**NFR-SEC-12 — Transport Security**

Production communication shall use HTTPS.

## 5.4 Reliability

**NFR-REL-01**

The application shall handle expected API and database failures without exposing internal stack traces to users.

**NFR-REL-02**

Critical background jobs shall be persisted and recoverable.

**NFR-REL-03**

Retryable jobs shall use controlled retry policies.

**NFR-REL-04**

Business operations shall use database transactions where consistency requires them.

**NFR-REL-05**

Sensitive operations shall use idempotency controls where duplicate execution could cause harm.

## 5.5 Maintainability

**NFR-MNT-01**

The backend shall use modular architecture and separation of concerns.

**NFR-MNT-02**

API, business logic, database access and AI orchestration shall be separated.

**NFR-MNT-03**

The project shall use meaningful naming conventions and documentation.

**NFR-MNT-04**

Database modifications shall use version-controlled migrations.

**NFR-MNT-05**

Git shall be used for source control.

## 5.6 Usability and Accessibility

**NFR-USA-01**

The interface shall be responsive across desktop and mobile screen sizes.

**NFR-USA-02**

The application shall provide understandable error messages.

**NFR-USA-03**

The interface shall provide loading indicators, validation feedback and success notifications.

**NFR-USA-04**

The application shall support keyboard navigation and basic accessibility practices.

## 5.7 Monitoring and Logging

**NFR-MON-01**

The backend shall use structured application logs.

**NFR-MON-02**

AI-related monitoring shall capture appropriate operational information, such as:

- Model used.
- Request duration.
- Token usage where available.
- Tool execution status.
- Retrieval results metadata.
- Failure category.

**NFR-MON-03**

Sensitive data and credentials shall not be unnecessarily recorded in logs.

## 5.8 Data Retention

**NFR-DAT-01**

The system shall maintain documented retention rules for customer data, conversations, audit logs and uploaded documents.

**NFR-DAT-02**

Deletion requests shall follow applicable legal and business retention requirements.

**NFR-DAT-03**

Sensitive customer data shall be protected through appropriate access controls.

Final retention durations require business and legal confirmation.

---

# 6. Business Workflow Requirements

## 6.1 Order Tracking Workflow

1. Customer opens the chat.
2. Customer asks for order status.
3. AI identifies the order-tracking intent.
4. AI requests an order number if required.
5. Backend validates the authenticated customer's ownership.
6. Backend retrieves verified order and tracking information.
7. AI generates a response from the verified result.
8. Conversation is saved.
9. Customer receives the response.
10. If unresolved, the customer may request human support.

**Important:** The AI must not invent delivery dates or tracking events.

## 6.2 Refund Workflow

1. Customer requests a refund.
2. AI identifies the refund intent.
3. Backend retrieves the relevant order.
4. Backend verifies ownership.
5. Backend evaluates eligibility using the active refund policy.
6. AI communicates the verified result.
7. If eligible, the customer confirms the request.
8. Backend creates the refund request.
9. Request enters the human-review workflow.
10. Authorized staff approves or rejects it.
11. Refund status is updated.
12. Customer receives a notification.

**Important:** Eligibility is not the same as approval. Actual refund processing requires human approval.

## 6.3 Cancellation Workflow

1. Customer requests cancellation.
2. Backend retrieves the order.
3. Backend checks applicable cancellation conditions.
4. AI explains the result.
5. Customer confirms the request.
6. Backend creates a cancellation request.
7. Request enters pending review.
8. Authorized staff reviews it.
9. The request is approved or rejected.
10. Customer receives the updated status.

**Important:** The AI does not automatically cancel an order.

## 6.4 Knowledge-Base Workflow

1. Authorized staff uploads a document or adds a URL.
2. Backend validates the input.
3. A background job is created.
4. Worker extracts the content.
5. Text is cleaned and divided into chunks.
6. Embeddings are generated.
7. Chunks and embeddings are stored.
8. Search indexes are updated.
9. Customer asks a question.
10. Hybrid retrieval finds relevant chunks.
11. AI generates an answer grounded in retrieved content.
12. Source information is returned to the customer.

## 6.5 Human Escalation Workflow

1. Customer asks a question.
2. AI identifies an unresolved issue or escalation requirement.
3. AI explains that human support is needed.
4. Customer confirms ticket creation when confirmation is required.
5. Backend creates a support ticket.
6. Ticket is assigned or placed in the appropriate queue.
7. Support agent reviews conversation context.
8. Agent responds and updates the ticket.
9. Customer receives a notification.

---

# 7. Data Requirements

The system shall use PostgreSQL and pgvector.

The database design is defined in `04_Database_Design.md`.

Major entities include:

| Module | Main Entities |
|---|---|
| Business and authorization | businesses, users, roles, permissions, user_roles, role_permissions |
| Customer | customers |
| Products and orders | products, orders, order_items, order_tracking_events |
| Refunds | refunds, refund_items, refund_policies |
| Cancellation | order_cancellation_requests |
| Support | support_tickets, ticket_assignments, ticket_notes, ticket_activities |
| Conversations | conversations, conversation_participants, messages, message_feedback |
| Knowledge base | documents, document_chunks |
| Memory | customer_memories |
| Authentication | refresh_tokens |
| Notifications | notifications |
| Monitoring | audit_logs |
| Background processing | background_jobs |
| Privacy | account_deletion_requests |
| Reliability | idempotency_keys |

All tenant-owned records shall be appropriately scoped to their business.

UUIDs shall be used as primary keys. Human-readable order and ticket numbers shall be stored separately.

---

# 8. Error Handling Requirements

The system shall use consistent API error responses.

Examples of expected HTTP status codes:

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 204 | Request successful with no response body |
| 400 | Invalid request |
| 401 | Authentication required or invalid |
| 403 | Authenticated user lacks permission |
| 404 | Resource not found or intentionally concealed due to ownership restrictions |
| 409 | Conflict or duplicate operation |
| 422 | Validation error |
| 429 | Rate limit exceeded |
| 500 | Unexpected server error |
| 503 | Temporary service unavailability |

The API shall not expose:

- Database stack traces.
- Internal file paths.
- Secrets or credentials.
- Raw provider error details.
- Sensitive customer information.

Errors shall be logged with appropriate request correlation information.

---

# 9. Acceptance Criteria

The MVP shall be considered functionally acceptable when the following conditions are met.

| ID | Acceptance Criterion |
|---|---|
| AC-01 | A customer can register and log in successfully |
| AC-02 | Protected endpoints reject unauthenticated requests |
| AC-03 | Customer access is restricted to their own resources |
| AC-04 | Unauthorized ownership access returns 404 |
| AC-05 | Customers can interact with the AI chat |
| AC-06 | The AI can classify common customer intents |
| AC-07 | The AI can retrieve relevant knowledge-base content |
| AC-08 | Knowledge-base answers include available source citations |
| AC-09 | Unsupported knowledge-base questions do not produce fabricated policy answers |
| AC-10 | Customers can retrieve verified order information |
| AC-11 | Customers can check product availability |
| AC-12 | Refund eligibility is checked against an active policy |
| AC-13 | Refund requests require customer confirmation |
| AC-14 | Actual refund processing requires human approval |
| AC-15 | Cancellation requests require customer confirmation and human review |
| AC-16 | Customers can create and view support tickets |
| AC-17 | Support agents can manage authorized assigned tickets |
| AC-18 | Internal notes are not visible to customers |
| AC-19 | Staff can escalate unresolved conversations |
| AC-20 | Notifications are recorded and visible to authorized users |
| AC-21 | Authorized staff can manage knowledge-base documents |
| AC-22 | Replaced or deleted documents do not leave obsolete searchable chunks active |
| AC-23 | Background jobs have persistent status and failure tracking |
| AC-24 | Administrative actions generate audit records |
| AC-25 | Customers can submit account deletion requests |
| AC-26 | Owner dashboard displays basic operational metrics |
| AC-27 | The application handles expected errors without exposing internal details |
| AC-28 | Automated tests cover core security and business workflows |

---

# 10. Requirement Traceability Matrix

This initial matrix links business requirements to implementation and testing areas. The detailed test-case mapping will be maintained in `08_Testing_Strategy.md`.

| Requirement Area | BRD Reference | Architecture / Module | Database Entities | Testing Focus |
|---|---|---|---|---|
| Authentication | User and security requirements | Auth module | users, refresh_tokens | Login, token rotation, revocation |
| RBAC | Role and permission requirements | Authorization module | roles, permissions, role_permissions | Permission enforcement |
| Customer ownership | Data privacy requirements | Customer and order services | customers, orders | Cross-customer access |
| AI chat | AI support requirements | AI orchestration | conversations, messages | Intent and response behavior |
| RAG | Knowledge-base requirements | Retrieval module | documents, document_chunks | Retrieval quality and citations |
| Order tracking | Order workflow | Order service | orders, order_tracking_events | Ownership and status accuracy |
| Product availability | Product support | Product service | products | Inventory accuracy |
| Refunds | Refund workflow | Refund service | refunds, refund_items, refund_policies | Eligibility and approval |
| Cancellation | Cancellation workflow | Cancellation service | order_cancellation_requests | Confirmation and review |
| Tickets | Human escalation | Ticket service | support_tickets, ticket_assignments, ticket_notes, ticket_activities | Assignment and visibility |
| Notifications | Notification requirements | Notification service | notifications | Creation and access |
| Background jobs | Processing requirements | Worker module | background_jobs | Claiming, retries and failures |
| Audit | Security requirements | Audit module | audit_logs | Audit completeness |
| Account deletion | Privacy requirements | Privacy module | account_deletion_requests | Request and retention workflow |
| Analytics | Owner oversight | Analytics module | tickets, messages, audit and related records | Metric correctness |

---

# 11. Assumptions and Pending Business Decisions

The following decisions are intentionally configurable or pending confirmation. They shall not block the initial architecture, but must be finalized before the corresponding production workflow is enabled.

| ID | Decision | Current Baseline |
|---|---|---|
| BD-01 | Refund return window | Configurable; exact duration pending |
| BD-02 | Refund exclusions | Configurable; exact categories pending |
| BD-03 | Partial refunds | Data model supports them; MVP policy behavior pending confirmation |
| BD-04 | Cancellation rules | Configurable; human review required |
| BD-05 | Data retention periods | Subject to legal and business confirmation |
| BD-06 | Embedding model | Configurable; initial vector dimension provisionally 1536 |
| BD-07 | Staff document permissions | Agents upload; admin/owner replace and delete |
| BD-08 | Production hosting | To be selected after local implementation and testing |
| BD-09 | Real email provider | Simulated email for MVP |
| BD-10 | Payment/refund gateway | Mock workflow for MVP; no real money movement |

If a policy is missing or ambiguous, the system shall fail safely rather than invent a business rule.

---

# 12. MVP Scope Boundary

## Included in MVP

- Authentication and authorization.
- Customer profile management.
- AI chat and basic intent classification.
- Controlled backend tool execution.
- Basic conversation memory and history.
- RAG with supported document formats and website ingestion.
- Hybrid search using PostgreSQL and pgvector.
- Order tracking.
- Product availability.
- Refund eligibility and human approval workflow.
- Cancellation request and human review workflow.
- Support tickets and escalation.
- Support dashboard.
- Knowledge-base administration.
- In-app and simulated email notifications.
- Background worker.
- Audit logs.
- Account deletion requests.
- Basic owner analytics.
- Docker-based local environment.

## Advanced Phase

- Hindi support.
- Advanced sentiment and urgency detection.
- Advanced confidence evaluation.
- Enhanced long-term memory.
- LangGraph orchestration.
- More sophisticated analytics.
- Production integrations with external services.

## Future Enhancements

- Real payment gateway integration.
- Automated refund execution after approved authorization.
- Real email/SMS providers.
- Live human chat.
- Production multi-business onboarding.
- Advanced observability and AI evaluation.

---

# 13. Document Dependencies

This SRS must remain consistent with the following project documents:

| Document | Filename | Purpose |
|---|---|---|
| Business Requirements | 01_BRD.md | Business objectives and scope |
| Software Requirements | 02_SRS.md | Functional and non-functional requirements |
| Technical Architecture | 03_Technical_Architecture.md | System components and communication |
| Database Design | 04_Database_Design.md | Tables, relationships and constraints |
| API Specification | 05_API_Specification.md | API contracts |
| Folder Structure | 06_Project_Folder_Structure.md | Code organization |
| Development Roadmap | 07_Development_Roadmap.md | Implementation sequence |
| Testing Strategy | 08_Testing_Strategy.md | Test cases and validation |

Any change to a requirement shall be reviewed against affected documents before implementation.

---

# 14. Approval Status

**Document:** 02_SRS.md  
**Version:** 1.1  
**Status:** Revised Draft — Pending Cross-Document Consistency Review and User Approval

This document is ready for consistency review against the BRD and Database Design.

No coding or implementation shall begin until all eight project documents have been revised, cross-checked and approved.