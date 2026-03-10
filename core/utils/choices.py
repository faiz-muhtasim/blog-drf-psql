POST_DRAFT = "draft"
POST_PUBLISHED = "published"

POST_STATUS_CHOICES = [
    (POST_DRAFT, "Draft"),
    (POST_PUBLISHED, "Published"),
]

TASK_TYPE_CHOICES = [
    ("activate_account", "Activate Account"),
    ("reset_password", "Reset Password"),
]