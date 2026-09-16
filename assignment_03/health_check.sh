services=("nginx" "ssh")

for service in "${services[@]}"; do
    status=$(systemctl is-active "$service")

    if [ "$status" = "active" ]; then
        echo "[$service]: Dang chay $status"
    else
        echo "[$service]: Khong hoat dong $status"
    fi
done
