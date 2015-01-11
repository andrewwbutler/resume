{% extends "section.md" %}
{% block body %}
{% for r in items %}
**{{ r.topic }}** - {{ r.date }}

{% for note in r.notes %}
  - {{ note }}
{% endfor %}

{% endfor %}
{% endblock body %}
