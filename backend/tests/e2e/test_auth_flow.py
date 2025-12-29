import pytest
from playwright.sync_api import Page, expect


@pytest.mark.skip(reason="Requires running frontend and backend servers")
def test_navigation_to_login(page: Page):
    """Test that a user can navigate from the home page to the login page."""
    base_url = "http://localhost:5173"
    page.goto(base_url)

    expect(page.get_by_text("Welcome to Playlist Builder")).to_be_visible()

    page.get_by_role("link", name="Login").click()
    expect(page.get_by_text("Welcome back")).to_be_visible()


@pytest.mark.skip(reason="Requires running frontend and backend servers")
def test_playlist_generation_flow(page: Page):
    """Critical User Journey: Generate a playlist from a prompt."""
    base_url = "http://localhost:5173"
    page.goto(f"{base_url}/playlists")

    # Fill prompt
    prompt_input = page.get_by_placeholder("e.g. Late night synthwave coding session")
    prompt_input.fill("80s synthwave for late night coding")

    # Click generate
    page.get_by_role("button", name="Generate Playlist").click()

    # Wait for review table
    expect(page.get_by_text("Review Generated Tracks")).to_be_visible(timeout=30000)

    # Check if table has at least one row
    expect(page.locator("table tbody tr")).to_have_count(1, timeout=5000)

    # Verify we see the Save button
    expect(page.get_by_role("button", name="Save to My Playlists")).to_be_visible()
