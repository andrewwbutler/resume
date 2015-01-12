{% extends "section.md" %}

{% block body %}
{% for school in items %}
**{{ school.school }}** - _{{ school.date }}_  
{{ school.major }}  
GPA: **{{ school.gpa }}**

{% endfor %}
{% endblock body %}
