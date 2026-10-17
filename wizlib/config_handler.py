from argparse import Namespace
from functools import cached_property
from pathlib import Path
import os
from dataclasses import dataclass
import subprocess

import yaml

from wizlib.handler import Handler
from wizlib.error import ConfigHandlerError
from wizlib.parser import WizParser


class ConfigHandler(Handler):
    """
    Handle app-level configuration, where settings could come from specific
    settings (such as from argparse), environment variables, or a YAML file.
    Within the Python code, config keys are underscore-separated all-lower.

    A ConfigHandler returns null in the case of a missing value, assuming that
    commands can handle their own null cases.
    """

    name = 'config'

    @classmethod
    def setup(cls, val):
        """Allow for alternative setup, passing in an injected data value as a
        dict, bypassing file loading, for testing. Possible long-term
        alternative to .fake() below."""

        if isinstance(val, str) or isinstance(val, Path):
            return cls(file=val)
        elif isinstance(val, dict) or isinstance(val, list):
            return cls(data=val)

    def __init__(self, file: str = None, data: dict = None):
        """Initiatlize with either a yaml file path or a data block to inject
        (for testing)"""
        self.file = file
        self.injected_data = data
        self.cache = {}
        self.fake_keys = set()

    @cached_property
    def data(self):
        """Returns the full set of configuration data, typically loaded from a
        yaml file. Is cached in code."""

        # If yaml_dict was provided, use it directly
        if self.injected_data is not None:
            return self.injected_data

        path = None
        if self.file:
            path = Path(self.file)
        elif self.app and self.app.name:
            localpath = Path.cwd() / f".{self.app.name}.yml"
            homepath = Path.home() / f".{self.app.name}.yml"
            if (envvar := self.env(self.app.name + '-config')):
                path = Path(envvar)
            elif (localpath.is_file()):
                path = localpath
            elif (homepath.is_file()):
                path = homepath
        if path:
            with open(path) as file:
                data = yaml.safe_load(file)
                return data

    @staticmethod
    def env(name):
        if (envvar := name.upper().replace('-', '_')) in os.environ:
            return os.environ[envvar]

    def get(self, *keys: str):
        """Return the value for the requested config entry. If the value from
        the YAML file (or injected data) is a string that is exactly a
        1Password secret reference (op://vault/item/field), it is resolved
        using the 1Password CLI (`op read`). Other strings are returned as-is.
        Can also return a dict or array. Note that the value returned is cached
        against the requested path, so future calls may not address nested
        paths.

        With a single argument, it is a hyphen-separated path through the
        yaml/dict hierarchy, e.g. get('myapp-host').

        With more than one argument, each argument is a literal key (which may
        itself contain hyphens), e.g. get('myapp', 'classify',
        'auto-threshold'). The environment override is the keys joined with
        underscores, with hyphens replaced by underscores, upper-cased, e.g.
        MYAPP_CLASSIFY_AUTO_THRESHOLD."""

        if not keys:
            raise TypeError('ConfigHandler.get() requires at least one key')

        if len(keys) == 1:
            data_path = keys[0]
            return self._lookup(data_path, data_path, data_path.split('-'),
                                repr(data_path))

        keys = tuple(keys)
        # Support ConfigHandler.fake(), which stores hyphen-joined strings.
        # Only faked entries are consulted, so values cached by single-string
        # lookups never collide with explicit paths.
        if keys not in self.cache and \
                (joined := '-'.join(keys)) in self.fake_keys:
            return self.cache[joined]
        return self._lookup(keys, '_'.join(keys), keys,
                            ', '.join(repr(k) for k in keys))

    def _lookup(self, cache_key, env_name: str, path, name: str):
        """Find a value by cache, then environment, then data, caching the
        result against cache_key. Returns None (uncached) if missing. The name
        identifies the config key in error messages."""

        # If we already found the value, return it
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Environment variables take precedence
        if (result := self.env(env_name)):
            self.cache[cache_key] = result
            return result

        # Otherwise look at the YAML or injected data
        if (data := self.data):
            for key in path:
                if not isinstance(data, dict) or key not in data:
                    return None
                data = data[key]
            if isinstance(data, str):
                data = resolve_secret(data, name)
            self.cache[cache_key] = data
            return data

    @classmethod
    def fake(cls, **vals):
        """Return a fake ConfigHandler with forced values, for testing"""
        self = cls()
        self.cache = {k.replace('_', '-'): vals[k] for k in vals}
        self.fake_keys = set(self.cache)
        return self


def resolve_op(ref: str) -> str:
    """Resolve a 1Password secret reference (op://...) using the 1Password
    CLI. Raises ConfigHandlerError with the reason if the op CLI is missing or
    fails."""
    try:
        result = subprocess.run(
            ['op', 'read', ref], capture_output=True, text=True)
    except FileNotFoundError as error:
        raise ConfigHandlerError("1Password CLI (op) not found") from error
    if result.returncode != 0:
        raise ConfigHandlerError(
            result.stderr.strip() or
            f"op exited with status {result.returncode}")
    return result.stdout.rstrip('\r\n')


# Value lookups, keyed by URI scheme. A config string value that is exactly
# '<scheme>://...' for a scheme listed here is passed to the matching resolver.
# To add a new lookup mechanism, add a scheme and resolver here.
RESOLVERS = {
    'op': resolve_op,
}


def resolve_secret(value: str, name: str = None) -> str:
    """Strip surrounding whitespace from the value (as config strings always
    have been). If it is then exactly a reference using a known scheme (such
    as op://vault/item/field), resolve it; otherwise return the stripped
    value. On failure, raise ConfigHandlerError naming the config key (if
    given), the reference, and the reason."""
    text = value.strip()
    scheme, sep, _ = text.partition('://')
    if sep and scheme in RESOLVERS:
        try:
            return RESOLVERS[scheme](text)
        except ConfigHandlerError as error:
            where = f"config key {name} ({text})" if name else text
            raise ConfigHandlerError(
                f"Unable to resolve {where}: {error}") from error
    return text
