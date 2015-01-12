{% extends "section.md" %}
{% block body %}
{% for job in items %}
**{{ job.employer }}{% if job.location %}, {{ job.location }}{% endif %}** - _{{ job.role }}_ - {{ job.date }}

{% for note in job.notes %}
  - {{ note }}
{% endfor %}

{% endfor %}
{% endblock body %}
