#!/bin/bash

YELLOW='\033[1;33m'
GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m'

INSTALL_DIR="/opt/userturk"
SETTINGS_FILE="$INSTALL_DIR/config/settings.py"
DATA_DIR="$INSTALL_DIR/data"
DB_FILE="$DATA_DIR/database.db"
ZIP_URL="https://github.com/mahyyar/UserTruck/archive/refs/heads/main.zip"
PROJECT_NAME="userturk"

check_prerequisites() {
    echo -e "${YELLOW}Checking system prerequisites...${NC}"

    if ! command -v unzip &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y unzip
    fi

    if ! command -v docker &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y docker.io
        sudo systemctl enable docker
        sudo systemctl start docker
    fi

    if ! command -v docker-compose &> /dev/null; then
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
            -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
}

validate_token() {
    response=$(curl -s "https://api.telegram.org/bot${1}/getMe")
    [[ "$response" =~ \"ok\":true ]]
}

get_token_and_id() {
    while true; do
        echo -e "${YELLOW}Enter your Telegram Bot Token:${NC}"
        read -r BOT_TOKEN
        if ! validate_token "$BOT_TOKEN"; then
            echo -e "${RED}Invalid token.${NC}"
            continue
        fi
        echo -e "${YELLOW}Enter Admin Numeric ID:${NC}"
        read -r ADMIN_ID
        if ! [[ "$ADMIN_ID" =~ ^[0-9]+$ ]]; then
            echo -e "${RED}Admin ID must be numeric.${NC}"
            continue
        fi
        export BOT_TOKEN ADMIN_ID
        return 0
    done
}

edit_settings() {
    mkdir -p "$INSTALL_DIR/config"
    cat > "$SETTINGS_FILE" << EOF
BOT_TOKEN = "$BOT_TOKEN"
ADMIN_ID = $ADMIN_ID
DB_PATH = "data/database.db"
EOF
}

setup_data_directory() {
    mkdir -p "$DATA_DIR"
    chmod 777 "$DATA_DIR"
    rm -f "$DB_FILE"
}

cleanup_old_install() {
    if [ -d "$INSTALL_DIR" ]; then
        sudo docker-compose -f "$INSTALL_DIR/docker-compose.yml" down --volumes --rmi all || true
        sudo rm -rf "$INSTALL_DIR"
    fi
}

install_bot() {
    cleanup_old_install
    check_prerequisites

    mkdir -p /opt
    cd /opt

    echo -e "${YELLOW}Downloading UserTurk...${NC}"
    curl -L "$ZIP_URL" -o userturk.zip

    unzip -q userturk.zip
    rm userturk.zip

    mv UserTruck-main "$INSTALL_DIR"

    get_token_and_id
    edit_settings
    setup_data_directory

    cd "$INSTALL_DIR"
    sudo docker-compose build --no-cache
    sudo docker-compose up -d

    echo -e "${GREEN}UserTurk bot installed and running ✔${NC}"
}

show_menu() {
    clear
    echo -e "${YELLOW}===== UserTurk Bot Manager =====${NC}"
    echo "1) Install Bot"
    echo "2) Update"
    echo "3) Uninstall"
    echo "4) Change Token/Admin ID"
    echo "5) Restart Bot"
    echo "6) Exit"
    echo -e "${YELLOW}Choose an option:${NC}"
}

while true; do
    show_menu
    read -r opt

    case $opt in
        1) install_bot ;;
        2) install_bot ;;
        3) cleanup_old_install ;;
        4) get_token_and_id ; edit_settings ;;
        5) sudo docker-compose -f "$INSTALL_DIR/docker-compose.yml" restart ;;
        6) exit 0 ;;
        *) echo -e "${RED}Invalid option!${NC}" ;;
    esac

    echo -e "${YELLOW}Press any key to continue...${NC}"
    read -n 1
done
