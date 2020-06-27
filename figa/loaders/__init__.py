from figa.loaders import env, json, yaml, ini, toml, hocon

# parse names, file extensions
parsers = {
    "env": env.EnvParser,
    "json": json.JSONParser,
    ("yaml", "yml"): yaml.YamlParser,
    ("ini", "cfg", "properties"): ini.IniParser,
    ("conf", "hocon"): hocon.HoconParser,
    "toml": toml.TomlParser
}

# convert single item names to tuples

parsers_full = {}
for k, v in parsers.items():
    if isinstance(k, tuple):
        for sk in k:
            parsers_full[sk] = v
    else:
        parsers_full[k] = v

from figa.loaders import http
parsers_full["http"] = http.HttpParser


def detect_and_parse(args, default=None):
    s_name = args[0].lower()
    ext = s_name.split(".")[-1]

    if s_name in parsers_full:
        return parsers_full[s_name].__handler__(*args[1:], default=default)
    elif ext in parsers_full:
        return parsers_full[ext].__handler__(*args, default=default)

    raise NotImplementedError("No parser found for {!r}".format(args[0]))
