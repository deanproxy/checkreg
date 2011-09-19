from django import template
import re

register = template.Library()

@register.simple_tag
def css(file):
	return '<link rel="stylesheet" type="text/css" href="/static/css/%s"/>' % file

@register.simple_tag
def js(file):
	return '<script src="/static/js/%s"></script>' % file

@register.simple_tag
def img(file):
	return '<img src="/static/images/%s"/>' % file

