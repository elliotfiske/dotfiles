printf "\e]1337;SetBadgeFormat=%s\a" \
  $(echo "$1 $2" | base64)
