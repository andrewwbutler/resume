{% extends "section.md" %}

{% block body %}
{% for item in items %}
**{{ item.title }}** 
{{item.institution}} - {{item.date}} 
{% if item.about is defined %}*{{ item.about }}*
{% endif %}

{% for note in item.notes %}
  - {{ note | wordwrap(width=76, wrapstring='\n    ') }}
{% endfor %}

{% endfor %}
{% endblock body %}

