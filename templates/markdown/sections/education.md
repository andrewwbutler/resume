{% extends "section.md" %}

{% block body %}
{% for school in items %}
**{{ school.school }}**  
{{ school.major }}  - _{{ school.date }}_
<br>
{% if school.notes is defined %}{{ school.notes }}{% endif %}


{% endfor %}
{% endblock body %}
