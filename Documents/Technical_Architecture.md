# 03 — Technical Architecture

**Project:** AI-Powered E-commerce Customer Support Agent  
**Document:** Technical Architecture  
**Version:** 1.1  
**Status:** Revised Draft — Pending Cross-Document Consistency Review and User Approval  
**Architecture Style:** Modular Monolith with Separate Background Worker  
**Backend:** Python, FastAPI  
**AI Stack:** LangChain, OpenAI  
**Database:** PostgreSQL, pgvector  
**Frontend:** React, TypeScript, Tailwind CSS  
**Deployment:** Docker

---

# 1. Introduction

## 1.1 Purpose

This document describes the technical architecture of the AI-Powered E-commerce Customer Support Agent.

It explains:

- How the frontend communicates with the backend.
- How the backend communicates with PostgreSQL.
- How LangChain coordinates AI workflows.
- How RAG retrieves relevant knowledge.
- How backend tools perform verified business operations.
- How authentication and authorization protect resources.
- How background workers process long-running tasks.
- How the complete application is deployed.

## 1.2 Architectural Goals

The architecture must satisfy the following goals:

1. Beginner-friendly development and debugging.
2. Clear separation of responsibilities.
3. Secure customer data access.
4. Reliable AI-generated responses.
5. Verified business operations.
6. Modular and maintainable code.
7. Minimal initial infrastructure cost.
8. Future scalability.
9. Testability of individual components.
10. Support for future integrations.

## 1.3 Architectural Decision

<badge color="success">Selected architecture</badge>

**Modular Monolith + Separate Background Worker**

The MVP will use one backend application organized into independent modules.

A separate worker process will handle persistent background jobs.

This is preferred over microservices because:

- The project is a learning-focused MVP.
- Microservices introduce unnecessary deployment complexity.
- Modules can be tested independently.
- Services can be separated later if scaling requirements justify it.

---

# 2. High-Level System Architecture

## 2.1 Architecture Diagram

```mermaid
flowchart TB
    U[Customer / Support Agent / Admin / Owner]

    subgraph FRONTEND["Frontend Layer"]
        UI[React + TypeScript]
        CHAT[Chat Interface]
        DASH[Role-Based Dashboards]
    end

    subgraph BACKEND["Python Backend - FastAPI"]
        API[API Gateway / Routers]
        AUTH[Authentication and RBAC]
        SERVICE[Business Services]
        AI[AI Orchestration Layer]
        TOOLS[Controlled Backend Tools]
        RAG[RAG Retrieval Service]
        ADMIN[Administration Services]
    end

    subgraph DATA["Data Layer"]
        DB[(PostgreSQL)]
        VECTOR[(pgvector)]
        FILES[Document Storage]
    end

    subgraph AIEXT["External AI"]
        OPENAI[OpenAI API]
    end

    subgraph WORKERS["Background Processing"]
        QUEUE[(PostgreSQL Job Table)]
        WORKER[Background Worker]
    end

    U --> UI
    UI --> CHAT
    UI --> DASH
    CHAT --> API
    DASH --> API

    API --> AUTH
    API --> SERVICE
    API --> AI
    API --> ADMIN

    AI --> RAG
    AI --> TOOLS
    AI --> OPENAI

    SERVICE --> DB
    AUTH --> DB
    ADMIN --> DB
    TOOLS --> DB
    RAG --> DB
    RAG --> VECTOR
    RAG --> OPENAI

    API --> QUEUE
    WORKER --> QUEUE
    WORKER --> DB
    WORKER --> FILES
    WORKER --> OPENAI

    RAG --> FILES
```

## 2.2 Architecture Layers

| Layer | Responsibility | Technology |
|---|---|---|
| Presentation | User interface | React, TypeScript |
| API | HTTP endpoints and request validation | FastAPI |
| Authentication | Identity, tokens and permissions | JWT, password hashing |
| Business Logic | Orders, refunds, tickets and customers | Python services |
| AI Orchestration | Intent classification and tool coordination | LangChain |
| Retrieval | Document search and context construction | PostgreSQL FTS, pgvector |
| Data Access | Database operations | SQLAlchemy |
| Persistence | Structured and vector data | PostgreSQL, pgvector |
| Background Processing | Ingestion, notifications and summaries | PostgreSQL job table, Python worker |
| External AI | Language model and embeddings | OpenAI API |

---

# 3. Technology Stack

## 3.1 Backend

| Technology | Purpose |
|---|---|
| Python | Main backend programming language |
| FastAPI | REST API development |
| Pydantic | Input and output validation |
| SQLAlchemy | Database ORM |
| Alembic | Database migrations |
| LangChain | LLM integration and AI pipelines |
| OpenAI API | Language generation and embeddings |
| Pytest | Backend testing |
| Uvicorn | ASGI application server |

## 3.2 Frontend

| Technology | Purpose |
|---|---|
| React | Component-based UI |
| TypeScript | Static typing |
| Tailwind CSS | Styling |
| React Router | Routing |
| Axios | HTTP communication |
| TanStack Query | Server-state management |
| Zustand or Context | Client-side state |
| React Hook Form | Form handling |
| Zod | Frontend validation |
| Recharts | Analytics visualization |

## 3.3 Database

| Technology | Purpose |
|---|---|
| PostgreSQL | Relational database |
| pgvector | Vector storage and similarity search |
| PostgreSQL Full-Text Search | Keyword retrieval |
| SQLAlchemy | Database interaction |
| Alembic | Schema versioning |

## 3.4 Infrastructure

| Technology | Purpose |
|---|---|
| Git | Version control |
| GitHub | Repository hosting |
| Docker | Containerization |
| Docker Compose | Local multi-container environment |
| Postman | API testing |
| Environment variables | Configuration and secrets |

Technology versions shall be pinned in project dependency files after compatibility verification.

---

# 4. Backend Architecture

## 4.1 Backend Design

The backend shall follow a layered modular structure.

```text
Client Request
     |
     v
API Router
     |
     v
Authentication / Authorization
     |
     v
Request Validation
     |
     v
Business Service
     |
     v
Repository / Data Access
     |
     v
PostgreSQL
```

For AI requests:

```text
Customer Message
       |
       v
Chat API
       |
       v
Authentication Context
       |
       v
AI Orchestrator
       |
       v
Intent Classification
       |
       v
Decision
   /       \
  v         v
RAG       Backend Tool
  |         |
  v         v
Retrieve   Verify Business Data
Context    and Permissions
  |         |
  +----+----+
       |
       v
Response Generation
       |
       v
Save Conversation
       |
       v
Return Response
```

## 4.2 API Router Layer

Responsibilities:

- Define API endpoints.
- Receive HTTP requests.
- Validate request payloads.
- Apply authentication dependencies.
- Call business services.
- Return structured responses.

Routers shall not contain complex business logic.

## 4.3 Service Layer

The service layer contains business rules.

Examples:

- `AuthService`
- `CustomerService`
- `OrderService`
- `RefundService`
- `CancellationService`
- `TicketService`
- `ConversationService`
- `KnowledgeBaseService`
- `NotificationService`
- `AuditService`

Services shall enforce business rules before accessing or modifying data.

## 4.4 Repository Layer

Repositories shall handle database operations.

Examples:

- `UserRepository`
- `OrderRepository`
- `TicketRepository`
- `DocumentRepository`

Repositories shall not make independent business decisions.

## 4.5 Schema Layer

Pydantic schemas shall define:

- Request structures.
- Response structures.
- Input validation.
- Data serialization.

Separate input and output schemas shall be used where necessary to prevent accidental exposure of internal database fields.

---

# 5. Authentication and Authorization Architecture

## 5.1 Authentication Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant API as FastAPI
    participant AUTH as Auth Service
    participant DB as PostgreSQL

    C->>API: POST Login Credentials
    API->>AUTH: Validate Credentials
    AUTH->>DB: Find User
    DB-->>AUTH: User Record
    AUTH->>AUTH: Verify Password
    AUTH->>AUTH: Create Access and Refresh Tokens
    AUTH-->>API: Authentication Result
    API-->>C: Access Token + Secure Refresh Cookie
```

## 5.2 Token Strategy

The application shall use:

- Short-lived JWT access tokens.
- Rotating refresh tokens.
- Secure, HttpOnly refresh-token cookies.
- Refresh-token family tracking.
- Token revocation.
- Refresh-token reuse detection.

The frontend shall not store long-lived refresh tokens in local storage.

The refresh endpoint shall implement appropriate CSRF protection.

## 5.3 Authorization Flow

Every protected request shall pass through:

1. Token validation.
2. User identification.
3. Account status verification.
4. Role and permission checks.
5. Resource ownership checks.
6. Business operation validation.

## 5.4 Resource-Level Authorization

Example:

```text
Customer A requests Order A
       |
       v
Authenticated Customer ID = A
       |
       v
Backend checks order ownership
       |
       +---- Owner matches ----> Return order
       |
       +---- Owner differs ----> Return 404
```

The backend shall not trust customer IDs supplied by the LLM.

For AI tools, authenticated identity shall be passed from trusted backend context.

## 5.5 Role Permissions

| Capability | Customer | Support Agent | Admin | Owner |
|---|---:|---:|---:|---:|
| Own profile | Yes | Yes | Yes | Yes |
| Own orders | Yes | Limited authorized access | Yes | Yes |
| Customer chat | Yes | Authorized conversations | Yes | Yes |
| Assigned tickets | No | Yes | Oversight | Oversight |
| Internal notes | No | Yes | Yes | Yes |
| Upload documents | No | Yes | Yes | Yes |
| Replace documents | No | No | Yes | Yes |
| Delete documents | No | No | Yes | Yes |
| Manage users | No | No | Yes | Yes |
| Manage roles | No | No | Yes | Yes |
| View audit logs | No | No | Authorized | Yes |
| Owner analytics | No | No | Configurable | Yes |

The final permission matrix shall be implemented using the permissions defined in the database design.

---

# 6. AI Agent Architecture

## 6.1 Design Approach

The MVP shall use a single orchestrating AI agent with controlled backend tool execution.

It will not use a multi-agent architecture.

LangChain will provide the initial LLM integration and pipeline components.

LangGraph may be introduced later for more complex stateful workflows.

## 6.2 AI Agent Components

| Component | Responsibility |
|---|---|
| Chat Controller | Receives chat requests |
| Intent Classifier | Identifies the user's request category |
| Context Manager | Retrieves relevant conversation context |
| AI Orchestrator | Selects the next processing step |
| Tool Registry | Exposes approved backend tools |
| RAG Service | Retrieves knowledge-base information |
| Response Generator | Generates a grounded response |
| Conversation Service | Saves messages and history |
| Escalation Service | Creates or updates human-support tickets |

## 6.3 AI Processing Flow

```mermaid
flowchart TD
    A[Customer Message] --> B[Validate Session]
    B --> C[Load Conversation Context]
    C --> D[Classify Intent]
    D --> E{Identify Required Action}

    E -->|Policy / FAQ| F[RAG Retrieval]
    E -->|Order Query| G[Order Tool]
    E -->|Refund| H[Refund Eligibility Tool]
    E -->|Cancellation| I[Cancellation Tool]
    E -->|Complaint / Unresolved| J[Escalation Service]
    E -->|General Query| K[General Response Pipeline]

    F --> L[Validate Retrieved Context]
    G --> M[Validate Business Result]
    H --> M
    I --> M
    J --> N[Ticket Creation Workflow]
    K --> O[Generate Response]

    L --> O
    M --> O
    N --> P[Prepare Escalation Response]

    O --> Q[Save Conversation]
    P --> Q
    Q --> R[Return Response]
```

## 6.4 Tool Execution Rules

Every tool must:

1. Have a clearly defined input schema.
2. Validate input.
3. Obtain identity from trusted backend context.
4. Check permissions.
5. Validate business rules.
6. Perform authorized operations.
7. Return structured results.
8. Log relevant activity.

### Example: Order Lookup Tool

```python
def get_order_details(order_number: str, authenticated_customer_id: str):
    """
    Retrieve an order only if it belongs to the authenticated customer.
    """

    order = order_repository.get_by_order_number(order_number)

    if order is None:
        return None

    if order.customer_id != authenticated_customer_id:
        return None

    return {
        "order_number": order.order_number,
        "status": order.status,
        "payment_status": order.payment_status,
        "estimated_delivery": order.estimated_delivery
    }
```

This is illustrative pseudocode. The actual implementation shall use the project's SQLAlchemy session, business-scoped repository and consistent HTTP error handling.

The LLM may supply an order number, but it shall not supply or override the authenticated customer identity.

## 6.5 Sensitive Tool Execution

The following actions require explicit customer confirmation:

- Creating a refund request.
- Creating a cancellation request.
- Other configured sensitive operations.

The following actions require human review:

- Actual refund processing.
- Order cancellation execution.

The agent shall not independently approve or execute these operations.

## 6.6 Prompt and Context Security

The system shall:

- Treat customer messages as untrusted input.
- Treat retrieved documents as untrusted data.
- Keep system instructions separate from retrieved content.
- Avoid exposing internal prompts.
- Restrict available tools.
- Validate every tool result.
- Prevent retrieved instructions from granting additional permissions.
- Apply authorization outside the LLM.

---

# 7. RAG Architecture

## 7.1 RAG Overview

Retrieval-Augmented Generation allows the AI to answer questions using company-specific documents.

Instead of relying only on the model's pre-trained knowledge, the system retrieves relevant information from its knowledge base and provides that information to the model.

## 7.2 Document Ingestion Pipeline

```mermaid
flowchart TD
    A[Upload PDF / TXT / DOCX / CSV / XLSX / URL]
    A --> B[Validate Source]
    B --> C[Create Background Job]
    C --> D[Extract Text]
    D --> E[Clean Text]
    E --> F[Split into Chunks]
    F --> G[Generate Embeddings]
    G --> H[Store Document Metadata]
    H --> I[Store Chunks and Vectors]
    I --> J[Update Search Indexes]
    J --> K[Mark Job Completed]
```

## 7.3 Supported Sources

| Source | Processing |
|---|---|
| PDF | Extract text and page metadata |
| TXT | Read plain text |
| DOCX | Extract paragraphs and tables where supported |
| CSV | Parse structured text and rows |
| XLSX | Extract worksheet content |
| Website URL | Fetch and extract permitted page content |

Website ingestion shall enforce:

- Same-domain crawling restrictions.
- Configurable page limits.
- Request timeouts.
- URL validation.
- Private-network and local-address restrictions.
- Appropriate content-type validation.

These restrictions help prevent server-side request forgery (SSRF) and unintended internal-network access.

## 7.4 Chunking Strategy

Documents shall be divided into smaller sections called chunks.

Each chunk shall preserve useful metadata, including:

- Document ID.
- Business ID.
- Chunk index.
- Source filename or URL.
- Page number, where available.
- Section title, where available.
- Extracted text.

Initial chunk size and overlap shall be configurable.

A starting experiment may use approximately 500–800 tokens per chunk with 50–100 tokens of overlap. These are initial tuning values, not permanent requirements.

## 7.5 Embedding Generation

Embeddings convert text into numerical vectors.

The system shall use a configurable OpenAI embedding model.

The selected embedding model and vector dimensions must match the PostgreSQL pgvector column definition.

The initial database design provisionally assumes 1536 dimensions. This must be verified against the actual selected model before implementation.

## 7.6 Hybrid Retrieval

The system shall combine:

1. PostgreSQL full-text search.
2. pgvector semantic similarity search.

The initial fusion method shall be Reciprocal Rank Fusion.

Conceptually:

```text
Customer Question
       |
       +------> Full-Text Search
       |
       +------> Vector Similarity Search
                    |
                    v
             Combine Ranked Results
                    |
                    v
               RRF Ranking
                    |
                    v
              Top-K Chunks
                    |
                    v
             Context Construction
```

The system shall initially use exact vector search.

HNSW indexing may be introduced after retrieval quality and performance are measured.

## 7.7 Response Generation

The response generator shall receive:

- Customer question.
- Relevant conversation context.
- Retrieved knowledge chunks.
- Relevant verified business-tool results.
- Response constraints.

The model shall generate an answer grounded in the available context.

If evidence is insufficient, the system shall ask for clarification or escalate.

## 7.8 Document Lifecycle

Document statuses shall represent processing state, such as:

- Uploaded.
- Processing.
- Indexed.
- Failed.
- Inactive.

On replacement:

1. Validate the new document.
2. Process the new content.
3. Ensure the new index is available.
4. Deactivate the obsolete content safely.
5. Prevent old chunks from appearing in future retrieval.

On deletion:

- Deactivate or remove searchable chunks according to retention rules.
- Update associated document state.
- Record the administrative action.

---

# 8. Business Services Architecture

## 8.1 Order Service

Responsibilities:

- Retrieve customer orders.
- Validate ownership.
- Return verified order status.
- Retrieve tracking events.
- Check product availability.

The service shall not depend on AI-generated business values.

## 8.2 Refund Service

Responsibilities:

- Retrieve refund policy.
- Check refund eligibility.
- Calculate eligible amounts.
- Create confirmed refund requests.
- Track human approval.
- Update refund status.
- Record audit activity.

## 8.3 Cancellation Service

Responsibilities:

- Check cancellation conditions.
- Create confirmed cancellation requests.
- Maintain pending-review status.
- Support authorized staff decisions.
- Record workflow history.

## 8.4 Ticket Service

Responsibilities:

- Create support tickets.
- Assign tickets.
- Update status.
- Store internal notes.
- Track activities.
- Support escalation.
- Preserve conversation references.

## 8.5 Notification Service

Responsibilities:

- Create in-app notifications.
- Simulate email notifications.
- Record notification delivery attempts.
- Support retries through background jobs where appropriate.

## 8.6 Audit Service

Responsibilities:

- Record security-sensitive actions.
- Record administrative changes.
- Track refund and cancellation decisions.
- Maintain actor and target references.
- Prevent ordinary application users from modifying audit history.

---

# 9. Background Worker Architecture

## 9.1 Why a Worker Is Required

Some operations may take longer than a normal HTTP request.

Examples:

- Large document ingestion.
- Embedding generation.
- Website crawling.
- Conversation summarization.
- Notification delivery.

These tasks shall not block normal API request processing.

## 9.2 Selected Architecture

**PostgreSQL-backed job queue + separate Python worker process.**

A dedicated message broker is not required for the MVP.

## 9.3 Job Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Running
    Running --> Completed
    Running --> Failed
    Failed --> RetryScheduled
    RetryScheduled --> Pending
    Failed --> Failed
```

## 9.4 Worker Responsibilities

The worker shall:

1. Poll for available jobs.
2. Claim jobs safely.
3. Update job status.
4. Execute the registered handler.
5. Record results.
6. Retry eligible failures.
7. Mark exhausted jobs as failed.

PostgreSQL `FOR UPDATE SKIP LOCKED` shall be used for safe concurrent job claiming.

## 9.5 Job Types

| Job | Purpose |
|---|---|
| Document Ingestion | Extract and index documents |
| Embedding Generation | Generate vectors |
| Website Crawling | Import approved website content |
| Notification | Process notification delivery |
| Conversation Summary | Create conversation summaries |
| Retry | Re-execute eligible failed operations |

FastAPI BackgroundTasks may be used for short, non-critical tasks only.

---

# 10. Real-Time Communication Architecture

## 10.1 Chat Communication

The application shall support streaming AI responses.

A suitable initial approach is Server-Sent Events (SSE) for one-way response streaming.

WebSockets may be used where two-way real-time communication is required.

## 10.2 WebSocket Use Cases

- Real-time chat updates.
- Ticket assignment notifications.
- Ticket status changes.
- Staff conversation updates.

## 10.3 Fallback

If real-time communication is unavailable, the frontend shall use polling to retrieve updates.

## 10.4 Connection Security

Real-time connections shall authenticate users and enforce the same resource-level permissions as REST endpoints.

A connected customer shall only receive events for conversations and resources they are authorized to access.

---

# 11. Database Architecture

## 11.1 Database Selection

PostgreSQL with pgvector shall be the primary database.

Reasons:

- Relational data support.
- Transaction management.
- Foreign keys and constraints.
- Full-text search.
- Vector similarity search.
- Reduced infrastructure complexity.

## 11.2 Database Access

The backend shall use:

- SQLAlchemy for database interaction.
- Alembic for migrations.
- Explicit transaction boundaries.
- Parameterized queries through the ORM or safe SQL execution.

## 11.3 Tenant Awareness

The MVP shall run one demo business.

Business identifiers shall be included in tenant-owned data.

The backend shall resolve business context from trusted configuration or authenticated server-side context.

The client shall not choose arbitrary tenant IDs.

## 11.4 Data Integrity

The system shall use:

- UUID primary keys.
- Foreign-key constraints.
- Unique constraints.
- Check constraints.
- Appropriate indexes.
- Transactional workflows.
- Idempotency keys for sensitive repeatable operations.

The detailed schema is defined in `04_Database_Design.md`.

---

# 12. Frontend Architecture

## 12.1 Frontend Design

The frontend shall use role-based application areas.

```text
React Application
       |
       v
Authentication Context
       |
       v
Application Router
       |
       +---- Customer Portal
       |
       +---- Support Dashboard
       |
       +---- Admin Dashboard
       |
       +---- Owner Dashboard
```

## 12.2 Customer Portal

Main modules:

- Login and registration.
- Chat interface.
- Conversation history.
- Order tracking.
- Refund status.
- Cancellation status.
- Support tickets.
- Customer profile.
- Notifications.

## 12.3 Support Dashboard

Main modules:

- Ticket list.
- Ticket filters.
- Ticket details.
- Conversation history.
- Internal notes.
- Customer and order context.
- Ticket assignment.
- Status management.
- Escalation.

## 12.4 Admin Dashboard

Main modules:

- User management.
- Role and permission management.
- Knowledge-base management.
- Product management.
- Order management.
- AI configuration.
- Audit logs.
- Ticket oversight.

## 12.5 Owner Dashboard

Main modules:

- Ticket statistics.
- Resolution metrics.
- AI versus human handling.
- Response times.
- Common query categories.
- Basic operational analytics.

## 12.6 Frontend Security

Frontend role-based navigation improves usability but does not provide security.

All protected operations shall be authorized by the backend.

---

# 13. API Communication Architecture

## 13.1 Request Flow

```text
React Frontend
      |
      v
Axios HTTP Client
      |
      v
FastAPI Endpoint
      |
      v
Authentication
      |
      v
Authorization
      |
      v
Pydantic Validation
      |
      v
Business Service
      |
      v
Database / AI / Worker
      |
      v
Structured API Response
      |
      v
React UI Update
```

## 13.2 API Standards

The API shall use:

- Consistent URL naming.
- Appropriate HTTP methods.
- Structured JSON responses.
- Standard HTTP status codes.
- Input validation.
- Pagination for large collections.
- Consistent error formats.
- Request correlation IDs.

## 13.3 API Versioning

The initial API shall use a versioned prefix:

```text
/api/v1/
```

Detailed endpoint contracts shall be documented in `05_API_Specification.md`.

---

# 14. Error Handling and Observability

## 14.1 Error Handling

The application shall handle:

- Invalid input.
- Authentication failures.
- Authorization failures.
- Missing resources.
- Database errors.
- OpenAI API errors.
- Rate limits.
- Background job failures.
- WebSocket and streaming interruptions.

Internal errors shall be logged without exposing sensitive implementation details to users.

## 14.2 Logging

The application shall use structured logs.

Important fields may include:

- Timestamp.
- Request ID.
- User ID where appropriate.
- Business ID.
- Module.
- Operation.
- Outcome.
- Duration.
- Error category.

Sensitive data and credentials shall not be logged unnecessarily.

## 14.3 AI Monitoring

AI monitoring shall capture appropriate operational metrics:

- Model assignment.
- Request duration.
- Token usage where available.
- Tool invocation count.
- Tool success and failure.
- Retrieval performance.
- Escalation rate.
- AI response latency.

---

# 15. Deployment Architecture

## 15.1 Local Development

The initial local environment shall contain:

```mermaid
flowchart TB
    B[Browser]
    FE[React Frontend Container]
    API[FastAPI Backend Container]
    WORKER[Python Worker Container]
    DB[(PostgreSQL + pgvector)]

    B --> FE
    FE --> API
    API --> DB
    WORKER --> DB
    API --> OPENAI[OpenAI API]
    WORKER --> OPENAI
```

The frontend may initially run directly through the Node.js development server while backend and database services run through Docker Compose.

## 15.2 Docker Services

Initial services:

| Service | Responsibility |
|---|---|
| frontend | React application |
| backend | FastAPI application |
| worker | Background job processor |
| database | PostgreSQL with pgvector |

A separate Redis service is not required for the MVP.

## 15.3 Environment Configuration

Example configuration:

```env
APP_ENV=development

DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/ecommerce_ai

OPENAI_API_KEY=your_api_key

ACCESS_TOKEN_SECRET=replace_with_secure_secret

FRONTEND_URL=http://localhost:5173
```

This is an illustrative configuration.

Actual secret values must be generated securely and must never be committed to Git.

## 15.4 Production Deployment

The final hosting provider shall be selected after local implementation and testing.

Production deployment shall include:

- HTTPS.
- Secure environment configuration.
- Database backups.
- Application monitoring.
- Worker monitoring.
- Database migration management.
- Rate limiting.
- Error tracking.
- Secure file storage.

---

# 16. Scalability and Future Architecture

The initial architecture shall be a modular monolith.

Future improvements may include:

| Area | Future Enhancement |
|---|---|
| Backend | Separate high-load modules into services if justified |
| AI | Introduce LangGraph for complex workflows |
| Retrieval | Evaluate HNSW and advanced retrieval techniques |
| Background Jobs | Introduce Redis or a dedicated message broker if required |
| Storage | Move document files to object storage |
| Search | Evaluate dedicated search infrastructure if needed |
| Multi-tenancy | Support production business onboarding |
| Monitoring | Add advanced distributed tracing |
| Integrations | Connect real payment, shipping and email services |

These enhancements shall be driven by measured requirements rather than added prematurely.

---

# 17. Architecture Decisions and Rationale

| ID | Decision | Reason |
|---|---|---|
| ADR-01 | Modular monolith | Lower complexity for MVP |
| ADR-02 | FastAPI | Python API development and validation |
| ADR-03 | PostgreSQL | Relational data and transaction support |
| ADR-04 | pgvector | Semantic search without separate vector infrastructure |
| ADR-05 | Hybrid retrieval | Combines keyword and semantic search |
| ADR-06 | LangChain | Initial LLM pipeline integration |
| ADR-07 | LangGraph later | Avoid premature orchestration complexity |
| ADR-08 | Controlled tool execution | Protects business operations |
| ADR-09 | Human refund approval | Prevents unauthorized financial execution |
| ADR-10 | Human cancellation review | Prevents unintended order cancellation |
| ADR-11 | PostgreSQL-backed worker | Persistent jobs without an additional broker |
| ADR-12 | JWT access and rotating refresh tokens | Stateless API access with controlled session renewal |
| ADR-13 | Tenant-aware schema | Supports future business isolation |
| ADR-14 | React and TypeScript | Maintainable frontend development |
| ADR-15 | Docker Compose | Reproducible local environment |

---

# 18. Architecture Validation Criteria

The architecture shall be considered ready for implementation when:

1. Every MVP requirement in the BRD and SRS has a corresponding architectural component.
2. Every protected operation has an authentication and authorization boundary.
3. Customer identity is derived from trusted backend context.
4. The AI cannot bypass business rules.
5. RAG ingestion and retrieval flows are defined.
6. Refund and cancellation workflows require appropriate human review.
7. Background jobs are persistent and recoverable.
8. Database responsibilities are consistent with the database design.
9. API and frontend responsibilities are separated.
10. Local deployment can be reproduced using documented steps.
11. The architecture supports automated unit and integration testing.
12. All unresolved business decisions are documented rather than assumed.

---

# 19. Dependencies on Other Documents

| Document | Filename | Architecture Dependency |
|---|---|---|
| Business Requirements | 01_BRD.md | Business scope and workflows |
| Software Requirements | 02_SRS.md | Functional and non-functional requirements |
| Database Design | 04_Database_Design.md | Data model and constraints |
| API Specification | 05_API_Specification.md | Endpoint contracts |
| Folder Structure | 06_Project_Folder_Structure.md | Module organization |
| Development Roadmap | 07_Development_Roadmap.md | Implementation sequence |
| Testing Strategy | 08_Testing_Strategy.md | Validation and quality assurance |

---

# 20. Approval Status

**Document:** 03_Technical_Architecture.md  
**Version:** 1.1  
**Status:** Revised Draft — Pending Cross-Document Consistency Review and User Approval

This document establishes the proposed technical architecture. Implementation shall begin only after all eight project documents have been revised, cross-checked and approved.