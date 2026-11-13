# 08 — Testing Strategy

## 1. Document Information

| Field | Details |
|---|---|
| Project | AI-Powered E-commerce Customer Support Agent |
| Document | Testing Strategy |
| Version | 1.0 |
| Status | Proposed |
| Backend | Python + FastAPI |
| Frontend | React + TypeScript |
| Database | PostgreSQL + pgvector |
| AI Framework | LangChain |
| API Testing | Postman |
| Backend Testing | Pytest |
| Frontend Testing | Vitest + React Testing Library |
| End-to-End Testing | Playwright |

---

## 2. Purpose

The purpose of this document is to establish a systematic testing approach to ensure that the application is reliable, secure, accurate, and ready for deployment.

Testing will cover:

- Backend APIs.
- Frontend components.
- Database operations.
- Authentication and authorization.
- AI-generated responses.
- RAG retrieval quality.
- Agent tool execution.
- Business workflows.
- Security.
- Performance.
- End-to-end application behavior.

The objective is to identify defects early rather than waiting until the entire application has been developed.

---

## 3. Testing Objectives

1. Verify that every functional requirement works correctly.
2. Ensure APIs return the expected responses.
3. Validate database relationships and data integrity.
4. Prevent unauthorized access to customer information.
5. Ensure AI responses are grounded in reliable information.
6. Verify that agent tools execute only authorized operations.
7. Ensure sensitive operations require appropriate confirmation.
8. Validate the complete customer support workflow.
9. Identify performance bottlenecks.
10. Verify application stability before deployment.

---

## 4. Testing Levels

The project will follow a layered testing approach.

### 4.1 Unit Testing

Unit testing verifies individual functions, classes, and components independently.

Examples:
- Password hashing.
- JWT token validation.
- Order eligibility calculation.
- Refund eligibility calculation.
- Ticket status validation.
- Text chunking.
- Retrieval ranking.
- Input validation.

Tools:
- Pytest for Python.
- Vitest for frontend components.

Acceptance criteria:
- Important business logic has unit tests.
- Expected and invalid inputs are tested.
- Tests execute independently.
- Failures identify the affected function or module.

### 4.2 Integration Testing

Integration testing verifies that different modules work together.

Examples:
- FastAPI connected to PostgreSQL.
- Authentication connected to the user repository.
- Order service connected to order and customer tables.
- RAG retrieval connected to pgvector.
- Agent tools connected to backend services.
- Frontend connected to backend APIs.

Acceptance criteria:
- Modules exchange data correctly.
- Database transactions behave correctly.
- Errors are handled across module boundaries.
- Authorization is preserved during integration.

### 4.3 API Testing

API testing verifies the behavior of REST endpoints.

Primary tool: Postman.

Each API will be tested for:
- Correct HTTP method.
- Correct endpoint.
- Valid request body.
- Required headers.
- Authentication.
- Authorization.
- Response status.
- Response structure.
- Validation errors.
- Database changes.
- Edge cases.

Acceptance criteria:
- Every implemented endpoint has documented test cases.
- Successful and unsuccessful scenarios are tested.
- Protected endpoints reject unauthenticated requests.
- Role restrictions are enforced.

### 4.4 System Testing

System testing validates the complete application after all major modules have been integrated.

Examples:
- Customer registration to AI chat.
- Order lookup through the chat interface.
- Knowledge-base upload to RAG-based response.
- Ticket creation and support-agent assignment.
- Refund eligibility and approval workflow.

Acceptance criteria:
- Complete workflows function as specified.
- Data remains consistent across modules.
- Critical failures are handled without crashing the application.

### 4.5 End-to-End Testing

End-to-end testing validates user journeys through the actual frontend.

Tool: Playwright.

Example scenarios:
- Customer logs in.
- Customer opens the chat.
- Customer asks about an order.
- Agent retrieves the verified order status.
- Customer creates a support ticket.
- Support agent updates the ticket.
- Customer views the updated ticket.

Acceptance criteria:
- Critical user journeys complete successfully.
- UI and backend state remain consistent.
- Important error and loading states behave correctly.

---

## 5. Functional Test Scenarios

### 5.1 Authentication Testing

| Test ID | Scenario | Expected Result |
|---|---|---|
| AUTH-01 | Register with valid details | Account created |
| AUTH-02 | Register with existing email | Duplicate account rejected |
| AUTH-03 | Login with valid credentials | Authentication successful |
| AUTH-04 | Login with incorrect password | Authentication rejected |
| AUTH-05 | Access protected API without token | 401 Unauthorized |
| AUTH-06 | Access API with expired token | Authentication rejected |
| AUTH-07 | Refresh access token | New access token issued |
| AUTH-08 | Reuse revoked refresh token | Request rejected |
| AUTH-09 | Logout | Refresh token revoked |
| AUTH-10 | Access restricted admin endpoint as customer | 403 Forbidden |

### 5.2 Customer and Order Testing

| Test ID | Scenario | Expected Result |
|---|---|---|
| ORD-01 | View own orders | Own orders returned |
| ORD-02 | View another customer's order | Access denied |
| ORD-03 | Search using valid order ID | Correct order returned |
| ORD-04 | Search using invalid order ID | Appropriate not-found response |
| ORD-05 | Search using another customer's order ID | No data disclosure |
| ORD-06 | Check product availability | Verified inventory result |
| ORD-07 | Request invalid pagination | Validation error |

### 5.3 Refund Testing

| Test ID | Scenario | Expected Result |
|---|---|---|
| REF-01 | Check eligible order | Eligible result |
| REF-02 | Check expired return window | Ineligible result |
| REF-03 | Check already refunded order | Duplicate refund prevented |
| REF-04 | Check another customer's order | Access denied |
| REF-05 | Customer requests refund | Confirmation and eligibility workflow |
| REF-06 | Agent attempts unauthorized approval | Access denied |
| REF-07 | Authorized human approves refund | Approval recorded |
| REF-08 | Actual payment processing requested in MVP | No real payment operation executed |

### 5.4 Support Ticket Testing

| Test ID | Scenario | Expected Result |
|---|---|---|
| TKT-01 | Create ticket with valid data | Ticket created |
| TKT-02 | Create ticket with missing fields | Validation error |
| TKT-03 | View own ticket | Ticket details returned |
| TKT-04 | View another customer's ticket | Access denied |
| TKT-05 | Assign ticket | Assignment recorded |
| TKT-06 | Update ticket status | Status updated |
| TKT-07 | Add internal note | Note visible only to authorized staff |
| TKT-08 | Escalate ticket | Escalation recorded |
| TKT-09 | Reopen resolved ticket | Ticket reopened if permitted |

### 5.5 Knowledge-Base Testing

| Test ID | Scenario | Expected Result |
|---|---|---|
| KB-01 | Upload valid PDF | Document accepted |
| KB-02 | Upload valid TXT | Document accepted |
| KB-03 | Upload valid DOCX | Document accepted |
| KB-04 | Upload valid CSV/XLSX | Supported content processed |
| KB-05 | Upload unsupported file | Request rejected |
| KB-06 | Upload oversized file | Request rejected |
| KB-07 | Upload document as customer | Access denied |
| KB-08 | Replace document | Old chunks replaced |
| KB-09 | Delete document | Associated chunks removed or made unavailable |
| KB-10 | Query indexed document | Relevant content retrieved |
| KB-11 | Query deleted document | Deleted content not retrieved |

---

## 6. AI and RAG Testing

AI systems require additional testing because an API can return a successful response while the generated answer is still incorrect.

### 6.1 LLM Response Testing

Test scenarios:
- Normal customer question.
- Ambiguous question.
- Incomplete question.
- Unsupported question.
- Irrelevant question.
- Long customer message.
- Hindi question.
- English question.
- Prompt-injection attempt.
- Provider timeout.
- Invalid structured output.

Expected behavior:
- Responses are relevant and understandable.
- The agent asks clarifying questions when required.
- Unsupported claims are avoided.
- Business facts are verified through backend services.
- Errors are handled safely.

### 6.2 RAG Pipeline Testing

Test the complete pipeline:

1. Document upload.
2. Text extraction.
3. Text cleaning.
4. Chunk generation.
5. Embedding generation.
6. Vector storage.
7. Keyword indexing.
8. Query embedding.
9. Hybrid retrieval.
10. Context construction.
11. LLM response generation.
12. Citation generation.

Example test:

**Input question:** What is the return period?

**Knowledge-base content:** Customers can request returns within 7 days of delivery, subject to the published return conditions.

**Expected result:** The assistant should answer using the retrieved policy and provide the correct source citation.

### 6.3 RAG Quality Metrics

| Metric | Purpose |
|---|---|
| Recall@K | Measures whether relevant chunks appear in the top K results |
| Precision@K | Measures how many retrieved chunks are relevant |
| MRR | Measures the rank of the first relevant result |
| Faithfulness | Measures whether the answer is supported by retrieved context |
| Answer Relevance | Measures whether the answer addresses the question |
| Citation Accuracy | Measures whether citations point to supporting sources |

These metrics will be evaluated using a manually prepared question-and-answer dataset.

### 6.4 AI Hallucination Testing

Test cases:
- Ask for an order that does not exist.
- Ask for a refund amount not available in the database.
- Ask about a product that is not in the catalog.
- Ask about a policy not present in the knowledge base.
- Ask the agent to invent tracking information.

Expected result:
- The agent must not invent business information.
- The agent must state when information cannot be verified.
- The agent must offer clarification or human support where appropriate.

### 6.5 Agent Tool Testing

| Tool | Test | Expected Result |
|---|---|---|
| Order Lookup | Valid authorized order | Verified order information |
| Order Lookup | Unauthorized order | Access denied |
| Product Availability | Existing product | Verified availability |
| Refund Eligibility | Eligible order | Eligibility result |
| Ticket Creation | Valid confirmed request | Ticket created |
| Customer Information | Authorized request | Permitted information returned |
| Complaint Classification | Complaint message | Classification returned |
| KB Retrieval | Relevant query | Relevant documents returned |
| Email Simulation | Valid notification | Notification record created |
| Human Escalation | Unresolved issue | Escalation workflow initiated |

The LLM must not bypass the validation rules implemented in backend services.

---

## 7. Security Testing

Security testing is mandatory because the application stores customer information and handles order-related operations.

### 7.1 Authentication Security
- Password hashing verification.
- Invalid JWT rejection.
- Expired token rejection.
- Refresh-token rotation.
- Refresh-token reuse detection.
- Logout and token revocation.

### 7.2 Authorization Security
- Customer cannot access another customer's records.
- Support agents cannot perform administrator-only actions.
- Administrators cannot bypass explicitly restricted approval workflows.
- Customers cannot upload or delete knowledge-base documents.
- Internal notes are not visible to customers.

### 7.3 Application Security
- SQL injection testing.
- Cross-site scripting testing.
- Cross-site request forgery protections where applicable.
- Rate-limiting tests.
- File upload validation.
- File type and size restrictions.
- Secure error responses.
- Secret management checks.
- HTTPS verification.

### 7.4 AI Security
- Prompt-injection testing.
- Sensitive-data disclosure testing.
- Unauthorized tool invocation.
- Malicious document content testing.
- Retrieved-content instruction isolation.
- Customer data leakage between conversations.
- Output validation before business operations.

### 7.5 Website Ingestion Security

Website ingestion must be tested against Server-Side Request Forgery (SSRF).

Controls:
- Allow only HTTP and HTTPS.
- Block localhost and private network addresses.
- Restrict redirect destinations.
- Restrict allowed domains where appropriate.
- Apply request timeouts and response-size limits.
- Reject dangerous or unsupported URL schemes.

---

## 8. Performance Testing

Performance testing checks whether the system meets its initial non-functional requirements.

Initial provisional targets:

| Operation | Target |
|---|---|
| Normal API response | P95 below 500 ms |
| Database-backed API | P95 below 500 ms |
| AI first-token latency | P95 below 3 seconds |
| Complete AI response | P95 below 10 seconds |
| Analytics API | P95 below 2 seconds |
| Initial concurrent users | 10–50 |

These are engineering targets, not guarantees. AI provider latency, network conditions, query complexity, and hosting resources affect actual results.

Testing scenarios:
- Multiple users logging in simultaneously.
- Multiple customers requesting order status.
- Concurrent chat requests.
- Multiple document uploads.
- Concurrent ticket creation.
- Database query load.
- Large conversation histories.

Possible tools:
- Locust for backend load testing.
- Browser performance tools for frontend analysis.
- Application and database monitoring.

---

## 9. Frontend Testing

Frontend testing will cover:

### Component Testing
- Login forms.
- Registration forms.
- Chat components.
- Message rendering.
- Order cards.
- Ticket cards.
- Admin upload forms.
- Dashboard charts.

### UI Behavior Testing
- Form validation.
- Loading states.
- Error states.
- Empty states.
- Responsive layout.
- Navigation.
- Protected routes.
- Role-specific screens.
- Accessibility basics.

### Chat Interface Testing
- Send message.
- Display assistant response.
- Display source citations.
- Display typing/loading state.
- Load previous conversations.
- Handle API failures.
- Display tool-action confirmation.
- Display ticket creation confirmation.

---

## 10. Test Environments

| Environment | Purpose |
|---|---|
| Local Development | Initial implementation and debugging |
| Test Environment | Automated and integration testing |
| Staging | Deployment-like validation |
| Production | Actual deployed application |

Development and testing must use mock or test data.

Production customer data must not be copied into local development environments without an explicitly approved and secure process.

---

## 11. Test Data Strategy

Initial testing will use realistic mock data.

Example records:
- 10 customers.
- 20 products.
- 30 orders.
- 10 support tickets.
- 5 refund records.
- 10 knowledge-base documents.
- Sample conversations.

Test data should include:
- Valid records.
- Invalid records.
- Missing fields.
- Duplicate values.
- Expired orders.
- Refunded orders.
- Different customer ownership.
- Different user roles.
- Documents with relevant and irrelevant information.

Sensitive personal data must not be used in mock datasets.

---

## 12. Test Execution Workflow

Every feature will follow this process:

1. Understand the requirement.
2. Identify test scenarios.
3. Prepare test data.
4. Implement the feature.
5. Execute unit tests.
6. Execute API tests in Postman.
7. Verify database changes.
8. Execute integration tests.
9. Fix defects.
10. Re-run failed tests.
11. Update test documentation.
12. Mark the feature complete.

No major feature should be considered complete merely because its endpoint returns HTTP 200.

---

## 13. Defect Management

Defects will be classified according to severity.

| Severity | Description | Example |
|---|---|---|
| Critical | Application or security failure | Customer can access another customer's order |
| High | Major business workflow broken | Ticket creation fails |
| Medium | Partial functionality issue | Incorrect pagination |
| Low | Minor UI or usability issue | Misaligned button |

Defect workflow:

- New
- Assigned
- In Progress
- Fixed
- Retest
- Closed

A defect is closed only after the fix has been verified.

Critical security defects must be resolved before deployment.

---

## 14. Testing Deliverables

The project should maintain:

1. Unit test files.
2. Integration test files.
3. Postman collection.
4. Postman environment configuration.
5. RAG evaluation dataset.
6. AI evaluation results.
7. Security test checklist.
8. Performance test results.
9. End-to-end test scripts.
10. Defect tracking log.
11. Final test execution report.

---

## 15. Definition of Done

A feature is considered complete only when:

- Its requirements are implemented.
- Input validation is implemented.
- Authentication and authorization are checked.
- Unit tests pass.
- Relevant API tests pass.
- Database behavior is verified.
- Error handling is implemented.
- Logging is available where appropriate.
- Documentation is updated.
- No unresolved critical defect remains.

---

## 16. Final MVP Acceptance Criteria

The MVP is ready for final review when:

- Customer registration and login work.
- JWT authentication and RBAC work.
- Customers can access only their own data.
- Order lookup returns verified information.
- Product availability is retrieved from the backend.
- Customers can ask questions through the AI chat.
- RAG answers use indexed knowledge-base documents.
- Relevant source citations are displayed.
- Refund eligibility is checked correctly.
- Actual refund processing is not performed in the MVP.
- Customers can create support tickets.
- Support agents can manage tickets.
- Human escalation works.
- Admins can manage knowledge-base documents.
- Conversation history is persisted.
- Critical security tests pass.
- Critical end-to-end workflows pass.
- Deployment and execution instructions are documented.

---

## 17. Future Testing Enhancements

After the MVP, testing can be expanded to include:

- Automated LLM evaluation pipelines.
- Multilingual response evaluation.
- Advanced RAG benchmarking.
- Red-team testing for AI agents.
- Continuous integration and deployment.
- Automated accessibility testing.
- Advanced load and stress testing.
- Multi-tenant isolation testing.
- Real payment-provider sandbox testing.

---

## 18. Final Note

Testing is a continuous activity throughout development, not a final step performed only before deployment.

The development process must include testing at every milestone. The project should prioritize correctness, security, data integrity, and reliable AI behavior over adding features quickly.