"""
Tests for the Mergington High School Activities API

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and conditions
- Act: Perform the action being tested
- Assert: Verify the results
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Verify GET /activities returns all activities with correct structure"""
        # Arrange
        # (no setup needed - testing default state)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        assert isinstance(activities, dict)
        assert len(activities) > 0
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_includes_chess_club(self, client):
        """Verify Chess Club activity is in the response"""
        # Arrange
        # (no setup needed - Chess Club exists by default)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert "Chess Club" in activities
        assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert len(activities["Chess Club"]["participants"]) >= 0


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client):
        """Successfully sign up a student for an activity"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity in result["message"]

    def test_signup_adds_participant_to_list(self, client):
        """Verify participant is actually added to the activity"""
        # Arrange
        email = "athlete@mergington.edu"
        activity = "Basketball Team"
        
        # Act
        client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email in activities[activity]["participants"]

    def test_signup_activity_not_found(self, client):
        """Attempting to sign up for non-existent activity returns 404"""
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]

    def test_signup_already_registered(self, client):
        """Attempting to sign up twice for same activity returns 400"""
        # Arrange
        email = "michael@mergington.edu"  # Already registered in Chess Club
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "Already signed up" in result["detail"]

    def test_signup_different_activities_allowed(self, client):
        """Student can sign up for multiple different activities"""
        # Arrange
        email = "multitalent@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Art Club"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_signup_multiple_students_same_activity(self, client):
        """Multiple students can sign up for the same activity"""
        # Arrange
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]
        activity = "Science Club"
        
        # Act
        responses = []
        for email in emails:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            responses.append(response)
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        for response in responses:
            assert response.status_code == 200
        for email in emails:
            assert email in activities[activity]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successful(self, client):
        """Successfully unregister a student from an activity"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity in result["message"]

    def test_unregister_removes_participant(self, client):
        """Verify participant is actually removed from the activity"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Act - verify initial state
        response_before = client.get("/activities")
        activities_before = response_before.json()
        initial_participant_count = len(activities_before[activity]["participants"])
        
        # Act - unregister
        client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        response_after = client.get("/activities")
        activities_after = response_after.json()
        assert email not in activities_after[activity]["participants"]
        assert len(activities_after[activity]["participants"]) == initial_participant_count - 1

    def test_unregister_activity_not_found(self, client):
        """Attempting to unregister from non-existent activity returns 404"""
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404

    def test_unregister_not_registered(self, client):
        """Attempting to unregister someone not registered returns 404"""
        # Arrange
        email = "notregistered@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not registered" in result["detail"]

    def test_unregister_then_can_signup_again(self, client):
        """After unregistering, student can sign up again"""
        # Arrange
        email = "flexible@mergington.edu"
        activity = "Drama Club"
        
        # Act - sign up
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Act - unregister
        response2 = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Act - sign up again
        response3 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200


class TestRootRedirect:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_index(self, client):
        """Verify GET / redirects to /static/index.html"""
        # Arrange
        # (no setup needed)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestIntegrationScenarios:
    """Integration tests simulating real user workflows"""

    def test_complete_signup_unregister_flow(self, client):
        """Test complete flow: signup → verify → unregister → verify"""
        # Arrange
        email = "testuser@mergington.edu"
        activity = "Debate Club"
        
        # Act - sign up
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert - signup succeeded
        assert signup_response.status_code == 200
        
        # Act - verify signup
        get_response = client.get("/activities")
        activities = get_response.json()
        
        # Assert - user is in participant list
        assert email in activities[activity]["participants"]
        
        # Act - unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert - unregister succeeded
        assert unregister_response.status_code == 200
        
        # Act - verify unregister
        final_response = client.get("/activities")
        activities = final_response.json()
        
        # Assert - user is no longer in participant list
        assert email not in activities[activity]["participants"]

    def test_participant_count_accuracy(self, client):
        """Verify participant counts remain accurate through operations"""
        # Arrange
        new_email = "newmember@mergington.edu"
        activity = "Soccer Club"
        
        get_response = client.get("/activities")
        activities = client.get("/activities").json()
        initial_counts = {name: len(data["participants"]) for name, data in activities.items()}
        
        # Act - sign up new participant
        client.post(
            f"/activities/{activity}/signup",
            params={"email": new_email}
        )
        
        # Assert - verify counts
        response = client.get("/activities")
        activities = response.json()
        
        for name, data in activities.items():
            current_count = len(data["participants"])
            if name == activity:
                assert current_count == initial_counts[name] + 1, f"{activity} count should increase by 1"
            else:
                assert current_count == initial_counts[name], f"{name} count should not change"
