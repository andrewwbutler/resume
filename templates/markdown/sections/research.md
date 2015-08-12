{% extends "section.md" %}

{% block body %}
{% for r in items %}
**{{ r.topic }}** - {{ r.date }}  
{% if r.about is defined %}*{{ r.about }}*
{% endif %}

{% for note in r.notes %}
  - {{ note | wordwrap(width=76, wrapstring='\n    ') }}
{% endfor %}

{% endfor %}
{% endblock body %}
