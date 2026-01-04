# Spec: Stabilize Core Functionality and MVP Release

## Goal

To ensure the current Vibomat application is fully functional, reliable, and ready for a public
v1.0 MVP release.

## Core Objectives

1. **API Reliability:** Audit all FastAPI endpoints to ensure they handle errors gracefully and
    return correct data.
2. **Spotify Relay:** Fix any issues with Spotify OAuth and playlist creation/synchronization.
3. **AI Generation:** Verify the Gemini SDK integration and prompt engineering for high-quality
    playlist results.
4. **Metadata Verification:** Ensure MusicBrainz/Discogs integration correctly verifies track
    information to prevent hallucinations.
5. **Frontend Consistency:** Resolve UI/UX issues in the React frontend, ensuring the "Digital
    Automat" theme is consistently applied.
6. **Deployment Readiness:** Ensure Docker configurations are optimized for production.

## Success Criteria

- [ ] 100% of core unit tests passing.
- [ ] End-to-end "Citizen" journey (Login -> Build Archive -> Sync to Spotify) is successful
    without errors.
- [ ] UI reflects the approved Art Deco / Automat design guidelines.
- [ ] Documentation (README, SETUP) is accurate and complete for first-time users.
