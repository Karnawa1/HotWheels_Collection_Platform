"""
Unit Tests for Authentication Service and Routes
Tests user registration, login, logout, and profile management
"""

import pytest
from app.services.auth_service import AuthService
from app.models.user import User


class TestAuthServiceRegistration:
    """Tests for user registration"""

    def test_register_user_success(self, app):
        """Test successful user registration"""
        with app.app_context():
            user, error = AuthService.register_user(
                username='newuser',
                email='newuser@example.com',
                password='SecurePass123',
                fullname='New User',
                country='USA'
            )
            
            assert user is not None
            assert error is None
            assert user.username == 'newuser'
            assert user.email == 'newuser@example.com'
            assert user.fullname == 'New User'
            assert user.isactive is True

    def test_register_user_duplicate_email(self, app, sample_user):
        """Test registration with duplicate email"""
        with app.app_context():
            user, error = AuthService.register_user(
                username='anotheruser',
                email='test@example.com',  # Same as sample_user
                password='SecurePass123'
            )
            
            assert user is None
            assert error is not None
            assert 'email' in error.lower() or 'already' in error.lower()

    def test_register_user_duplicate_username(self, app, sample_user):
        """Test registration with duplicate username"""
        with app.app_context():
            user, error = AuthService.register_user(
                username='testuser',  # Same as sample_user
                email='different@example.com',
                password='SecurePass123'
            )
            
            assert user is None
            assert error is not None
            assert 'username' in error.lower() or 'already' in error.lower()

    def test_register_user_invalid_email(self, app):
        """Test registration with invalid email"""
        with app.app_context():
            user, error = AuthService.register_user(
                username='validuser',
                email='invalid-email',
                password='SecurePass123'
            )
            
            assert user is None
            assert error is not None
            assert 'email' in error.lower()

    def test_register_user_weak_password(self, app):
        """Test registration with weak password"""
        with app.app_context():
            user, error = AuthService.register_user(
                username='validuser',
                email='valid@example.com',
                password='weak'  # Too short, no numbers
            )
            
            assert user is None
            assert error is not None

    def test_register_user_invalid_username(self, app):
        """Test registration with invalid username"""
        with app.app_context():
            user, error = AuthService.register_user(
                username='ab',  # Too short
                email='valid@example.com',
                password='SecurePass123'
            )
            
            assert user is None
            assert error is not None


class TestAuthServiceAuthentication:
    """Tests for user authentication"""

    def test_authenticate_success(self, app, sample_user):
        """Test successful authentication"""
        with app.app_context():
            result, error = AuthService.authenticate(
                email='test@example.com',
                password='TestPass123'
            )
            
            assert result is not None
            assert error is None
            assert 'accessToken' in result
            assert 'refreshToken' in result
            assert 'user' in result

    def test_authenticate_wrong_password(self, app, sample_user):
        """Test authentication with wrong password"""
        with app.app_context():
            result, error = AuthService.authenticate(
                email='test@example.com',
                password='WrongPassword123'
            )
            
            assert result is None
            assert error is not None
            assert 'invalid' in error.lower()

    def test_authenticate_nonexistent_email(self, app):
        """Test authentication with non-existent email"""
        with app.app_context():
            result, error = AuthService.authenticate(
                email='nonexistent@example.com',
                password='TestPass123'
            )
            
            assert result is None
            assert error is not None

    def test_authenticate_inactive_user(self, app, inactive_user):
        """Test authentication with inactive user"""
        with app.app_context():
            result, error = AuthService.authenticate(
                email='inactive@example.com',
                password='TestPass789'
            )
            
            assert result is None
            assert error is not None
            assert 'deactivated' in error.lower()


class TestAuthServiceLogout:
    """Tests for user logout"""

    def test_logout_success(self, app, sample_user):
        """Test successful logout"""
        with app.app_context():
            # First authenticate to create a session
            result, _ = AuthService.authenticate(
                email='test@example.com',
                password='TestPass123'
            )
            
            # Then logout
            success, error = AuthService.logout(
                user_id=sample_user.userid,
                token=result['accessToken']
            )
            
            assert success is True
            assert error is None


class TestAuthServiceGetUser:
    """Tests for getting user by ID"""

    def test_get_user_by_id_success(self, app, sample_user):
        """Test getting user by ID"""
        with app.app_context():
            user = AuthService.get_user_by_id(sample_user.userid)
            
            assert user is not None
            assert user.userid == sample_user.userid
            assert user.username == 'testuser'

    def test_get_user_by_id_not_found(self, app):
        """Test getting non-existent user"""
        with app.app_context():
            user = AuthService.get_user_by_id(99999)
            assert user is None

    def test_get_user_by_id_inactive(self, app, inactive_user):
        """Test getting inactive user returns None"""
        with app.app_context():
            user = AuthService.get_user_by_id(inactive_user.userid)
            assert user is None


class TestAuthServiceUpdateProfile:
    """Tests for profile updates"""

    def test_update_profile_success(self, app, sample_user):
        """Test successful profile update"""
        with app.app_context():
            user, error = AuthService.update_user_profile(
                user_id=sample_user.userid,
                fullname='Updated Name',
                country='Canada',
                city='Toronto',
                bio='Updated bio'
            )
            
            assert user is not None
            assert error is None
            assert user.fullname == 'Updated Name'
            assert user.country == 'Canada'

    def test_update_profile_user_not_found(self, app):
        """Test updating non-existent user profile"""
        with app.app_context():
            user, error = AuthService.update_user_profile(
                user_id=99999,
                fullname='Test'
            )
            
            assert user is None
            assert error is not None

    def test_update_profile_partial(self, app, sample_user):
        """Test partial profile update (only some fields)"""
        with app.app_context():
            original_country = sample_user.country
            
            user, error = AuthService.update_user_profile(
                user_id=sample_user.userid,
                fullname='Only Name Updated'
            )
            
            assert user is not None
            assert user.fullname == 'Only Name Updated'
            # Country should remain unchanged
            assert user.country == original_country


class TestAuthServiceChangePassword:
    """Tests for password changes"""

    def test_change_password_success(self, app, sample_user):
        """Test successful password change"""
        with app.app_context():
            success, error = AuthService.change_password(
                user_id=sample_user.userid,
                old_password='TestPass123',
                new_password='NewSecurePass456'
            )
            
            assert success is True
            assert error is None
            
            # Verify new password works
            result, _ = AuthService.authenticate(
                email='test@example.com',
                password='NewSecurePass456'
            )
            assert result is not None

    def test_change_password_wrong_old_password(self, app, sample_user):
        """Test password change with wrong old password"""
        with app.app_context():
            success, error = AuthService.change_password(
                user_id=sample_user.userid,
                old_password='WrongOldPassword',
                new_password='NewSecurePass456'
            )
            
            assert success is False
            assert error is not None
            assert 'incorrect' in error.lower()

    def test_change_password_weak_new_password(self, app, sample_user):
        """Test password change with weak new password"""
        with app.app_context():
            success, error = AuthService.change_password(
                user_id=sample_user.userid,
                old_password='TestPass123',
                new_password='weak'
            )
            
            assert success is False
            assert error is not None

    def test_change_password_user_not_found(self, app):
        """Test password change for non-existent user"""
        with app.app_context():
            success, error = AuthService.change_password(
                user_id=99999,
                old_password='OldPass123',
                new_password='NewPass456'
            )
            
            assert success is False
            assert error is not None


class TestUserModel:
    """Tests for User model methods"""

    def test_set_and_check_password(self, app):
        """Test password hashing and verification"""
        with app.app_context():
            user = User(username='pwtest', email='pwtest@example.com')
            user.set_password('MySecurePassword123')
            
            assert user.passwordhash is not None
            assert user.passwordhash != 'MySecurePassword123'  # Should be hashed
            assert user.check_password('MySecurePassword123') is True
            assert user.check_password('WrongPassword') is False

    def test_user_to_dict(self, app, sample_user):
        """Test user to_dict conversion"""
        with app.app_context():
            user_dict = sample_user.to_dict()
            
            assert user_dict['user_id'] == sample_user.userid
            assert user_dict['username'] == 'testuser'
            assert user_dict['full_name'] == 'Test User'
            assert user_dict['is_active'] is True
            assert 'password' not in user_dict
            assert 'passwordhash' not in user_dict

    def test_user_to_dict_with_sensitive(self, app, sample_user):
        """Test user to_dict with masked email"""
        with app.app_context():
            user_dict = sample_user.to_dict(include_sensitive=True)
            
            assert 'email' in user_dict
            assert '***' in user_dict['email']  # Email should be masked


class TestAuthRoutes:
    """Tests for authentication API routes"""

    def test_register_route_success(self, client):
        """Test register endpoint"""
        response = client.post('/api/v1/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert 'user' in data['data']

    def test_register_route_missing_fields(self, client):
        """Test register endpoint with missing fields"""
        response = client.post('/api/v1/auth/register', json={
            'username': 'newuser'
            # Missing email and password
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

    def test_login_route_success(self, client, sample_user):
        """Test login endpoint"""
        response = client.post('/api/v1/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPass123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'accessToken' in data['data']

    def test_login_route_invalid_credentials(self, client, sample_user):
        """Test login endpoint with invalid credentials"""
        response = client.post('/api/v1/auth/login', json={
            'email': 'test@example.com',
            'password': 'WrongPassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False

    def test_me_route_authenticated(self, client, sample_user, auth_headers):
        """Test get current user endpoint"""
        response = client.get('/api/v1/auth/me', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['user']['username'] == 'testuser'

    def test_me_route_unauthenticated(self, client):
        """Test get current user without authentication"""
        response = client.get('/api/v1/auth/me')
        
        assert response.status_code == 401

    def test_update_profile_route(self, client, sample_user, auth_headers):
        """Test update profile endpoint"""
        response = client.put('/api/v1/auth/me', 
            headers=auth_headers,
            json={'full_name': 'Updated Name'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_change_password_route(self, client, sample_user, auth_headers):
        """Test change password endpoint"""
        response = client.post('/api/v1/auth/change-password',
            headers=auth_headers,
            json={
                'old_password': 'TestPass123',
                'new_password': 'NewSecurePass456'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_logout_route(self, client, sample_user, auth_headers):
        """Test logout endpoint"""
        response = client.post('/api/v1/auth/logout', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

