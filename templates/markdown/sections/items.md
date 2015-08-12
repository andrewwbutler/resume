{% extends "section.md" %}

{% macro listitem(item) %}{% if item.description is defined %}  - **{{ item.name | wordwrap(width=76, wrapstring='\n    ') }}:**
    {{ item.description | wordwrap(width=76, wrapstring='\n    ') }}
{% elif item.notes is defined %}  - {{ item.name | wordwrap(width=76, wrapstring='\n    ') }}
{% for note in item.notes %}    - {{ note | wordwrap(width=74, wrapstring='\n      ') }}
{% endfor %}{% else %}  - {{ item | wordwrap(width=76, wrapstring='\n    ') }}
{% endif %}{% endmacro %}

{% block body %}
{% if subsections is defined %}
{% for subs in subsections %}

#### {{ subs.name }} ####
{% for item in subs.subitems %}{{ listitem(item) }}{% endfor %}
{% endfor %}
{% else %}
{% for item in items %}{{ listitem(item) }}{% endfor %}
{% endif %}
{% endblock body %}
