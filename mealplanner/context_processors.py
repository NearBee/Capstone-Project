from .forms import (
    user_registration_form,
    user_login_form,
    planner_creation_form,
    user_edit_form,
)
from .models import Planner


def multipage_information(request):

    if not request.user.is_authenticated:
        return {
            "user_registration_form": user_registration_form(),
            "user_login_form": user_login_form(),
            "planner_form": planner_creation_form(),
        }

    return {
        "user_registration_form": user_registration_form(),
        "user_login_form": user_login_form(),
        "user_edit_form": user_edit_form(),
        "planner_form": planner_creation_form(),
        "number_of_plans": len(Planner.objects.filter(owner=request.user)),
        "favorite_meals": request.user.favorite_dishes.all().count(),
    }
