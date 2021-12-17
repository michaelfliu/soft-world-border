import argparse
import json
import os

from textwrap import dedent


def preprocess_config(config):
    config["insanityGain"].sort(key=lambda x: x["distance"])
    for zone in config["insanityZones"]:
        effect = zone["effect"]
        if effect.get("type") is None:
            effect["type"] = "constant"
        if effect.get("level") is None:
            effect["level"] = 0
        else:
            effect["level"] -= 1
    for zone in config["distanceZones"]:
        effect = zone["effect"]
        if effect.get("type") is None:
            effect["type"] = "constant"
        if effect.get("level") is None:
            effect["level"] = 0
        else:
            effect["level"] -= 1


def get_insanity_gain_name(dist):
    return f"ig_zone_{dist}"


def get_distance_zone_name(min_dist, max_dist):
    min_str = str(min_dist) if min_dist is not None else "0"
    max_str = str(max_dist) if max_dist is not None else "inf"
    return f"dz_zone_{min_str}_{max_str}"


def get_insanity_zone_name(min_insanity, max_insanity):
    min_str = str(min_insanity) if min_insanity is not None else "0"
    max_str = str(max_insanity) if max_insanity is not None else "inf"
    return f"iz_zone_{min_str}_{max_str}"


def get_period_loop_name(period):
    return f"apply_periodic_effects_{period}s"


def make_predicates(config, predicates_dir):
    insanity_gains = config["insanityGain"]
    distance_zones = config["distanceZones"]
    insanity_zones = config["insanityZones"]

    os.makedirs(predicates_dir, exist_ok=True)

    make_insanity_gain_predicates(insanity_gains, predicates_dir)
    make_distance_zone_predicates(distance_zones, predicates_dir)
    make_insanity_zone_predicates(insanity_zones, predicates_dir)


def make_insanity_gain_predicates(insanity_gains, predicates_dir):
    distances = [0] + [ig["distance"] for ig in insanity_gains] + [None]
    for i in range(len(distances) - 1):
        predicate = make_dist_predicate(distances[i], distances[i+1])
        filename = get_insanity_gain_name(distances[i]) + ".json"
        with open(os.path.join(predicates_dir, filename), 'w') as f:
            f.write(predicate)


def make_distance_zone_predicates(distance_zones, predicates_dir):
    for dist_zone in distance_zones:
        min_dist = dist_zone.get("minDistance")
        max_dist = dist_zone.get("maxDistance")
        predicate = make_dist_predicate(min_dist, max_dist)
        filename = get_distance_zone_name(min_dist, max_dist) + ".json"
        with open(os.path.join(predicates_dir, filename), 'w') as f:
            f.write(predicate)


def make_insanity_zone_predicates(insanity_zones, predicates_dir):
    for insanity_zone in insanity_zones:
        min_insanity = insanity_zone.get("minInsanity")
        max_insanity = insanity_zone.get("maxInsanity")
        predicate = make_insanity_predicate(min_insanity, max_insanity)
        filename = get_insanity_zone_name(min_insanity, max_insanity) + ".json"
        with open(os.path.join(predicates_dir, filename), 'w') as f:
            f.write(predicate)


def make_dist_predicate(min_dist=None, max_dist=None):
    if min_dist is None and max_dist is None:
        raise Exception("make_dist_predicate called with no arguments")
    elif min_dist is None:
        predicate = make_in_dist_predicate(max_dist)
    elif max_dist is None:
        predicate = make_out_dist_predicate(min_dist)
    else:
        in_predicate = make_in_dist_predicate(max_dist)
        out_predicate = make_out_dist_predicate(min_dist)
        predicate = dedent(f'''[{in_predicate},{out_predicate}]''')
    return predicate


def make_in_dist_predicate(max_dist):
    return dedent(f'''\
        {{
          "condition": "minecraft:entity_scores",
          "entity": "this",
          "scores": {{
            "sb_player_dx": {{
              "min": {-max_dist},
              "max": {max_dist}
            }},
            "sb_player_dz": {{
              "min": {-max_dist},
              "max": {max_dist}
            }}
          }}
        }}
        ''')


def make_out_dist_predicate(min_dist):
    in_predicate = make_in_dist_predicate(min_dist)
    return dedent(f'''
        {{
          "condition": "minecraft:inverted",
          "term": {in_predicate}
        }}
        ''')


def make_insanity_predicate(min_dist=None, max_dist=None):
    if min_dist is None and max_dist is None:
        raise Exception("make_insanity_predicate called with no arguments")
    elif min_dist is None:
        predicate = make_in_insanity_predicate(max_dist)
    elif max_dist is None:
        predicate = make_out_insanity_predicate(min_dist)
    else:
        in_predicate = make_in_insanity_predicate(max_dist)
        out_predicate = make_out_insanity_predicate(min_dist)
        predicate = dedent(f'''\
            [
                {in_predicate},
                {out_predicate}
            ]
            ''')
    return predicate


def make_in_insanity_predicate(max_insanity):
    return dedent(f'''\
        {{
          "condition": "minecraft:entity_scores",
          "entity": "this",
          "scores": {{
            "sb_insanity": {{
              "min": {-max_insanity},
              "max": {max_insanity}
            }}
          }}
        }}
        ''')


def make_out_insanity_predicate(min_dist):
    in_predicate = make_in_insanity_predicate(min_dist)
    return dedent(f'''
        {{
          "condition": "minecraft:inverted",
          "term": {in_predicate}
        }}
        ''')


def make_insanity_update(insanity_gains, datapack_path):
    commands = [make_insanity_clear_command(get_insanity_gain_name(0))]
    for insanity_gain in insanity_gains:
        dist = insanity_gain["distance"]
        amount = insanity_gain["amount"]
        pred_name = get_insanity_gain_name(dist)
        commands.append(make_insanity_update_command(pred_name, amount))
    update_insanity_file = os.path.join(
        datapack_path, "data", "softborder", "functions", "private", "gen", "update_insanity.mcfunction")
    with open(update_insanity_file, 'w') as f:
        f.write('\n'.join(commands) + '\n')


def make_insanity_clear_command(pred_name):
    return f"execute as @a if predicate softborder:{pred_name} if score @s sb_player_under_cover matches 1.. run scoreboard players set @s sb_insanity 0"


def make_insanity_update_command(pred_name, amount):
    return f"execute as @a if predicate softborder:{pred_name} run scoreboard players add @s sb_insanity {amount}"


def make_const_effects(config, datapack_path):
    insanity_effects = make_insanity_const_effects(config["insanityZones"])
    distance_effects = make_distance_const_effects(config["distanceZones"])
    apply_const_effects_file = os.path.join(
        datapack_path, "data", "softborder", "functions", "private", "gen", "apply_const_effects.mcfunction")
    with open(apply_const_effects_file, 'w') as f:
        f.write('\n'.join(insanity_effects + distance_effects) + '\n')


def make_insanity_const_effects(insanity_zones):
    effect_commands = []
    for zone in insanity_zones:
        effect = zone["effect"]
        if effect["type"] == "constant":
            min_insanity = zone.get("minInsanity")
            max_insanity = zone.get("maxInsanity")
            pred = get_insanity_zone_name(min_insanity, max_insanity)
            effect_id = effect["id"]
            effect_level = effect["level"]
            effect_commands.append(make_const_effect(
                pred, effect_id, effect_level))
    return effect_commands


def make_distance_const_effects(distance_zones):
    effect_commands = []
    for zone in distance_zones:
        effect = zone["effect"]
        if effect["type"] == "constant":
            min_dist = zone.get("minDistance")
            max_dist = zone.get("maxDistance")
            pred = get_distance_zone_name(min_dist, max_dist)
            effect_id = effect["id"]
            effect_level = effect["level"]
            effect_commands.append(make_const_effect(
                pred, effect_id, effect_level))
    return effect_commands


def make_const_effect(pred_name, effect_id, effect_level):
    return f"effect give @a[predicate=softborder:{pred_name}] {effect_id} 5 {effect_level} true"


def make_periodic_effects(config, datapack_path):
    insanity_effects = make_periodic_insanity_effects(config["insanityZones"], datapack_path)
    distance_effects = make_periodic_distance_effects(config["distanceZones"], datapack_path)
    effects = insanity_effects + distance_effects

    make_start_periodic_effects(effects, datapack_path)
    make_stop_periodic_effects(effects, datapack_path)


def make_periodic_insanity_effects(insanity_zones, datapack_path):
    names = []
    for zone in insanity_zones:
        effect = zone["effect"]
        if effect["type"] != "constant":
            min_insanity = zone.get("minInsanity")
            max_insanity = zone.get("maxInsanity")
            name = get_insanity_zone_name(min_insanity, max_insanity)
            names.append(name)
            effect_id = effect["id"]
            effect_level = effect["level"]
            period = effect["type"]["period"]
            pulse = effect["type"]["pulse"]
            filename = os.path.join(datapack_path, "data", "softborder", "functions", "private", "gen", name + ".mcfunction")
            with open(filename, 'w') as f:
                f.write(make_periodic_effect(name, effect_id, effect_level, period, pulse))
    return names


def make_periodic_distance_effects(distance_zones, datapack_path):
    names = []
    for zone in distance_zones:
        effect = zone["effect"]
        if effect["type"] != "constant":
            min_dist = zone["minDistance"]
            max_dist = zone["maxDistance"]
            name = get_distance_zone_name(min_dist, max_dist)
            names.append(name)
            effect_id = effect["id"]
            effect_level = effect["level"]
            period = effect["type"]["period"]
            pulse = effect["type"]["pulse"]
            filename = os.path.join(datapack_path, "data", "softborder", "functions", "private", "gen", name + ".mcfunction")
            with open(filename, 'w') as f:
                f.write(make_periodic_effect(name, effect_id, effect_level, period, pulse))
    return names


def make_periodic_effect(name, effect_id, effect_level, period, pulse):
    return dedent(f'''\
        effect give @a[predicate=softborder:{name}] {effect_id} {pulse} {effect_level} true
        schedule function softborder:private/gen/{name} {period}s replace
        ''')


def make_start_periodic_effects(effects, datapack_path):
    commands = [make_start_periodic_effect(effect) for effect in effects]
    start_file_path = os.path.join(datapack_path, "data", "softborder", "functions", "private", "gen", "start_periodic_effects.mcfunction")
    with open(start_file_path, 'w') as f:
        for line in commands:
            f.write(line)
            f.write(os.linesep)


def make_start_periodic_effect(effect):
    return f"function softborder:private/gen/{effect}"


def make_stop_periodic_effects(effects, datapack_path):
    commands = [make_stop_periodic_effect(effect) for effect in effects]
    stop_file_path = os.path.join(datapack_path, "data", "softborder", "functions", "private", "gen", "stop_periodic_effects.mcfunction")
    with open(stop_file_path, 'w') as f:
        for line in commands:
            f.write(line)
            f.write(os.linesep)


def make_stop_periodic_effect(effect):
    return f"schedule clear softborder:private/gen/{effect}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates datapack files from config")
    parser.add_argument(
        "--config", '-c', default="./config.json", help="path to the config file")
    parser.add_argument("--output", '-o', default=".",
                        help="path to the datapack folder")
    parser.add_argument("--force", '-f', default=False,
                        action="store_true", help="overwrite existing configs")

    args = parser.parse_args()
    args.config = os.path.normpath(args.config)
    args.output = os.path.normpath(args.output)
    predicates_dir = os.path.join(
        args.output, "data", "softborder", "predicates")
    gen_dir = os.path.join(args.output, "data", "softborder", "functions", "private", "gen")

    validate_fail = False
    if not os.path.exists(args.config):
        print(f"Error: Cannot find config file {args.config}")
        validate_fail = True
    if (not os.path.exists(args.output)) or (not os.path.isdir(args.output)):
        print(f"Error: Cannot find output directory {args.output}")
        validate_fail = True
    elif not args.force and (os.path.exists(predicates_dir) or os.path.exists(gen_dir)):
        print(f"Error: Output directories {predicates_dir} and {gen_dir} not empty. Use -f to overwrite existing configs")
        validate_fail = True
    if validate_fail:
        exit(1)

    with open(args.config) as config_file:
        config = json.load(config_file)

    preprocess_config(config)
    make_predicates(config, predicates_dir)

    os.makedirs(gen_dir, exist_ok=True)
    make_insanity_update(config["insanityGain"], args.output)
    make_const_effects(config, args.output)
    make_periodic_effects(config, args.output)
