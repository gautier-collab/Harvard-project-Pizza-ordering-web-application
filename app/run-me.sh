cd app/container-files

while read -r line; do
    echo "$line"
    if [[ "$line" == *"Watching for file changes with"* ]]; then
        echo "" && echo "The web application is launched at http://127.0.0.1:8000/" && echo ""
        cd - && cd app && python3 website-opening.py
    fi
done< <(sudo docker-compose up --build)