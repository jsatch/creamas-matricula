from django import template

register = template.Library()

@register.filter
def substract(value, arg):
	return value - arg

@register.filter
def porcentaje(value, arg):
	porcentaje =  float(arg)/float(value)
	if porcentaje >= 0.8:
		return "red"
	elif porcentaje >= 0.5:
		return "yellow"
	elif porcentaje >= 0.1:
		return "green"
	else:
		return "transparent"