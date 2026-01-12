# ADR-001: Full-stack Monorepo Architecture

**Status:** Proposed
**Date:** 2026-01-03

## Context

The project requires implementing a full-stack web application for managing personal tasks with user authentication. The system needs to support complete CRUD operations for tasks with secure user authentication and authorization. We need to decide on the architectural approach for organizing the codebase - whether to use a monorepo with both frontend and backend in a single repository or separate repositories for each component.

The requirements include:
- Next.js 16+ frontend with App Router
- FastAPI backend with SQLModel
- PostgreSQL database
- JWT-based authentication
- Support for 100+ concurrent users
- API responses under 200ms p95
- Development hot reload under 3 seconds

## Decision

We will implement a full-stack monorepo architecture where both the frontend and backend code reside in a single repository. The structure will be:

- `frontend/`: Next.js 16+ App Router application with authentication and task management UI
- `backend/`: FastAPI application with SQLModel database models, Pydantic schemas, API routers, and middleware
- `docker-compose.yml`: Orchestrates PostgreSQL, backend, and frontend services for local development

This approach provides a clear separation of concerns while maintaining the benefits of a unified codebase.

## Alternatives

1. **Separate repositories (polyrepo)**: Frontend and backend in separate repositories
   - Pros: Independent deployment, separate team ownership, independent versioning
   - Cons: Complex coordination between services, harder to maintain consistency, more complex CI/CD

2. **Hybrid approach**: Shared libraries in separate repos, main app in monorepo
   - Pros: Some modularity while maintaining integration benefits
   - Cons: Still complex coordination, partial monorepo benefits

3. **Full integration**: All code in single tightly-coupled structure without clear separation
   - Pros: Maximum code sharing, single deployment unit
   - Cons: Technology lock-in, harder to scale teams, potential for tight coupling

## Consequences

**Positive:**
- Simplified development workflow: Single repository to clone, single environment to set up
- Easier coordination: Changes that span frontend/backend can be made in single commit/PR
- Consistent tooling: Shared linting, formatting, and development tools
- Faster iteration: Easier to make coordinated changes across frontend/backend
- Simplified dependency management: Shared configuration and environment setup
- Better for small-to-medium teams: Single codebase to understand and maintain

**Negative:**
- Repository bloat: Single repository grows larger with mixed technology stacks
- Potential for tight coupling: Risk of creating too many dependencies between frontend/backend
- Complex CI/CD: Single repository with multiple deployable units requires sophisticated pipeline
- Team scaling: As team grows, potential for conflicts increases
- Security considerations: Both frontend and backend in same repo may have different security requirements

## References

- [specs/001-task-crud-auth/plan.md](../specs/001-task-crud-auth/plan.md)
- [specs/001-task-crud-auth/spec.md](../specs/001-task-crud-auth/spec.md)
- [specs/001-task-crud-auth/data-model.md](../specs/001-task-crud-auth/data-model.md)