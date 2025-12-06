#!/bin/bash

YELLOW='\033[1;33m'
GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m'

INSTALL_DIR="/opt/userturk"
SETTINGS_FILE="$INSTALL_DIR/config/settings.py"
COMPOSE_FILE="$INSTALL_DIR/docker-compose.yml"
DATA_DIR="$INSTALL_DIR/data"
DB_FILE="$DATA_DIR/database.db"
REPO_URL="https://github.com/YOUR_USERNAME/UserTurk.git"
PROJECT_NAME="userturk"


check_prerequisites() {
    echo -e "${YELLOW}Checking system prerequisites...${NC}"

    if ! command -v git &> /dev/null; then
        echo -e "${YELLOW}Git not found. Installing...${NC}"
        sudo apt-get update
        sudo apt-get install -y git || exit 1
    fi

    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}Docker not found. Installing...${NC}"
        sudo apt-get update
        sudo apt-get install -y docker.io || exit 1
        sudo systemctl enable docker
        sudo systemctl start docker
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo -e "${YELLOW}Docker Compose not found. Installing...${NC}"
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
            -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi

    echo -e "${GREEN}All prerequisites installed successfully.${NC}"
}


validate_token() {
    local token=$1
    echo -e "${YELLOW}Validating Telegram bot token...${NC}"

    response=$(curl -s "https://api.telegram.org/bot${token}/getMe")

    if [[ "$response" =~ \"ok\":true ]]; then
        echo -e "${GREEN}Token is valid ✔${NC}"
        return 0
    else
        echo -e "${RED}Invalid bot token!${NC}"
        return 1
    fi
}


get_token_and_id() {
    while true; do
        echo -e "${YELLOW}Enter your Telegram Bot Token:${NC}"
        read -r BOT_TOKEN

        echo -e "${YELLOW}Enter Admin Numeric ID:${NC}"
        read -r ADMIN_ID

        if ! validate_token "$BOT_TOKEN"; then
            echo -e "${RED}Please enter a valid token.${NC}"
            continue
        fi

        if ! [[ "$ADMIN_ID" =~ ^[0-9]+$ ]]; then
            echo -e "${RED}Admin ID must be numeric.${NC}"
            continue
        fi

        export BOT_TOKEN ADMIN_ID
        return 0
    done
}


edit_settings() {
    echo -e "${YELLOW}Configuring settings.py...${NC}"

    mkdir -p "$INSTALL_DIR/config"

    cat > "$SETTINGS_FILE" << EOF
BOT_TOKEN = "$BOT_TOKEN"
ADMIN_ID = $ADMIN_ID
DB_PATH = "data/database.db"
EOF

    echo -e "${GREEN}settings.py configured successfully ✔${NC}"
}


setup_data_directory() {
    echo -e "${YELLOW}Setting up database directory...${NC}"
    mkdir -p "$DATA_DIR"
    chmod 777 "$DATA_DIR"
    rm -f "$DB_FILE"
    echo -e "${GREEN}Database directory ready ✔${NC}"
}


cleanup_docker() {
    echo -e "${YELLOW}Removing old containers/images...${NC}"

    if [ -f "$COMPOSE_FILE" ]; then
        sudo docker-compose -f "$COMPOSE_FILE" down --volumes --rmi all || true
    fi

    sudo docker ps -a -q -f "name=$PROJECT_NAME" | xargs -r sudo docker rm
    sudo docker images -q "$PROJECT_NAME" | xargs -r sudo docker rmi

    echo -e "${GREEN}Cleanup complete ✔${NC}"
}

install_bot() {
    echo -e "${GREEN}Starting UserTurk Installation...${NC}"

    if [ -d "$INSTALL_DIR" ]; then
        cleanup_docker
        sudo rm -rf "$INSTALL_DIR"
    fi

    check_prerequisites

    echo -e "${YELLOW}Cloning repository...${NC}"
    git clone "$REPO_URL" "$INSTALL_DIR" || exit 1

    get_token_and_id
    edit_settings
    setup_data_directory

    echo -e "${YELLOW}Building and starting Docker Compose...${NC}"
    cd "$INSTALL_DIR"

    sudo docker-compose build --no-cache
    sudo docker-compose up -d

    echo -e "${GREEN}UserTurk bot installed and running! ✔${NC}"
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
        2) cleanup_docker ; install_bot ;;
        3) cleanup_docker ; sudo rm -rf "$INSTALL_DIR" ; echo -e "${GREEN}Bot removed ✔${NC}" ;;
        4) get_token_and_id ; edit_settings ;;
        5) sudo docker-compose -f "$COMPOSE_FILE" restart ;;
        6) exit 0 ;;
        *) echo -e "${RED}Invalid option!${NC}" ;;
    esac

    echo -e "${YELLOW}Press any key to continue...${NC}"
    read -n 1
done
