{% macro calculate_threat_score(url_length, num_dots, has_https, has_ip_address) %}
    -- Calculate a simple threat score based on URL characteristics
    CASE
        WHEN {{ has_ip_address }} = 1 THEN 100
        WHEN {{ url_length }} > 100 AND {{ num_dots }} > 5 THEN 80
        WHEN {{ has_https }} = 0 AND {{ url_length }} > 50 THEN 60
        ELSE 20
    END
{% endmacro %}

