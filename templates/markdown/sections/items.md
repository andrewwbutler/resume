{% extends "section.md" %}
{% macro listitem(item) %}{% if item.description %}  - **{{ item.name }}:** {{ item.description }}{% elif item.notes %}  - {{ item.name }}
{% for note in item.notes %}    - {{ note }}
{% endfor %}{% else %}  - {{ item }}{% endif %}{% endmacro %}
{% block body %}
{% if subsections %}
{% for subs in subsections %}
####{{ subs.name }}####
{% for item in subs.subitems %}
{{ listitem(item) }}
{% endfor %}

{% endfor %}
{% else %}
{% for item in items %}
{{ listitem(item) }}
{% endfor %}
{% endif %}
{% endblock body %}
