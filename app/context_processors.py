# context_processors.py
def user_has_subrole(request):
    return {
        'has_view_all_users_subrole': request.user.has_subrole('view all users')
    }
