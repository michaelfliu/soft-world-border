execute in minecraft:overworld as @a[distance=0..] positioned as @s store result score @s sb_blocks_above_player if blocks ~ ~1 ~ ~ 319 ~ ~ ~1 ~ masked
execute in minecraft:the_nether as @a[distance=0..] positioned as @s store result score @s sb_blocks_above_player if blocks ~ ~1 ~ ~ 255 ~ ~ ~1 ~ masked
execute in minecraft:the_end as @a[distance=0..] positioned as @s store result score @s sb_blocks_above_player if blocks ~ ~1 ~ ~ 255 ~ ~ ~1 ~ masked

execute as @a if score @s sb_blocks_above_player matches 0 run scoreboard players add @s sb_insanity 100
