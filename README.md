# Soft World Border

Have you ever played survival multiplayer Minecraft with your friends, but as soon as the server starts, everyone tucks themselves into their own little corner of the world? You've thought to yourself, "maybe I should set up a world border this season! That'll fix things for sure!" Unfortunately, when you do this, you run out of diamonds in two days because one of your especially "hardworking" friends mines them all and throws them into their personal ender chest. Your friends who enjoy adventuring quit after they realize that the far lands are out of reach. This cuts the server population in half, which means your builder friends who actually like basing together (so much that they live with each other in real life) don't have as many people to show off their builds to. They leave, and it's just you, playing singleplayer.

Well with SoftBorder, you won't experience this again\*! Instead of a hard cutoff for how far players can travel, this datapack lets you configure increasingly worse effects as players get further away from an origin location. Oh, and as an added bonus, insanity goes off the charts when the player is on the surface for some reason. Sorry!

---

## Insanity

The main idea behind the soft worldborder is a number representing each player's "insanity". When the player is within a certain distance of the origin, they have no insanity and do not suffer any side effects related to insanity. However, after crossing a threshold, the player begins to accumulate insanity points every second. The datapack can be configured to give increasing amounts of insanity based on how far the player is away from the origin.

When the player has enough insanity points, they will start experiencing effects defined in the configuration file.

---

## Dependencies

If you are happy with the existing config, then no dependencies other than Minecraft 1.18 are required.

---

## Config.json

The configuration file has 3 sections

```json
{
    "insanityGain": [
        ...
    ],
    "distanceZones": [
        ...
    ],
    "insanityZones": [
        ...
    ]
}
```

### `insanityGain`

This section contains a list of distances paired with the amount of insanity the player gains per second when outside of that distance. The sections are not cumulative, so specifying an insanity gain of 1 at a distance of 64 blocks and an insanity gain of 2 at a distance of 128 blocks will not give 3 insanity outside 128 blocks. Implicitly, when the player is within the lowest specified distance, their insanity is set immediately to 0.

```json
    "insanityGain": [
        {
            "distance": 64,
            "insanity": 1
        },
        {
            "distance": 128,
            "insanity": 2
        },
    ],
```

### `distanceZones`

This section lists all distance based effects. These effects are applied to the player when they are at least `minDist` blocks away from the origin and within `maxDist` blocks from the origin. At least one of these must be specified, but leaving one out implies that the effect is applied either outside of `minDist` blocks or inside of `maxDist` blocks away.

```json
    "distanceZones": [
        {
            "minDistance": 64,
            "maxDistance": 75,
            "effect": {
                "id": "minecraft:glowing",
            }
        },
        {
            "minDistance": 75,
            "effect": {
                "id": "minecraft:hunger",
                "level": 2,
                "type": "constant"
            }
        }
    ],
```

### `insanityZones`

Just like `distanceZones`, this field lists effects that will be given to the player when they are within some **insanity** threshold.

```json
    "insanityZones": [
        {
            "minInsanity": 64,
            "maxInsanity": 75,
            "effect": {
                "id": "minecraft:glowing",
            }
        },
        {
            "minInsanity": 75,
            "effect": {
                "id": "minecraft:hunger",
                "level": 2,
                "type": "constant"
            }
        }
    ],
```

### Effect format

Each effect specifies an `id` that is the minecraft ID of the effect. These must be in the list allowed by the `/effect` command.

The `level` field selects the level of the effect. This is one more than the "amplifier" value used by Minecraft's `/effect` command, so putting a `level` of 2 with slowness means the player will gain slowness 2. If the `level` is omitted, a value of 1 is assumed.

The `type` field determines how the effect is applied to the player. `constant` type effects will be applied for 5 seconds every one second, meaning the player will always be under their effects. This is the type assumed if the `type` field is not in the effect.

It is also possible to define periodic effects using the `type` field. Simply give it a `period` (how often it will run) and a `pulse` (how long to apply the effect for). For example, the `instant_damage` effect with a period of 5 and a pulse of 1 will apply instant damage to the player for 1 second every 5 seconds. Note that the pulse does not actually matter here; instant damage only applies when the effect is first given to the player so any `pulse` less than 5 would work.

```json
"effect": {
    "id": "minecraft:slowness",
    "level": 2,
    "type": "constant"
}

"effect": {
    "id": "minecraft:instant_damage",
    "type": {
        "period": 5,
        "pulse": 1
    }
}
```

---

## Installing

After setting up the configuration to your liking, 

---

## Fine Print

<sup>\* Not actually guaranteed, I am not responsible if anyone tells you this is a horrible idea.</sup>
