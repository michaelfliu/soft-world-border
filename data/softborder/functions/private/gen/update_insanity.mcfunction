execute as @a if predicate softborder:ig_zone_0 if score @s sb_player_under_cover matches 1.. run scoreboard players set @s sb_insanity 0
execute as @a if predicate softborder:ig_zone_64 run scoreboard players add @s sb_insanity 1
execute as @a if predicate softborder:ig_zone_128 run scoreboard players add @s sb_insanity 3
execute as @a if predicate softborder:ig_zone_256 run scoreboard players add @s sb_insanity 7
execute as @a if predicate softborder:ig_zone_512 run scoreboard players add @s sb_insanity 15
execute as @a if predicate softborder:ig_zone_512 run scoreboard players add @s sb_insanity 31
execute as @a if predicate softborder:ig_zone_1024 run scoreboard players add @s sb_insanity 63
execute as @a if predicate softborder:ig_zone_2048 run scoreboard players add @s sb_insanity 127
execute as @a if predicate softborder:ig_zone_4096 run scoreboard players add @s sb_insanity 255
execute as @a if predicate softborder:ig_zone_8192 run scoreboard players add @s sb_insanity 2047
