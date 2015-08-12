{% extends "section.md" %}

{% block body %}
{% for school in items %}
**{{ school.school }}** - _{{ school.date }}_  
{{ school.major }}  
{% if school.gpa is defined %}GPA: **{{ school.gpa }}**{% endif %}

{% endfor %}
{% endblock body %}
