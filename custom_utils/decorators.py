from django.http import HttpResponseRedirect

def redirect_if_logged(func):

	def if_logged(request, *args, **kwargs):
		if request.user.is_authenticated():
			return func(request, *args, **kwargs)
		return HttpResponseRedirect("/")

	return if_logged
