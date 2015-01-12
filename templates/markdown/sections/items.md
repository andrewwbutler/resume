{% extends "section.md" %}

{% macro listitem(item) %}{% if item.description %}  - **{{ item.name | wordwrap(wrapstring='\n    ') }}:**
    {{ item.description | wordwrap(wrapstring='\n    ') }}
{% elif item.notes %}  - {{ item.name | wordwrap(wrapstring='\n    ') }}
{% for note in item.notes %}    - {{ note | wordwrap(wrapstring='\n      ') }}
{% endfor %}{% else %}  - {{ item | wordwrap(wrapstring='\n    ') }}
{% endif %}{% endmacro %}

{% block body %}
{% if subsections %}
{% for subs in subsections %}
#### {{ subs.name }} ####
{% for item in subs.subitems %}{{ listitem(item) }}{% endfor %}

{% endfor %}
{% else %}
{% for item in items %}{{ listitem(item) }}{% endfor %}
{% endif %}
{% endblock body %}
