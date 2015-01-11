{% extends "section.md" %}
{% block body %}
{% for job in items %}
**{{ job.employer }}, {{ job.location }}** - _{{ job.role }}_ - {{ job.date }}

{% for note in job.notes %}
  - {{ note }}
{% endfor %}

{% endfor %}
{% endblock body %}
