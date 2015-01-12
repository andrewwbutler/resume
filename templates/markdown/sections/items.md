{% extends "section.md" %}
{% block body %}

{% if title == 'Selected Coursework' %}
[Full Course List](/education/)
{% endif %}

{% if subsections %}
{% for subs in subsections %}
####{{ subs.name }}####
{% for item in subs.subitems %}
  - {{ item }}
{% endfor %}

{% endfor %}
{% else %}
{% for item in items %}
  - {{ item }}
{% endfor %}
{% endif %}

{% endblock body %}
