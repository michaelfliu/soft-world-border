scoreboard objectives add sb_origin dummy "Softborder Origin"
scoreboard objectives add sb_insanity dummy "Insanity"
scoreboard objectives add sb_player_dx dummy "X Distance to Origin"
scoreboard objectives add sb_player_dz dummy "Z Distance to Origin"
scoreboard objectives add sb_blocks_above_player dummy "Blocks Above Player"

scoreboard players reset * sb_origin
scoreboard players reset * sb_insanity
scoreboard players reset * sb_player_dx
scoreboard players reset * sb_player_dz
scoreboard players reset * sb_blocks_above_player

function softborder:menu
