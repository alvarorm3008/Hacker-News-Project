from ASWproject.utils import calculate_karma
def karma_processor(request):
    if request.user.is_authenticated:
        karma = calculate_karma(request.user)
    else:
        karma = 1
    return {'karma': karma}