import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a TestClient for API testing."""
    return TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_all_activities_returns_success(self, client):
        """Test that GET /activities returns all activities with correct structure."""
        # Arrange
        # (activities are already set up by the reset_activities fixture)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert "Chess Club" in activities
        assert "Programming Class" in activities


    def test_get_activities_contains_participant_info(self, client):
        """Test that each activity contains participant information."""
        # Arrange
        # (activities are already set up by the reset_activities fixture)

        # Act
        response = client.get("/activities")

        # Assert
        activities = response.json()
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
        assert "michael@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_student_success(self, client):
        """Test successful student signup for an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"


    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds the participant to the activities list."""
        # Arrange
        activity_name = "Gym Class"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        updated_activities = activities_response.json()

        # Assert
        assert response.status_code == 200
        assert email in updated_activities[activity_name]["participants"]


    def test_signup_activity_not_found(self, client):
        """Test signup fails when activity doesn't exist."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


    def test_signup_duplicate_registration(self, client):
        """Test that a student cannot signup twice for the same activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up for this activity"


    def test_signup_without_email_parameter(self, client):
        """Test signup fails when email parameter is missing."""
        # Arrange
        activity_name = "Tennis Club"

        # Act
        response = client.post(f"/activities/{activity_name}/signup")

        # Assert
        assert response.status_code == 422  # Unprocessable Entity


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_student_success(self, client):
        """Test successful student unregistration from an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the participant from the activities list."""
        # Arrange
        activity_name = "Drama Club"
        email = "lucas@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        updated_activities = activities_response.json()

        # Assert
        assert response.status_code == 200
        assert email not in updated_activities[activity_name]["participants"]


    def test_unregister_activity_not_found(self, client):
        """Test unregister fails when activity doesn't exist."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


    def test_unregister_student_not_registered(self, client):
        """Test unregister fails when student is not registered for the activity."""
        # Arrange
        activity_name = "Tennis Club"
        email = "student@mergington.edu"  # Not registered

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Student is not signed up for this activity"


    def test_unregister_without_email_parameter(self, client):
        """Test unregister fails when email parameter is missing."""
        # Arrange
        activity_name = "Programming Class"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup")

        # Assert
        assert response.status_code == 422  # Unprocessable Entity
