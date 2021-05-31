now="$(TZ='Europe/Paris' date -I)"
zola build && sed -i "s/{{ now }}/$now/g" public/humans.txt