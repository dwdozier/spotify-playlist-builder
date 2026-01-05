# Plan: Foundation & Security Hygiene

## Phase 1: Configuration & Environment Audit

- [x] Audit `config.py` against `.env` files.

- [x] Refactor `.env.example` to be the single source of truth for required keys.

- [x] Ensure `pydantic-settings` models enforce required fields in production mode.

- [x] Update documentation (README/SETUP) to reflect new env var structure.

## Phase 2: Session Security & Auth Guards (Frontend)

- [ ] Implement global Axios/Fetch interceptor for 401 handling.
- [ ] Create/Update the `ProtectedRoute` wrapper (or TanStack Router equivalent).
- [ ] Implement "Redirect to Login and Return" logic (saving `redirect_url` in query param or state).
- [ ] Verify `test_auth_flow.py` (E2E) covers session expiry/redirection.

## Phase 3: OAuth Scope Transparency

- [ ] Audit current Spotify scopes in `backend/app/core/providers/spotify.py`.
- [ ] Update `ServiceConnection` model (or API response) to include `scopes` list.
- [ ] Update "Relay Station" UI to display these scopes in a user-friendly way.
- [ ] Verify backend validates scopes upon connection.

## Phase 4: Verification

- [ ] Run full test suite (backend & frontend).
- [ ] Manual verification of Auth Redirect flow.
- [ ] Manual verification of Relay Station UI.
