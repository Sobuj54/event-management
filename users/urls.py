from django.urls import path
from users.views import sign_up, sign_in, activate_user, sign_out, ProfileView, EditProfileView, ChangePassword
from django.contrib.auth.views import PasswordChangeDoneView

app_name = "users"

urlpatterns = [
    path("sign-up/", sign_up, name="sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    path("sign-out/", sign_out, name="sign-out"),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    path("profile/",ProfileView.as_view(), name="profile"),
    path("edit-profile/", EditProfileView.as_view(), name="edit-profile"),
    path("password-change/", ChangePassword.as_view(), name="password-change"),
    path("password-change/done/", PasswordChangeDoneView.as_view(template_name="accounts/password-change-done.html"), name="password-change-done")
]