{% extends "section.md" %}

{% block body %}
{% for pub in items %}
"{{ pub.title }}."
{{ pub.authors }}.
{{ pub.venuetype }} {{ pub.venue }}, {{ pub.month }} {{ pub.year }}.

{% endfor %}
{% endblock body %}
