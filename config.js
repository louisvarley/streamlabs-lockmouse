var settings = {
  "liveOnly": false,
  "command": "!lock",
  "permission": "Everyone",
  "costs": 0,
  "useCooldown": false,
  "useCooldownMessages": true,
  "cooldown": 60,
  "onCooldown": "$user, $command is still on cooldown for $cd seconds!",
  "lockDuration": 10,
  "userCooldown": 300,
  "onUserCooldown": "$user, $command is still on user cooldown for $cd seconds!",
  "responseNotEnoughPoints": "$user you need $cost $currency to use $command.",
  "responseOnSuccess": "$user has locked the mouse for $lockDuration seconds."
};