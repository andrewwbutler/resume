{% extends "section.md" %}

{% block body %}
{{ text | wordwrap(width=80, wrapstring='\n')}}
{% endblock body %}
