from userauths.models import Profile, User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

"""
    class MyTokenObtainPairSerializer(TokenObtainPairSerializer):: This line creates a new token serializer called MyTokenObtainPairSerializer that is based on an existing one called TokenObtainPairSerializer. Think of it as customizing the way tokens work.
    @classmethod: This line indicates that the following function is a class method, which means it belongs to the class itself and not to an instance (object) of the class.
    def get_token(cls, user):: This is a function (or method) that gets called when we want to create a token for a user. The user is the person who's trying to access something on the website.
    token = super().get_token(user): Here, it's asking for a regular token from the original token serializer (the one it's based on). This regular token is like a key to enter the website.
    token['full_name'] = user.full_name, token['email'] = user.email, token['username'] = user.username: This code is customizing the token by adding extra information to it. For example, it's putting the user's full name, email, and username into the token. These are like special notes attached to the key.
    return token: Finally, the customized token is given back to the user. Now, when this token is used, it not only lets the user in but also carries their full name, email, and username as extra information, which the website can use as needed.
    """


# Define a custom serializer that inherits from TokenObtainPairSerializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    # Define a custom method to get the token for a user
    def get_token(cls, user):
        # Call the parent class's get_token method
        token = super().get_token(user)

        # Add custom claims to the token
        token["full_name"] = user.full_name
        token["email"] = user.email
        token["username"] = user.username
        try:
            token["vendor_id"] = user.vendor.id
        except:
            token["vendor_id"] = 0

        # ...

        # Return the token with custom claims
        return token


# Define a serializer for user registration, which inherits from serializers.ModelSerializer
class RegisterSerializer(serializers.ModelSerializer):
    # Define fields for the serializer, including password and password2
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        # Specify the model that this serializer is associated with
        model = User
        # Define the fields from the model that should be included in the serializer
        fields = ("full_name", "email", "phone", "password", "password2")

    def validate(self, attrs):
        # Define a validation method to check if the passwords match
        if attrs["password"] != attrs["password2"]:
            # Raise a validation error if the passwords don't match
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        # Return the validated attributes
        return attrs

    def create(self, validated_data):
        # Define a method to create a new user based on validated data
        user = User.objects.create(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            phone=validated_data["phone"],
        )
        email_username, mobile = user.email.split("@")
        user.username = email_username

        # Set the user's password based on the validated data
        user.set_password(validated_data["password"])
        user.save()

        # Return the created user
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


# def __init__(self, *args, **kwargs):
#     super(ProfileSerializer, self).__init__(*args, **kwargs)
#     # Customize serialization depth based on the request method.
#     request = self.context.get('request')
#     if request and request.method == 'POST':
#         # When creating a new product FAQ, set serialization depth to 0.
#         self.Meta.depth = 0
#     else:
#         # For other methods, set serialization depth to 3.
#         self.Meta.depth = 3
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user).data
        return response


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


# The data flow in your Django application involves several steps that bridge the frontend request with the backend logic, leading to the generation of a JWT token containing custom claims. Let me explain how this works, especially focusing on how the user data is accessed and added to the token.

# ### 1. **Frontend Request**
# When a user tries to log in, your frontend sends a POST request to the backend at the endpoint `user/token/` with the user's email and password.

# Example of the request:
# ```javascript
# const { data, status } = await axios.post('user/token/', {
#     email,
#     password,
# });
# ```

# ### 2. **Backend Receives the Request**
# The `MyTokenObtainPairView` is the view responsible for handling this request. This view is a subclass of `TokenObtainPairView`, and it uses the `MyTokenObtainPairSerializer` to process the request.

# ### 3. **Serializer Validates the User**
# When the request reaches the backend, the `MyTokenObtainPairSerializer` starts processing it.

# - **Authentication**: The `MyTokenObtainPairSerializer` (inherited from `TokenObtainPairSerializer`) first validates the email and password provided in the request. This is done using Django's built-in authentication system.

# - **User Lookup**: Internally, Django's authentication system fetches the user from the database using the provided email (because `USERNAME_FIELD` is set to `email` in your custom `User` model). The password is then checked against the stored hash in the database.

# ### 4. **Token Generation**
# Once the user is authenticated (i.e., the email and password are valid), the `get_token` method in `MyTokenObtainPairSerializer` is called.

# - **Calling Parent's `get_token` Method**:
#    ```python
#    token = super().get_token(user)
#    ```
#    This line calls the parent class's `get_token` method, which creates a basic JWT token for the user. The `user` object here is the authenticated user instance that was retrieved based on the provided email and password.

# - **Adding Custom Claims**:
#    After generating the basic token, the code adds custom claims like `full_name`, `email`, `username`, and `vendor_id` to the token:
#    ```python
#    token['full_name'] = user.full_name
#    token['email'] = user.email
#    token['username'] = user.username
#    ```
#    These fields are accessed directly from the `user` object, which represents the authenticated user.

#    For `vendor_id`, the code attempts to access the related `vendor` object:
#    ```python
#    try:
#        token['vendor_id'] = user.vendor.id
#    except:
#        token['vendor_id'] = 0
#    ```
#    This tries to add the `vendor_id` if the user has an associated vendor. If not, it defaults to `0`.

# ### 5. **Returning the Token**
# The token, now enriched with the custom claims, is returned to the frontend as part of the response to the POST request. The frontend can then use this token for authenticating future requests.

# ### Summary of the Data Flow:
# 1. **Frontend sends email and password**: These credentials are sent in a POST request to the backend.
# 2. **Backend authenticates the user**: The backend uses Django's authentication system to validate the credentials and retrieve the user object.
# 3. **Token generation with custom claims**: The backend generates a JWT token and adds additional user information (custom claims) to the token using the `MyTokenObtainPairSerializer`.
# 4. **Token returned to the frontend**: The generated token, containing the email, full name, username, and vendor ID (if applicable), is sent back to the frontend.

# The key point is that the `user` object, which is accessed in the `get_token` method, is derived from the email and password provided by the frontend. Once the user is authenticated, the full user object, including all its fields, is available for generating the token with custom claims.
