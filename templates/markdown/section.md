<div style="position: relative;">
  {% if legend %}
    <div style="position: absolute; bottom: 0; right: 0;">{{ legend }}</div>
  {% endif %}
  <h3>{{ name }}</h2>
</div>
---
{% block body %}
{{ data }}
{% endblock body %}
