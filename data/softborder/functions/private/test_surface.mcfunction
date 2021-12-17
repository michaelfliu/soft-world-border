execute in minecraft:overworld as @a[distance=0..] positioned as @s store success score @s sb_player_under_cover run clone ~ ~1 ~ ~ 319 ~ ~ ~1 ~ masked force
execute in minecraft:the_nether as @a[distance=0..] positioned as @s store success score @s sb_player_under_cover run clone ~ ~1 ~ ~ 255 ~ ~ ~1 ~ masked force
execute in minecraft:the_end as @a[distance=0..] positioned as @s store success score @s sb_player_under_cover run clone ~ ~1 ~ ~ 255 ~ ~ ~1 ~ masked force
execute as @a if score @s sb_player_under_cover matches 0 run scoreboard players add @s sb_insanity 100
