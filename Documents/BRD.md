# 01 — Business Requirements Document (BRD)

## 1. Document Information

| Field | Details |
|---|---|
| Project Name | AI-Powered E-commerce Customer Support Agent |
| Document | Business Requirements Document |
| Version | 1.1 |
| Status | Revised Draft — Pending Approval |
| Project Type | Learning and Portfolio Project |
| Primary Users | Customers, Support Agents, Administrators, Business Owners |
| Initial Business Model | Single demo business |
| Future Business Model | Multi-business support |
| Backend | Python + FastAPI |
| Frontend | React + TypeScript |
| Database | PostgreSQL + pgvector |
| AI Framework | LangChain |

---

## 2. Executive Summary

The project aims to develop an AI-powered customer support platform for an e-commerce business.

The application will use a Large Language Model (LLM), Retrieval-Augmented Generation (RAG), backend business tools and a web-based interface to automate common customer support activities.

Customers will be able to:
- Ask questions about company policies and products.
- Check order status and shipment information.
- Check product availability.
- Check refund eligibility.
- Create and track support tickets.
- Receive assistance from an AI support agent.
- Escalate unresolved issues to human support.

Support agents will manage tickets and customer conversations. Administrators will manage users, permissions and knowledge-base documents. Business owners will access operational analytics.

The AI agent will not independently control business records. Verified customer, order, inventory, refund and ticket information must come from authorized backend services.

The project will initially use mock business data and simulated external integrations to keep development affordable and manageable.

---

## 3. Business Problem

E-commerce businesses receive large volumes of repetitive customer support requests.

Common questions include:
- Where is my order?
- When will my order be delivered?
- What is the return policy?
- Can I request a refund?
- Is a particular product available?
- How can I contact customer support?
- How can I raise a complaint?

Traditional support systems often require human intervention for routine queries.

This can result in:
- Long response times.
- Repetitive manual work.
- Increased support workload.
- Inconsistent responses.
- Difficulty retrieving relevant policy information.
- Delayed issue resolution.

The proposed system will automate suitable interactions while preserving human control over sensitive operations.

---

## 4. Business Objectives

The primary objectives are:

1. Automate common customer support questions.
2. Reduce repetitive support-agent workload.
3. Provide accurate answers from approved business documents.
4. Retrieve verified order and product information.
5. Automate support-ticket creation and routing.
6. Provide a controlled refund eligibility workflow.
7. Escalate unresolved or sensitive issues to human agents.
8. Maintain customer conversation history.
9. Provide operational analytics.
10. Build a modular application that can support future enhancements.

### Success Indicators

| Indicator | Measurement |
|---|---|
| AI response quality | Human-reviewed response evaluation |
| RAG quality | Retrieval relevance and answer faithfulness |
| Order lookup accuracy | Correct backend order data returned |
| Ticket creation success | Successful ticket creation rate |
| Escalation reliability | Correct escalation workflow execution |
| API reliability | Successful request rate |
| Customer feedback | Message ratings and CSAT |
| Support efficiency | Response and resolution time |
| Security | Authorization and security test results |

The project will establish baseline measurements using mock data. Actual improvement percentages will not be claimed without measured results.

---

## 5. Stakeholders and User Roles

### 5.1 Customer

A customer can:
- Register and log in.
- View their profile.
- View their own orders.
- Track shipments using available tracking information.
- Ask AI support questions.
- View conversation history.
- Check refund eligibility.
- Submit a refund request.
- Create support tickets.
- View their own tickets.
- Provide feedback.
- Request account deletion.

Customers must never access another customer's private information.

### 5.2 Support Agent

A support agent can:
- View tickets assigned to them.
- View authorized customer information associated with their support work.
- View authorized order details.
- Participate in support conversations.
- Update permitted ticket statuses.
- Add internal ticket notes.
- Escalate tickets.
- Upload knowledge-base documents.
- Check refund eligibility through authorized workflows.

Agents cannot approve refunds in the MVP.

Agents cannot replace or delete knowledge-base documents by default.

### 5.3 Administrator

An administrator can:
- Manage users and roles.
- View and manage support tickets.
- Assign tickets.
- Upload, replace and delete knowledge-base documents.
- Manage products and orders through authorized interfaces.
- Review refund requests.
- Approve or reject refunds.
- Review audit logs.
- Configure business-level settings.

### 5.4 Business Owner

A business owner can:
- View business analytics.
- Monitor support operations.
- Review ticket and resolution statistics.
- View customer feedback metrics.
- Monitor AI performance.
- Review business-level settings.
- Oversee support operations.

The owner role does not automatically bypass sensitive approval rules.

---

## 6. Project Scope

### 6.1 MVP Scope — Must Have

The initial MVP includes:

**Authentication and authorization**
- Customer registration and login.
- JWT access authentication.
- Refresh-token rotation.
- Role-based access control.
- Resource-level authorization.

**Customer management**
- Customer profile.
- Customer order history.
- Conversation history.

**AI support**
- OpenAI integration.
- LangChain-based LLM pipeline.
- Customer question answering.
- Structured AI responses.
- Basic intent classification.
- Basic confidence and insufficient-context handling.

**Knowledge base**
- PDF, TXT, DOCX, CSV and XLSX ingestion.
- Individual website URL ingestion.
- Limited same-domain website crawling.
- Document chunking and embeddings.
- PostgreSQL full-text search.
- pgvector semantic search.
- Hybrid retrieval.
- Source citations.
- Document upload and management.

**E-commerce operations**
- Order lookup.
- Shipment tracking from stored tracking information.
- Product availability lookup.
- Refund eligibility.
- Customer refund request.
- Human refund approval and rejection.
- Order cancellation request and human review.

**Support management**
- Support ticket creation.
- Ticket assignment.
- Ticket status management.
- Internal notes.
- Ticket activity history.
- Human escalation.

**Notifications**
- In-app notifications.
- Simulated email notifications.
- Ticket status and assignment notifications.

**Memory**
- Conversation history.
- Basic persistent conversation summaries.

**Administration**
- User and role management.
- Knowledge-base document management.
- Ticket oversight.
- Audit logs.

**Testing and deployment**
- Unit testing.
- API testing.
- Integration testing.
- End-to-end testing of critical workflows.
- Security testing.
- Docker-based local environment.

### 6.2 Advanced Phase

The following capabilities are planned after the MVP:

- Advanced intent classification.
- Advanced sentiment analysis.
- Complaint urgency prediction.
- Advanced confidence evaluation.
- English and Hindi support.
- Advanced conversation memory.
- LangGraph-based stateful orchestration.
- Advanced AI evaluation.
- Expanded analytics.
- Advanced multilingual retrieval.

### 6.3 Future Enhancements

The following are outside the initial MVP:

- Real payment and refund-provider integration.
- Actual payment reversal.
- Live human chat infrastructure.
- Real email delivery provider.
- Multiple e-commerce platform integrations.
- Production multi-tenant onboarding.
- Additional languages.
- Advanced workflow automation.

---

## 7. Core Business Workflows

### 7.1 Customer Order Tracking

1. Customer logs in.
2. Customer asks about an order.
3. AI agent requests an order number if necessary.
4. Backend verifies customer ownership.
5. Backend retrieves order and tracking information.
6. AI agent generates a response using verified data.
7. Customer receives the order status and available delivery information.

Business rule:

The AI must never invent order status, delivery date, carrier or tracking number.

If tracking data is unavailable, the system must communicate that clearly.

### 7.2 Knowledge-Base Question Answering

1. Authorized staff uploads a business document.
2. Backend validates the file.
3. Document ingestion extracts and cleans content.
4. Content is divided into chunks.
5. Embeddings are generated.
6. Chunks are stored in PostgreSQL with pgvector.
7. Full-text search indexes are maintained.
8. Customer submits a question.
9. The retrieval system searches relevant content.
10. LLM generates an answer using retrieved context.
11. The response includes source information.

Business rule:

If relevant information is unavailable, the agent must ask for clarification or offer human support instead of inventing an answer.

### 7.3 Refund Eligibility and Approval

1. Customer asks about a refund.
2. Agent requests an order identifier if needed.
3. Backend verifies order ownership.
4. Backend retrieves the applicable refund policy.
5. Backend checks delivery date or purchase date.
6. Backend checks exclusions and order status.
7. Backend calculates the eligible amount.
8. Customer receives the eligibility result.
9. Customer confirms the refund request.
10. Backend creates a refund request.
11. Authorized administrator reviews the request.
12. Administrator approves or rejects it.
13. The customer receives a notification.

Business rules:

- Refund eligibility is calculated by backend services.
- The AI cannot independently approve refunds.
- Actual payment processing is excluded from the MVP.
- The refund policy must be configured before eligibility can be evaluated.
- If no applicable policy exists, the system must not invent one.
- Duplicate active refund requests must be prevented.
- Partial refunds are supported by the data model but remain subject to final MVP policy configuration.

### 7.4 Order Cancellation

1. Customer requests cancellation.
2. Backend verifies customer ownership.
3. Backend checks current order status.
4. Agent explains the cancellation request process.
5. Customer confirms the request.
6. Backend creates a cancellation request.
7. Authorized staff reviews the request.
8. Staff approves or rejects it.
9. Customer receives the outcome.

Business rules:

- No automatic cancellation is performed in the MVP.
- The order is not marked cancelled merely because a customer asks.
- Only an authorized service operation can change the order status.
- Payment reversal is outside the MVP.

### 7.5 Support Ticket Creation

1. Customer describes an unresolved issue.
2. Agent identifies that human support is required.
3. Agent summarizes the issue.
4. Customer is asked to confirm ticket creation.
5. Backend creates the ticket.
6. Ticket receives a unique ticket number.
7. Ticket is assigned according to the initial assignment policy.
8. Customer receives confirmation.
9. Support staff manages the ticket.

### 7.6 Human Escalation

Escalation occurs when:
- AI cannot resolve the query.
- Required information is missing.
- Retrieval confidence is insufficient.
- Customer requests a human.
- A sensitive operation requires human review.
- The issue is urgent or complex.

The system must preserve relevant conversation context when escalating.

---

## 8. Business Rules

### 8.1 Identity and Access
- All protected operations require authentication.
- Backend services enforce permissions.
- Customers access only their own data.
- Staff access is restricted according to assigned roles and permissions.
- Business-level isolation is enforced.
- Resource ownership failures must not reveal whether another customer's resource exists.

### 8.2 AI and Business Data
- LLM responses are not a source of truth for business records.
- Order details come from backend services.
- Refund eligibility comes from backend services.
- Product availability comes from backend services.
- Retrieved document content is treated as untrusted data.
- Prompt instructions embedded in uploaded documents must not override system policies.

### 8.3 Refunds
- A configured refund policy is required.
- Eligibility is checked by backend logic.
- Customer confirmation is required before submitting a refund request.
- Human approval is required.
- No actual payment refund occurs in the MVP.

### 8.4 Tickets
- Ticket creation requires customer confirmation when initiated by AI.
- Ticket status changes must be validated.
- Internal notes are staff-only.
- Assignment history is retained.
- Ticket activity history is recorded.

### 8.5 Knowledge Base
- Only authorized staff can upload documents.
- Administrators and business owners can replace or delete documents.
- Agents may upload documents but cannot replace or delete them by default.
- Obsolete document chunks must not appear in retrieval results.
- Website ingestion must enforce SSRF protection.

### 8.6 Sensitive Verification
For sensitive account-security actions, the MVP uses password re-entry where appropriate.

OTP-based verification is deferred.

Refund approval relies on authenticated human authorization and audit logging. It is not delegated to the AI agent.

---

## 9. Business-Level Permission Summary

| Operation | Customer | Agent | Admin | Owner |
|---|---|---|---|---|
| View own orders | Yes | No by default | Yes | Yes |
| View assigned customer orders | No | Yes | Yes | Yes |
| Check refund eligibility | Own orders | Authorized | Yes | Yes |
| Submit refund request | Yes | On behalf, if authorized | Yes | Yes |
| Approve/reject refund | No | No | Yes | Yes |
| Create support ticket | Yes | Yes | Yes | Yes |
| View assigned tickets | No | Yes | Yes | Yes |
| Assign tickets | No | No by default | Yes | Yes |
| Add internal notes | No | Yes | Yes | Yes |
| Upload KB documents | No | Yes | Yes | Yes |
| Replace/delete KB documents | No | No by default | Yes | Yes |
| View audit logs | No | No | Yes | Yes |
| Manage users | No | No | Yes | Yes |
| View business analytics | No | Limited | Yes | Yes |

All permissions must be enforced by backend authorization logic.

---

## 10. Non-Functional Requirements

### 10.1 Performance

Initial provisional targets:

| Operation | Target |
|---|---|
| Normal API P95 | Below 500 ms |
| Database-backed API P95 | Below 500 ms |
| AI first-token P95 | Below 3 seconds |
| Complete AI response P95 | Below 10 seconds |
| Analytics API P95 | Below 2 seconds |
| Initial concurrent users | 10–50 |

These targets depend on infrastructure, model provider latency and data volume.

### 10.2 Security
- Secure password hashing.
- JWT access authentication.
- Refresh-token rotation.
- HttpOnly refresh-token cookie.
- CSRF protection where cookie authentication requires it.
- RBAC and resource-level authorization.
- Rate limiting.
- Secure file uploads.
- HTTPS.
- Secret management.
- Audit logging.
- Prompt-injection protection.
- SSRF protection for website ingestion.

### 10.3 Reliability
- Structured error handling.
- Database transactions.
- Durable background jobs.
- Retry handling for eligible failures.
- Idempotency for important mutating operations.
- Application logging.
- AI provider timeout handling.

### 10.4 Scalability
- Modular monolithic architecture initially.
- Business identifiers in the data model.
- Stateless API services where practical.
- Database indexes based on access patterns.
- Background workers for longer tasks.
- Future separation of services only when justified.

### 10.5 Usability
- Responsive web interface.
- Clear loading and error states.
- Simple customer chat.
- Accessible navigation.
- Role-specific dashboards.
- Clear source citations.
- Clear human-escalation process.

### 10.6 Language
- English is the MVP language.
- Hindi support is planned for the advanced phase.

---

## 11. Technology Direction

| Layer | Selected Technology |
|---|---|
| Programming language | Python |
| Backend | FastAPI |
| Frontend | React + TypeScript |
| Styling | Tailwind CSS |
| Database | PostgreSQL |
| Vector search | pgvector |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| LLM provider | OpenAI API |
| AI orchestration | LangChain |
| Advanced orchestration | LangGraph, later phase |
| API testing | Postman |
| Backend testing | Pytest |
| Frontend testing | Vitest + React Testing Library |
| E2E testing | Playwright |
| Performance testing | Locust |
| Version control | Git + GitHub |
| Containerization | Docker |

---

## 12. Assumptions and Constraints

### Assumptions
- One demo business is used initially.
- Mock data is available for customers, orders and products.
- External payment processing is not required for the MVP.
- Email notifications are simulated.
- The OpenAI API is available.
- Customers use a web application.
- Initial support operations are handled through a basic support dashboard.

### Constraints
- The project is intended for learning and portfolio demonstration.
- Development should prioritize free or low-cost services.
- AI API usage must be monitored.
- Implementation must be beginner-friendly and incremental.
- No coding begins before documentation approval.
- The initial schedule is estimated at 8–12 weeks, not guaranteed.

---

## 13. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| AI hallucination | Backend verification and RAG grounding |
| Unauthorized data access | RBAC, ownership checks and tenant isolation |
| Incorrect refund decision | Configured policy and backend eligibility rules |
| Prompt injection | Input and retrieved-content isolation |
| API cost | Usage limits and model selection |
| Retrieval quality | Hybrid retrieval and evaluation dataset |
| Integration complexity | Modular architecture and incremental testing |
| Project delays | Prioritize MVP and defer advanced features |
| Background task failure | Persistent job table and worker retries |
| Data retention issues | Explicit deletion and retention workflow |

---

## 14. MVP Acceptance Criteria

The MVP will be accepted when:

1. Customers can register and log in.
2. Role-based authorization works.
3. Customers can access only their own records.
4. Customers can view their orders.
5. Customers can retrieve available tracking information.
6. Customers can check product availability.
7. Customers can interact with the AI support agent.
8. The agent can retrieve knowledge-base information.
9. Responses include source citations where applicable.
10. Customers can check refund eligibility.
11. Refund requests require customer confirmation.
12. Refund approval requires authorized human action.
13. Actual payment refund processing is disabled.
14. Customers can submit cancellation requests.
15. Cancellation requests require review.
16. Customers can create support tickets.
17. Support agents can manage authorized tickets.
18. Internal notes remain private.
19. Human escalation works.
20. Administrators can manage knowledge-base documents.
21. Conversation history is stored.
22. In-app and simulated email notifications work.
23. Important actions are audit-logged.
24. Critical API, integration and security tests pass.

---

## 15. Out of Scope

The following are not part of the initial MVP:

- Real payment processing.
- Real refund transactions.
- Automatic order cancellation.
- Production-grade live chat infrastructure.
- Full production multi-tenant onboarding.
- Advanced multilingual support.
- Advanced sentiment prediction.
- Complex multi-agent orchestration.
- External e-commerce platform synchronization.
- Real email provider integration.

---

## 16. Delivery Approach

The project follows these stages:

1. Business requirements and documentation.
2. Documentation review and approval.
3. Environment setup.
4. Python fundamentals.
5. LangChain and LLM learning.
6. RAG implementation.
7. Tool integration.
8. Backend implementation.
9. Database integration.
10. Frontend development.
11. Frontend-backend integration.
12. Testing and security validation.
13. Deployment.
14. Final project demonstration.

Implementation begins only after all eight documents are reviewed and approved.

---

## 17. Document Status

This document is a revised business requirements baseline.

It must be reviewed alongside:
- Software Requirements Specification.
- Technical Architecture.
- Database Design.
- API Specification.
- Project Folder Structure.
- Development Roadmap.
- Testing Strategy.

**Status: Revised Draft — Pending Cross-Document Consistency Review and User Approval.**