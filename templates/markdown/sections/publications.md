{% extends "section.md" %}

{% block body %}
{% for pub in items %}
"{{ pub.title }}."
{{ pub.authors }}.
{{ pub.journal }}, {{ pub.ref }} {{ pub.year }}.

{% endfor %}
{% endblock body %}
