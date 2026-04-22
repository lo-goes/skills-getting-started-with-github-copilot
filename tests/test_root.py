import pytest
from fastapi.testclient import TestClient
from src.app import app


class TestRootEndpoint:
    """Tests for GET / endpoint."""

    def test_root_redirects_to_index(self, client):
        """Test that GET / redirects to /static/index.html."""
        # Arrange
        # (TestClient is set up and ready)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"


    def test_root_redirect_is_temporary(self, client):
        """Test that the redirect is a temporary redirect (307) not permanent (301)."""
        # Arrange
        # (TestClient is set up and ready)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
