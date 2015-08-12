### {{ name }} ###
---
{% if legend is defined %}
{{ legend }}

{% endif %}
{% block body %}
{{ data }}
{% endblock body %}
