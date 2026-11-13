# 06 — Project Folder Structure

**Project:** AI-Powered E-commerce Customer Support Agent  
**Document:** Project Folder Structure  
**Version:** 1.1  
**Status:** Revised Draft — Pending Cross-Document Consistency Review and User Approval  
**Architecture:** Modular Monolith with Separate Background Worker  
**Backend:** Python, FastAPI  
**AI:** LangChain, OpenAI  
**Database:** PostgreSQL, pgvector  
**Frontend:** React, TypeScript, Tailwind CSS  
**Infrastructure:** Docker, Docker Compose

---

# 1. Introduction

## 1.1 Purpose

This document defines the complete directory and file organization of the AI-Powered E-commerce Customer Support Agent.

It explains:

- How the project repository will be organized.
- Where backend code will be written.
- Where frontend components will be stored.
- Where AI and RAG logic will reside.
- Where database models and migrations will be maintained.
- How background jobs will be organized.
- Where automated tests will be written.
- How configuration and environment variables will be managed.

## 1.2 Folder Structure Goals

The structure must:

1. Follow modular architecture.
2. Separate frontend and backend.
3. Separate API routes from business logic.
4. Separate database operations from AI orchestration.
5. Keep reusable components organized.
6. Support unit and integration testing.
7. Make debugging easier for beginners.
8. Support future enhancements without major restructuring.
9. Keep secrets outside version control.
10. Avoid unnecessary complexity.

## 1.3 Architectural Approach

The project will use a single Git repository containing:

- Backend application.
- Frontend application.
- Background worker.
- Database migrations.
- Automated tests.
- Docker configuration.
- Project documentation.

The backend will be a modular monolith. The background worker will be a separate process using the same backend codebase and PostgreSQL job table.

---

# 2. Root Project Structure

The repository name will be:

`ecommerce-ai-support-agent`

```text
ecommerce-ai-support-agent/
│
├── backend/
│
├── frontend/
│
├── infrastructure/
│
├── tests/
│
├── docs/
│
├── scripts/
│
├── .github/
│
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── Makefile
├── README.md
└── LICENSE
```

## 2.1 Root Directory Responsibilities

| File or Folder | Responsibility |
|---|---|
| backend/ | Python FastAPI application and worker |
| frontend/ | React and TypeScript application |
| infrastructure/ | Docker and deployment configuration |
| tests/ | Cross-module and end-to-end tests |
| docs/ | Approved project documentation |
| scripts/ | Development and maintenance scripts |
| .github/ | GitHub workflows and templates |
| .gitignore | Files excluded from Git |
| .dockerignore | Files excluded from Docker build contexts |
| docker-compose.yml | Local multi-service environment |
| Makefile | Optional shortcuts for common commands |
| README.md | Project overview and setup instructions |
| LICENSE | Project license, selected before public release |

---

# 3. Backend Folder Structure

The backend will use Python, FastAPI, SQLAlchemy, Alembic and LangChain.

## 3.1 Complete Backend Structure

```text
backend/
│
├── app/
│   │
│   ├── main.py
│   ├── worker.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   │
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── customers.py
│   │       ├── products.py
│   │       ├── orders.py
│   │       ├── refunds.py
│   │       ├── cancellations.py
│   │       ├── conversations.py
│   │       ├── chat.py
│   │       ├── tickets.py
│   │       ├── knowledge_base.py
│   │       ├── notifications.py
│   │       ├── jobs.py
│   │       ├── analytics.py
│   │       │
│   │       └── admin/
│   │           ├── __init__.py
│   │           ├── users.py
│   │           ├── roles.py
│   │           ├── products.py
│   │           ├── orders.py
│   │           ├── refunds.py
│   │           ├── cancellations.py
│   │           ├── documents.py
│   │           ├── ai_config.py
│   │           ├── audit_logs.py
│   │           └── jobs.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   ├── middleware.py
│   │   ├── permissions.py
│   │   ├── constants.py
│   │   └── rate_limiter.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   ├── base.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── business.py
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── permission.py
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── order_tracking.py
│   │   ├── refund.py
│   │   ├── refund_policy.py
│   │   ├── cancellation.py
│   │   ├── support_ticket.py
│   │   ├── ticket_assignment.py
│   │   ├── ticket_note.py
│   │   ├── ticket_activity.py
│   │   ├── conversation.py
│   │   ├── conversation_participant.py
│   │   ├── message.py
│   │   ├── message_feedback.py
│   │   ├── document.py
│   │   ├── document_chunk.py
│   │   ├── customer_memory.py
│   │   ├── refresh_token.py
│   │   ├── notification.py
│   │   ├── audit_log.py
│   │   ├── background_job.py
│   │   ├── account_deletion_request.py
│   │   └── idempotency_key.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── refund.py
│   │   ├── cancellation.py
│   │   ├── conversation.py
│   │   ├── chat.py
│   │   ├── ticket.py
│   │   ├── knowledge_base.py
│   │   ├── notification.py
│   │   ├── job.py
│   │   └── analytics.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── customer_repository.py
│   │   ├── product_repository.py
│   │   ├── order_repository.py
│   │   ├── refund_repository.py
│   │   ├── cancellation_repository.py
│   │   ├── ticket_repository.py
│   │   ├── conversation_repository.py
│   │   ├── document_repository.py
│   │   ├── notification_repository.py
│   │   ├── audit_repository.py
│   │   └── job_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── customer_service.py
│   │   ├── product_service.py
│   │   ├── order_service.py
│   │   ├── refund_service.py
│   │   ├── cancellation_service.py
│   │   ├── conversation_service.py
│   │   ├── ticket_service.py
│   │   ├── knowledge_base_service.py
│   │   ├── notification_service.py
│   │   ├── audit_service.py
│   │   ├── account_deletion_service.py
│   │   └── analytics_service.py
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── llm_factory.py
│   │   ├── prompt_manager.py
│   │   ├── intent_classifier.py
│   │   ├── context_manager.py
│   │   ├── response_generator.py
│   │   ├── confidence_handler.py
│   │   │
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── order_tools.py
│   │   │   ├── product_tools.py
│   │   │   ├── refund_tools.py
│   │   │   ├── cancellation_tools.py
│   │   │   ├── ticket_tools.py
│   │   │   ├── customer_tools.py
│   │   │   ├── knowledge_tools.py
│   │   │   └── escalation_tools.py
│   │   │
│   │   ├── memory/
│   │   │   ├── __init__.py
│   │   │   ├── conversation_memory.py
│   │   │   ├── memory_repository.py
│   │   │   └── summarizer.py
│   │   │
│   │   └── prompts/
│   │       ├── system_prompt.md
│   │       ├── intent_prompt.md
│   │       ├── response_prompt.md
│   │       └── escalation_prompt.md
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   ├── document_loader.py
│   │   ├── text_cleaner.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   ├── hybrid_search.py
│   │   ├── reranker.py
│   │   ├── context_builder.py
│   │   ├── citation_builder.py
│   │   │
│   │   └── loaders/
│   │       ├── __init__.py
│   │       ├── pdf_loader.py
│   │       ├── txt_loader.py
│   │       ├── docx_loader.py
│   │       ├── csv_loader.py
│   │       ├── xlsx_loader.py
│   │       └── website_loader.py
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── job_runner.py
│   │   ├── job_registry.py
│   │   ├── job_claiming.py
│   │   │
│   │   └── handlers/
│   │       ├── __init__.py
│   │       ├── document_ingestion_handler.py
│   │       ├── notification_handler.py
│   │       ├── conversation_summary_handler.py
│   │       └── retry_handler.py
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── openai_client.py
│   │   ├── email_client.py
│   │   └── storage_client.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── datetime_utils.py
│       ├── pagination.py
│       ├── file_validation.py
│       └── idempotency.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_auth_service.py
│   │   ├── test_order_service.py
│   │   ├── test_refund_service.py
│   │   ├── test_ticket_service.py
│   │   ├── test_intent_classifier.py
│   │   └── test_rag_retriever.py
│   │
│   ├── integration/
│   │   ├── test_auth_api.py
│   │   ├── test_customer_api.py
│   │   ├── test_order_api.py
│   │   ├── test_refund_api.py
│   │   ├── test_ticket_api.py
│   │   ├── test_chat_api.py
│   │   └── test_knowledge_base_api.py
│   │
│   └── security/
│       ├── test_resource_ownership.py
│       ├── test_rbac.py
│       ├── test_refresh_token_reuse.py
│       └── test_idempotency.py
│
├── storage/
│   └── .gitkeep
│
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

# 4. Backend File Responsibilities

## 4.1 Application Entry Points

| File | Responsibility |
|---|---|
| `app/main.py` | Creates the FastAPI application and registers middleware and routers |
| `app/worker.py` | Starts the background worker process |

The API process and worker process shall be separate runtime processes.

They may share the same application modules and configuration.

## 4.2 API Folder

The `api/` directory contains HTTP endpoint definitions.

Each file corresponds to a resource or feature.

Examples:

- `auth.py`: Registration, login, logout and refresh.
- `orders.py`: Customer order retrieval.
- `refunds.py`: Refund eligibility and request endpoints.
- `chat.py`: AI chat and streaming endpoints.
- `tickets.py`: Ticket management.
- `knowledge_base.py`: Document upload and retrieval administration.

API files should validate requests and call services. They should not contain complex database or AI logic.

## 4.3 Core Folder

The `core/` directory contains application-wide functionality.

| File | Responsibility |
|---|---|
| config.py | Environment-based configuration |
| security.py | Password hashing and token utilities |
| exceptions.py | Custom application exceptions |
| logging.py | Structured logging configuration |
| middleware.py | Request IDs and application middleware |
| permissions.py | Permission dependencies and authorization helpers |
| constants.py | Shared constants and enums |
| rate_limiter.py | Rate-limiting configuration |

## 4.4 Database Folder

| File | Responsibility |
|---|---|
| session.py | Database engine and session management |
| base.py | SQLAlchemy declarative base and model registration support |
| init_db.py | Development database initialization utilities |

Database connections shall be managed centrally.

API handlers shall not create independent database engines.

## 4.5 Models Folder

The `models/` directory contains SQLAlchemy database models.

Examples:

- `user.py`: User entity.
- `order.py`: Order entity.
- `refund.py`: Refund entity.
- `support_ticket.py`: Support ticket entity.
- `message.py`: Conversation message entity.
- `document.py`: Knowledge document entity.
- `document_chunk.py`: Text chunk and embedding entity.
- `background_job.py`: Persistent job entity.

Each model should map to the corresponding database design.

A model represents database structure; it does not contain API request validation.

## 4.6 Schemas Folder

The `schemas/` directory contains Pydantic schemas.

Examples:

- `auth.py`: Registration and login request/response schemas.
- `order.py`: Order response and filtering schemas.
- `refund.py`: Refund request and response schemas.
- `chat.py`: Chat message and streaming metadata schemas.
- `ticket.py`: Ticket creation and update schemas.

Schemas define what data the application accepts and returns.

They are separate from SQLAlchemy models.

## 4.7 Repositories Folder

The `repositories/` directory contains database access logic.

Examples:

- `order_repository.py`: Retrieve orders.
- `refund_repository.py`: Retrieve and persist refunds.
- `ticket_repository.py`: Ticket database operations.
- `document_repository.py`: Document and chunk persistence.
- `job_repository.py`: Background job claiming and status updates.

Repositories should focus on persistence rather than business decisions.

## 4.8 Services Folder

The `services/` directory contains business logic.

Examples:

- `auth_service.py`: Authentication rules.
- `order_service.py`: Order ownership and retrieval.
- `refund_service.py`: Refund policy and approval workflow.
- `cancellation_service.py`: Cancellation request workflow.
- `ticket_service.py`: Ticket creation and assignment.
- `knowledge_base_service.py`: Document management.
- `audit_service.py`: Audit event creation.

Services coordinate repositories and other application components.

## 4.9 AI Folder

The `ai/` directory contains AI orchestration and related logic.

| File | Responsibility |
|---|---|
| orchestrator.py | Coordinates AI request processing |
| llm_factory.py | Creates configured LLM clients |
| prompt_manager.py | Loads and manages prompt templates |
| intent_classifier.py | Classifies customer intent |
| context_manager.py | Retrieves permitted conversation context |
| response_generator.py | Generates grounded responses |
| confidence_handler.py | Handles insufficient evidence and escalation conditions |

### AI Tools

The `ai/tools/` directory contains approved functions that the agent can invoke.

Each tool must call the relevant business service.

For example:

```text
AI Orchestrator
      |
      v
Order Tool
      |
      v
Order Service
      |
      v
Order Repository
      |
      v
PostgreSQL
```

The AI tool shall not bypass service-layer authorization.

### AI Memory

The `ai/memory/` directory handles:

- Session conversation context.
- Conversation summaries.
- Memory retrieval.
- Authorized customer context.

Persistent memory data shall be stored in PostgreSQL.

### AI Prompts

The `ai/prompts/` directory contains version-controlled prompt templates.

Prompts must not contain secrets or customer-specific private data.

## 4.10 RAG Folder

The `rag/` directory contains the document retrieval pipeline.

| File | Responsibility |
|---|---|
| ingestion.py | Coordinates ingestion |
| document_loader.py | Selects the appropriate loader |
| text_cleaner.py | Cleans extracted content |
| chunker.py | Splits content into chunks |
| embeddings.py | Generates embeddings |
| retriever.py | Retrieves relevant content |
| hybrid_search.py | Combines full-text and vector retrieval |
| reranker.py | Optional ranking refinement |
| context_builder.py | Prepares retrieved context |
| citation_builder.py | Builds source references |

The `loaders/` directory contains file-format-specific extraction logic.

## 4.11 Workers Folder

The `workers/` directory contains persistent background-job processing.

| File | Responsibility |
|---|---|
| job_runner.py | Main job execution loop |
| job_registry.py | Maps job types to handlers |
| job_claiming.py | Safely claims available jobs |
| document_ingestion_handler.py | Processes document ingestion |
| notification_handler.py | Processes notifications |
| conversation_summary_handler.py | Generates conversation summaries |
| retry_handler.py | Handles retryable failures |

The worker shall use the PostgreSQL job table and safe concurrent claiming.

## 4.12 Integrations Folder

The `integrations/` directory contains external-system adapters.

Examples:

- OpenAI client.
- Email provider adapter.
- File storage adapter.

The application shall interact with external providers through these adapters rather than spreading provider-specific code throughout business services.

## 4.13 Utils Folder

The `utils/` directory contains small reusable helpers.

Examples:

- Date and time utilities.
- Pagination helpers.
- File validation.
- Idempotency utilities.

Business rules should not be placed in generic utility functions.

---

# 5. Frontend Folder Structure

The frontend shall use React, TypeScript, Tailwind CSS and React Router.

## 5.1 Complete Frontend Structure

```text
frontend/
│
├── public/
│   ├── favicon.ico
│   └── logo.svg
│
├── src/
│   │
│   ├── main.tsx
│   ├── App.tsx
│   │
│   ├── app/
│   │   ├── router.tsx
│   │   ├── providers.tsx
│   │   └── query-client.ts
│   │
│   ├── assets/
│   │   ├── images/
│   │   └── icons/
│   │
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Loader.tsx
│   │   │   ├── Pagination.tsx
│   │   │   ├── ErrorMessage.tsx
│   │   │   └── Toast.tsx
│   │   │
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── DashboardLayout.tsx
│   │   │
│   │   └── charts/
│   │       ├── TicketChart.tsx
│   │       └── ResolutionChart.tsx
│   │
│   ├── features/
│   │   ├── auth/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── auth-api.ts
│   │   │   └── auth-types.ts
│   │   │
│   │   ├── customer/
│   │   │   ├── CustomerDashboard.tsx
│   │   │   ├── ProfilePage.tsx
│   │   │   └── customer-api.ts
│   │   │
│   │   ├── chat/
│   │   │   ├── ChatPage.tsx
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   ├── SourceCitation.tsx
│   │   │   ├── chat-api.ts
│   │   │   └── chat-types.ts
│   │   │
│   │   ├── orders/
│   │   │   ├── OrderList.tsx
│   │   │   ├── OrderDetails.tsx
│   │   │   ├── OrderTracking.tsx
│   │   │   └── order-api.ts
│   │   │
│   │   ├── refunds/
│   │   │   ├── RefundList.tsx
│   │   │   ├── RefundRequestForm.tsx
│   │   │   ├── RefundDetails.tsx
│   │   │   └── refund-api.ts
│   │   │
│   │   ├── cancellations/
│   │   │   ├── CancellationList.tsx
│   │   │   ├── CancellationRequestForm.tsx
│   │   │   └── cancellation-api.ts
│   │   │
│   │   ├── tickets/
│   │   │   ├── TicketList.tsx
│   │   │   ├── TicketDetails.tsx
│   │   │   ├── TicketForm.tsx
│   │   │   └── ticket-api.ts
│   │   │
│   │   ├── support/
│   │   │   ├── SupportDashboard.tsx
│   │   │   ├── AssignedTickets.tsx
│   │   │   ├── TicketAssignment.tsx
│   │   │   ├── InternalNotes.tsx
│   │   │   └── support-api.ts
│   │   │
│   │   ├── knowledge-base/
│   │   │   ├── KnowledgeDashboard.tsx
│   │   │   ├── DocumentUpload.tsx
│   │   │   ├── DocumentList.tsx
│   │   │   ├── WebsiteIngestion.tsx
│   │   │   └── knowledge-api.ts
│   │   │
│   │   ├── admin/
│   │   │   ├── AdminDashboard.tsx
│   │   │   ├── UserManagement.tsx
│   │   │   ├── RoleManagement.tsx
│   │   │   ├── ProductManagement.tsx
│   │   │   ├── OrderManagement.tsx
│   │   │   ├── AIConfiguration.tsx
│   │   │   └── AuditLogs.tsx
│   │   │
│   │   ├── analytics/
│   │   │   ├── AnalyticsDashboard.tsx
│   │   │   ├── TicketMetrics.tsx
│   │   │   └── analytics-api.ts
│   │   │
│   │   └── notifications/
│   │       ├── NotificationList.tsx
│   │       └── notification-api.ts
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useChat.ts
│   │   └── useNotifications.ts
│   │
│   ├── services/
│   │   ├── api-client.ts
│   │   ├── auth-client.ts
│   │   └── stream-client.ts
│   │
│   ├── store/
│   │   ├── auth-store.ts
│   │   └── ui-store.ts
│   │
│   ├── types/
│   │   ├── api.ts
│   │   ├── user.ts
│   │   └── common.ts
│   │
│   ├── utils/
│   │   ├── date.ts
│   │   ├── format.ts
│   │   └── validation.ts
│   │
│   └── styles/
│       └── index.css
│
├── tests/
│   ├── components/
│   ├── features/
│   └── e2e/
│
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

---

# 6. Frontend File Responsibilities

## 6.1 Application Entry Points

| File | Responsibility |
|---|---|
| main.tsx | Mounts the React application |
| App.tsx | Root application component |
| router.tsx | Defines application routes |
| providers.tsx | Registers application-wide providers |
| query-client.ts | Configures TanStack Query |

## 6.2 Components

Reusable UI elements shall be placed in `components/`.

Examples:

- Buttons.
- Inputs.
- Modals.
- Loaders.
- Pagination.
- Navigation.
- Charts.

Feature-specific business components shall remain in their respective feature folders.

## 6.3 Features

The `features/` directory organizes frontend code by business functionality.

For example, all chat-related components, API calls and types belong inside:

```text
src/features/chat/
```

This makes features easier to locate and maintain.

## 6.4 Services

The `services/` directory contains shared communication clients.

| File | Responsibility |
|---|---|
| api-client.ts | Shared Axios instance and common HTTP configuration |
| auth-client.ts | Authentication-related client helpers |
| stream-client.ts | SSE or streaming communication |

The frontend shall use the backend refresh-cookie strategy and shall not persist long-lived refresh tokens in local storage.

## 6.5 Hooks

Reusable React hooks shall be placed in `hooks/`.

Examples:

- Authentication state.
- Chat behavior.
- Notification state.

## 6.6 Store

The `store/` directory contains shared client-side state.

Only state that needs to be shared across components shall be placed here.

Server data should primarily be managed through TanStack Query.

## 6.7 Types

The `types/` directory contains shared TypeScript types.

API-specific types may remain inside their feature folders when they are not shared.

---

# 7. Infrastructure Folder Structure

```text
infrastructure/
│
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── worker.Dockerfile
│
├── database/
│   ├── init.sql
│   └── seed.sql
│
├── nginx/
│   └── nginx.conf
│
└── deployment/
    ├── deployment-notes.md
    └── environment-checklist.md
```

## 7.1 Dockerfiles

| File | Responsibility |
|---|---|
| backend.Dockerfile | Builds backend image |
| frontend.Dockerfile | Builds frontend image |
| worker.Dockerfile | Builds worker image |

Backend and worker may share a common build definition when appropriate, but they must have separate runtime commands.

## 7.2 Database Scripts

- `init.sql`: Development database initialization, including required extensions where appropriate.
- `seed.sql`: Optional development seed data.

Alembic migrations shall remain the authoritative source of schema changes. Seed scripts shall not independently redefine the schema.

## 7.3 Docker Compose

The root `docker-compose.yml` shall define:

- PostgreSQL with pgvector support.
- FastAPI backend.
- Python background worker.
- React frontend.

Local development may run the React development server directly instead of using its production container.

---

# 8. Documentation Folder

```text
docs/
│
├── 01_BRD.md
├── 02_SRS.md
├── 03_Technical_Architecture.md
├── 04_Database_Design.md
├── 05_API_Specification.md
├── 06_Project_Folder_Structure.md
├── 07_Development_Roadmap.md
└── 08_Testing_Strategy.md
```

All official project documentation shall use Markdown `.md` format.

The repository shall contain the approved versions of these documents.

---

# 9. GitHub Folder

```text
.github/
│
├── workflows/
│   ├── backend-tests.yml
│   └── frontend-tests.yml
│
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
│
└── pull_request_template.md
```

These files support:

- Automated testing.
- Issue reporting.
- Feature tracking.
- Consistent pull requests.

Automated deployment workflows may be added after the deployment strategy is selected.

---

# 10. Environment Configuration

## 10.1 Backend Environment File

Location:

`backend/.env.example`

Example:

```env
APP_ENV=development
APP_NAME=Ecommerce AI Support Agent

DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/ecommerce_ai

OPENAI_API_KEY=replace_with_your_key
OPENAI_CHAT_MODEL=replace_with_selected_model
OPENAI_EMBEDDING_MODEL=replace_with_selected_embedding_model

ACCESS_TOKEN_SECRET=replace_with_secure_secret

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

FRONTEND_URL=http://localhost:5173

UPLOAD_DIR=storage/uploads
MAX_UPLOAD_SIZE_MB=10
```

These values are examples. The actual model names, secrets and expiration policies shall be finalized during implementation.

## 10.2 Frontend Environment File

Location:

`frontend/.env.example`

Example:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Only public frontend configuration shall use the `VITE_` prefix.

Secrets such as OpenAI API keys must never be placed in frontend environment variables.

## 10.3 Environment Rules

- `.env` files shall not be committed.
- `.env.example` files shall contain placeholders only.
- Production secrets shall be managed securely.
- Different environments shall use separate configurations.
- Database credentials shall not be hardcoded.

---

# 11. Git Ignore Rules

The root `.gitignore` shall exclude:

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Environment files
.env
.env.*
!.env.example

# Frontend
node_modules/
dist/
coverage/

# IDE
.idea/
.vscode/

# Operating system
.DS_Store
Thumbs.db

# Logs
*.log

# Uploaded files and generated storage
backend/storage/*
!backend/storage/.gitkeep

# Test artifacts
htmlcov/
.coverage

# Temporary files
tmp/
temp/
```

The `.dockerignore` shall also exclude unnecessary local files, secrets, test artifacts and development dependencies from production image build contexts.

---

# 12. Naming Conventions

## 12.1 Python

Use:

- `snake_case` for files and functions.
- `PascalCase` for classes.
- `UPPER_SNAKE_CASE` for constants.

Examples:

```python
class OrderService:
    pass

def get_order_details():
    pass

MAX_UPLOAD_SIZE = 10
```

## 12.2 React and TypeScript

Use:

- `PascalCase` for React component files.
- `camelCase` for variables and functions.
- `PascalCase` for TypeScript types and interfaces.
- `kebab-case` for suitable non-component utility files.

Examples:

```text
ChatWindow.tsx
OrderDetails.tsx
order-api.ts
```

## 12.3 Database

Use:

- `snake_case` for table names.
- `snake_case` for column names.
- Explicit foreign-key naming.
- UUID primary keys.
- Separate human-readable ticket and order numbers.

---

# 13. Code Organization Rules

## 13.1 API Layer

API endpoints shall:

- Validate requests.
- Apply authentication and authorization.
- Call the appropriate service.
- Return structured responses.

They shall not contain large business workflows.

## 13.2 Service Layer

Services shall:

- Enforce business rules.
- Coordinate repositories.
- Manage transactions where required.
- Apply resource ownership checks.
- Coordinate audit events.

## 13.3 Repository Layer

Repositories shall:

- Execute database operations.
- Retrieve records.
- Persist records.
- Apply scoped database filters.

They shall not make independent LLM or business approval decisions.

## 13.4 AI Layer

AI modules shall:

- Coordinate model calls.
- Classify intent.
- Retrieve authorized context.
- Invoke approved tools.
- Generate responses.

They shall not bypass business services.

## 13.5 RAG Layer

RAG modules shall:

- Extract content.
- Clean and chunk content.
- Generate embeddings.
- Store searchable content.
- Perform hybrid retrieval.
- Prepare citations.

## 13.6 Worker Layer

Workers shall:

- Claim persistent jobs.
- Execute registered handlers.
- Track execution status.
- Handle retries.
- Record failures.

---

# 14. Testing Folder Organization

Backend tests shall be separated into:

| Test Directory | Purpose |
|---|---|
| unit/ | Individual functions and services |
| integration/ | API, database and module interactions |
| security/ | Authorization, ownership and sensitive-operation tests |

Frontend tests shall cover:

- Component behavior.
- Feature workflows.
- Form validation.
- Authentication state.
- Chat interactions.
- End-to-end customer journeys.

Cross-system end-to-end tests shall be maintained in the root `tests/` directory.

The detailed testing matrix and test scenarios shall be defined in `08_Testing_Strategy.md`.

---

# 15. Files That Must Not Be Created Prematurely

The folder structure defines the target architecture, not a requirement to create every file on the first day.

During implementation:

1. Create the project root.
2. Initialize the backend.
3. Configure the database.
4. Add the required modules incrementally.
5. Implement and test each feature.
6. Create frontend features when backend contracts are stable.
7. Add background processing when its database foundation is ready.

Empty modules should not be created without a defined purpose.

---

# 16. Recommended Development Order

The folder structure shall be implemented in the following sequence:

| Step | Work | Main Location |
|---|---|---|
| 1 | Initialize Git repository | Project root |
| 2 | Create Python virtual environment | backend/ |
| 3 | Initialize FastAPI | backend/app/ |
| 4 | Configure application settings | backend/app/core/ |
| 5 | Configure PostgreSQL | backend/app/database/ |
| 6 | Create SQLAlchemy models | backend/app/models/ |
| 7 | Configure Alembic | backend/alembic/ |
| 8 | Create authentication module | backend/app/api/ and services/ |
| 9 | Implement business services | backend/app/services/ |
| 10 | Implement AI orchestration | backend/app/ai/ |
| 11 | Implement RAG pipeline | backend/app/rag/ |
| 12 | Implement worker | backend/app/workers/ |
| 13 | Build frontend foundation | frontend/src/ |
| 14 | Implement frontend features | frontend/src/features/ |
| 15 | Add Docker configuration | infrastructure/ |
| 16 | Run integrated tests | tests/ |

The detailed phase-by-phase sequence will be defined in `07_Development_Roadmap.md`.

---

# 17. Folder Structure Validation Checklist

The project structure shall be considered ready when:

- [ ] Backend and frontend are separated.
- [ ] Backend API routes are separated from business services.
- [ ] Database models and Pydantic schemas are separated.
- [ ] Repositories are separated from services.
- [ ] AI orchestration is separated from business logic.
- [ ] RAG ingestion and retrieval are independently organized.
- [ ] Background worker has a separate entry point.
- [ ] Database migrations have a dedicated location.
- [ ] Tests are separated by test type.
- [ ] Environment examples are available.
- [ ] Secrets are excluded from Git.
- [ ] Docker configuration is organized.
- [ ] All eight Markdown documents are stored in docs/.
- [ ] The structure remains consistent with the API and database documents.

---

# 18. Dependencies on Other Documents

| Document | Filename | Dependency |
|---|---|---|
| Business Requirements | 01_BRD.md | Features and user roles |
| Software Requirements | 02_SRS.md | Functional requirements |
| Technical Architecture | 03_Technical_Architecture.md | Module responsibilities |
| Database Design | 04_Database_Design.md | Database entities |
| API Specification | 05_API_Specification.md | Endpoint organization |
| Project Folder Structure | 06_Project_Folder_Structure.md | Repository layout |
| Development Roadmap | 07_Development_Roadmap.md | Implementation sequence |
| Testing Strategy | 08_Testing_Strategy.md | Test organization |

---

# 19. Approval Status

**Document:** 06_Project_Folder_Structure.md  
**Version:** 1.1  
**Status:** Revised Draft — Pending Cross-Document Consistency Review and User Approval

This document defines the target repository structure. Files shall be created incrementally during implementation, after all eight project documents have been revised, cross-checked and approved.