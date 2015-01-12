{% extends "section.md" %}

{% block body %}
{% for r in items %}
**{{ r.topic }}** - {{ r.date }}  
{% if r.about %}*{{ r.about }}*
{% endif %}

{% for note in r.notes %}
  - {{ note | wordwrap(wrapstring='\n    ') }}
{% endfor %}

{% endfor %}
{% endblock body %}
