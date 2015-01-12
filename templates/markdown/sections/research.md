{% extends "section.md" %}
{% block body %}
{% for r in items %}
**{{ r.topic }}** - {{ r.date }}  
{% if r.advisor %}*Advisor: {{ r.advisor }}*{% endif %}


{% for note in r.notes %}
  - {{ note }}
{% endfor %}

{% endfor %}
{% endblock body %}
