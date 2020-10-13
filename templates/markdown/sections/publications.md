{% extends "section.md" %}
{% macro render_pub(pub) -%}
"[{{pub.title}}]({{ pub.url}})."
<br>
{% for auth in pub.authors %}
    {{ auth }}{{ ", " if not loop.last else ". " }}
{% endfor %} {{ pub.journal }} {% if pub.venueshort is defined %} ({{ pub.venueshort }}){% endif %}{% if pub.venuelocation is defined %}, {{ pub.venuelocation }}{% endif %}. {{ pub.month }} {{ pub.year }}.
{%- endmacro %}

{% block body %}
{% for pub in items %}
{{ render_pub(pub) | wordwrap }}

{% endfor %}
{% endblock body %}
