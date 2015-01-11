{% extends "section.md" %}
{% block body %}

{% if title == 'Selected Coursework' %}
[Full Course List](/education/)
{% endif %}

{% for item in items %}
  - {{ item }}
{% endfor %}
{% endblock body %}
