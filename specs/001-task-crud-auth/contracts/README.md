# API Contracts

This directory contains OpenAPI 3.0 specifications for all API endpoints in the Task CRUD with Authentication application.

## Contract Files

### `auth.openapi.yaml`
- Authentication endpoints (registration, login)
- JWT token management
- User validation and security

### `tasks.openapi.yaml`
- Task CRUD operations (create, read, update, delete)
- User-specific task filtering
- Completion status toggling

## Contract Usage Guide

### Validation Rules
1. All endpoints require JWT authentication (except registration/login)
2. User data isolation: All task operations are filtered by user_id
3. Input validation through JSON schema
4. Proper HTTP status codes:
   - 200: Success for GET/PUT/DELETE operations
   - 201: Created for POST operations
   - 204: No Content for successful DELETE
   - 400: Bad Request for validation errors
   - 401: Unauthorized for invalid JWT
   - 404: Not Found for missing resources (or wrong user_id)

### Security Checklist
- [ ] All endpoints validate JWT token
- [ ] All task operations filter by user_id from JWT
- [ ] Return 404 (not 403) for unauthorized resource access
- [ ] Input validation prevents injection attacks
- [ ] Passwords are hashed before storage
- [ ] JWT tokens stored in httpOnly cookies

### Implementation Requirements
- Backend must implement all endpoints as specified
- Frontend must consume API according to contract
- Error responses must match schema
- Authentication must follow JWT/httpOnly cookie pattern
- Database queries must filter by user_id for security