execute as @a store result score @s sb_player_dx run data get entity @s Pos[0]
execute as @a store result score @s sb_player_dz run data get entity @s Pos[2]
execute as @a run scoreboard players operation @s sb_player_dx -= x sb_origin
execute as @a run scoreboard players operation @s sb_player_dz -= z sb_origin
