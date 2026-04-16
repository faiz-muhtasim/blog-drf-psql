def format_post(post_obj, comments=None):
    data = {
        'id': post_obj.id,
        'title': post_obj.title,
        'description': post_obj.description,
        'status': post_obj.status,
        'user': format_user(post_obj.user),
    }
    if comments is not None:
        data['comments'] = comments
    return data

def format_user(user_obj):
    return {
        'id': user_obj.id,
        'username': user_obj.username,
        'email': user_obj.email,
    }

def format_comment(comment_obj):
    return {
        'id': comment_obj.id,
        'body': comment_obj.body,
        'created_at': comment_obj.created_at,
        'user': format_user(comment_obj.user),
    }