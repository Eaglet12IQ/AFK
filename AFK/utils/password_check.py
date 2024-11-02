import regex as re
from django.http import JsonResponse

def password_check(password):
    if len(password) < 8:
        return JsonResponse({"message": "Пароль содержит менее 8 символов."}, status=400)
    
    if not re.search(r'\p{Lu}', password):
        return JsonResponse({"message": "Пароль не содержит хотя бы одну заглавную букву."}, status=400)
    
    if not re.search(r'\p{Nd}', password):
        return JsonResponse({"message": "Пароль не содержит хотя бы одну цифру."}, status=400)
    
    if not re.search(r'[^\w\s]', password):
        return JsonResponse({"message": "Пароль не содержит хотя бы один специальный символ."}, status=400)
    
    return False