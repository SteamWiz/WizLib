# CHANGELOG

<!-- version list -->

## v4.1.0 (2026-10-17)

### Bug Fixes

- Name config key in secret errors, keep stripping plain values, add migration docs
  ([#9](https://github.com/SteamWiz/WizLib/pull/9),
  [`0d1b603`](https://github.com/SteamWiz/WizLib/commit/0d1b603186d0cc066c028965f6a2680d1fb142d1))

- Return None from ConfigHandler.get when a path runs through a non-dict value
  ([#4](https://github.com/SteamWiz/WizLib/pull/4),
  [`fac5068`](https://github.com/SteamWiz/WizLib/commit/fac5068511d48f5150e73e2e20a47664ab89e49f))

### Chores

- MIT license, copyright 2026 Francis Potter
  ([`cc6c98a`](https://github.com/SteamWiz/WizLib/commit/cc6c98a756b47de3a8a48b24fa9661c15e0da801))

- Use shared Dyngle operations from SteamWiz/Conf submodule
  ([`8832b89`](https://github.com/SteamWiz/WizLib/commit/8832b89427fb17fba493649d37bcd49b62dfc65f))

### Continuous Integration

- Name the pull-request workflow 'PR Checks'
  ([`dfcbf1a`](https://github.com/SteamWiz/WizLib/commit/dfcbf1a1dd83ba64490cd9aa2a9961904e48e366))

- Reference steamwiz/actions@v1
  ([`af65357`](https://github.com/SteamWiz/WizLib/commit/af653570e093ead9532ce6c9cd921fd118188bb2))

- Split PR checks from release; read-only PR token, one run per PR
  ([`80a508f`](https://github.com/SteamWiz/WizLib/commit/80a508fd8be38c02e326683e6b4d133eb4221596))

### Documentation

- Remove GitLab reference from changelog
  ([`53257b5`](https://github.com/SteamWiz/WizLib/commit/53257b5f8ae92b3d66d1f57813b1905da3c29c8f))

### Features

- Replace $(...) config substitution with 1Password secret references
  ([#9](https://github.com/SteamWiz/WizLib/pull/9),
  [`c777544`](https://github.com/SteamWiz/WizLib/commit/c77754492a9b28a5b7d4a40a360365f16323c0ff))

- Support explicit key paths in ConfigHandler.get so YAML keys can contain hyphens
  ([#5](https://github.com/SteamWiz/WizLib/pull/5),
  [`2cc6023`](https://github.com/SteamWiz/WizLib/commit/2cc602330dd13c81a8f179719dfd1ed0b619bea5))

### Refactoring

- Dispatch config value references by URI scheme
  ([`f299609`](https://github.com/SteamWiz/WizLib/commit/f299609c49690e26202a6bf1eea09a76c07e477c))

### Breaking Changes

- $(...) shell substitution in config values has been removed. Replace `$(op read "op://...")` with
  the bare `op://...` reference.


## v4.0.8 (2026-10-01)

### Continuous Integration

- Inline publish steps into ci.yml (PyPI reusable workflow OIDC not supported)
  ([`8adffc5`](https://github.com/SteamWiz/WizLib/commit/8adffc5b603dd376a542aebbce86e12d4e276337))

- Remove unused publish.yml and fix stale CI config reference
  ([`b51fc01`](https://github.com/SteamWiz/WizLib/commit/b51fc01c682b918759e8fc8553b1966e563a0989))


## v4.0.7 (2026-07-20)

### Continuous Integration

- Move build job to caller workflow to fix GitHub Actions reusable workflow if: bug
  ([`f35d1a5`](https://github.com/SteamWiz/WizLib/commit/f35d1a5d3b9a871c125e39ca1f6f715e20b28632))


## v4.0.6 (2026-07-20)


## v4.0.5 (2026-07-20)


## v4.0.4 (2026-07-20)


## v4.0.3 (2026-07-20)

### Continuous Integration

- Ignore push to main to prevent concurrency cancellation on PSR commits
  ([`90c891f`](https://github.com/SteamWiz/WizLib/commit/90c891f163ae691fb4f9c5949816b4c884407d38))


## v4.0.2 (2026-07-20)


## v4.0.1 (2026-07-20)

### Bug Fixes

- Grant id-token: write at workflow level for OIDC publish
  ([`437d122`](https://github.com/SteamWiz/WizLib/commit/437d122ee07fa14fe723489641671230a88e601d))

- Set build_command to empty string (PSR v10 requires string not bool)
  ([`2bd4527`](https://github.com/SteamWiz/WizLib/commit/2bd452753e08a44ae3f9d4c09fe7dee038e9c8c1))

### Continuous Integration

- Add publish workflow and align version + PSR config for v4.0.0
  ([`0909caf`](https://github.com/SteamWiz/WizLib/commit/0909cafbc059ab0392b978f9a3b13bddb7aeea26))


## v1.0.1 (2026-07-19)

### Bug Fixes

- Deploy artifact root, not book subdir
  ([`255e0ad`](https://github.com/SteamWiz/WizLib/commit/255e0ada785b34b2239d25648f8e1b6147fde120))

### Continuous Integration

- Trigger Docs workflow to test Cloudflare secrets
  ([`88de3a9`](https://github.com/SteamWiz/WizLib/commit/88de3a943d72a4aacfc5ac495c530bbade61786e))


## v1.0.0 (2026-07-19)

- Initial Release

## v3.4.2 (2026-07-19)

### Chores

- Add semantic_release config for GitHub Actions pipeline
  ([`5773261`](https://github.com/steamwiz/WizLib/commit/57732618f7f1d7905f2879ae2cdb9447dcd446bc))

### Continuous Integration

- Add checks: write permission for test result publishing
  ([`2b58c7c`](https://github.com/steamwiz/WizLib/commit/2b58c7c391b15dfbd86e5088d33ddc054e6d6566))

- Add GitHub Actions workflows for CI and docs
  ([`7d33178`](https://github.com/steamwiz/WizLib/commit/7d3317875c14866d29229b1a73fa2419bc807bb1))

- Add workflow_dispatch trigger with release-level input
  ([`628934a`](https://github.com/steamwiz/WizLib/commit/628934a4c4a1dc70bc84224da35680bb26fd76ed))

- Grant permissions required by reusable pipeline
  ([`5928e06`](https://github.com/steamwiz/WizLib/commit/5928e06afff9f5ec86eac217a9baa3d89a2f9e26))

- Set source-dir explicitly to wizlib (repo renamed to WizLib)
  ([`6b4b054`](https://github.com/steamwiz/WizLib/commit/6b4b054e34643cc0ddd44c5dc8f123e892d27a00))

- Switch to GitHub App credentials for release
  ([`e3f83df`](https://github.com/steamwiz/WizLib/commit/e3f83dfde3f20f28b708aaca21900ffc7c6c4571))

- Trigger after checks permission fix
  ([`43acdf9`](https://github.com/steamwiz/WizLib/commit/43acdf94fb9a04ec83b7a3c67db238ebefb514e6))

- Trigger after coverage checkout fix
  ([`b1c9564`](https://github.com/steamwiz/WizLib/commit/b1c95641a25f3c1ebd5ce6bc37b8001501fd93a0))

- Trigger after coverage path fix
  ([`af70f02`](https://github.com/steamwiz/WizLib/commit/af70f023dc250b3782230d75a1f35874489818dd))

- Trigger after hidden file fix
  ([`3a01a0d`](https://github.com/steamwiz/WizLib/commit/3a01a0d2c1613ccca176c93c54f44a6f2d65dee7))

- Trigger after pipeline rewrite
  ([`1952608`](https://github.com/steamwiz/WizLib/commit/19526087df8596c2f55fcef14db665f600e342fe))

- Trigger after poetry config ordering fix
  ([`878f9cc`](https://github.com/steamwiz/WizLib/commit/878f9ccbe30ee4cd6be043091242125174365886))

- Trigger after Poetry venv fix
  ([`1f64f66`](https://github.com/steamwiz/WizLib/commit/1f64f660bf2a23542320100d03c95e855bcaca07))

- Trigger after release checkout fix
  ([`69f1f17`](https://github.com/steamwiz/WizLib/commit/69f1f17c4be12ee66ca9f03a59ad8779bd2656c1))

- Trigger after removing cache step
  ([`eb9be64`](https://github.com/steamwiz/WizLib/commit/eb9be64e6d59899df0ca0a883dcd2a7d0101d94f))

- Trigger after venv path fix
  ([`1b60a6f`](https://github.com/steamwiz/WizLib/commit/1b60a6f23f35f0a2f0e590501a66d09c03f6527d))

- Trigger after workspace path fix
  ([`e2e6372`](https://github.com/steamwiz/WizLib/commit/e2e637247f73a4c6bfc6c61be4db1d68c431d712))

- Trigger debug run
  ([`b447227`](https://github.com/steamwiz/WizLib/commit/b447227106475257ffc485031bf96c120d288e2b))

- Trigger workflow after v1 tag
  ([`fc2780f`](https://github.com/steamwiz/WizLib/commit/fc2780fdb30bb09e37d09f441f9cb8ca6dd32c4c))


## v1.0.0 (2026-07-19)

- Initial Release
