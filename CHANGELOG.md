# CHANGELOG


## v0.10.0 (2025-07-29)

### Features

- Update to the new mikro schema
  ([`acc0be9`](https://github.com/arkitektio/mikro-next/commit/acc0be968f273164c33cec49fe69abe2d00767be))


## v0.9.0 (2025-07-25)

### Features

- Fix tests plus potential numpy errors
  ([`958724a`](https://github.com/arkitektio/mikro-next/commit/958724ab4c4888df5687adeee358e3d1f52d73a0))


## v0.8.2 (2025-07-24)

### Refactoring

- Organize imports and streamline structure registration
  ([`43088e1`](https://github.com/arkitektio/mikro-next/commit/43088e19eae6aeace610095492bf3116728a5923))


## v0.8.1 (2025-07-24)

### Bug Fixes

- Force numocdes update?
  ([`f1204f1`](https://github.com/arkitektio/mikro-next/commit/f1204f1f23ab4e6b9e6c4f3cf3cf3c244029069a))


## v0.8.0 (2025-07-24)

### Bug Fixes

- Remove python verison constraints
  ([`e9aec80`](https://github.com/arkitektio/mikro-next/commit/e9aec80444a7e96aefe0215cae7cdf13f1076e64))

### Features

- Update zarr
  ([`d2e8c10`](https://github.com/arkitektio/mikro-next/commit/d2e8c1008c62f8127ed3124ab625459f37b89cb6))


## v0.7.2 (2025-07-18)

### Bug Fixes

- Delete all widgets
  ([`b977739`](https://github.com/arkitektio/mikro-next/commit/b977739e947c44cf5edab5ce28b14748aa932f24))


## v0.7.1 (2025-07-11)

### Bug Fixes

- Fixed auth link order after datalayer
  ([`ddb4a8c`](https://github.com/arkitektio/mikro-next/commit/ddb4a8c982209cff82c94903be89b2a3084c5122))

### Chores

- Add some Documentation
  ([`a146601`](https://github.com/arkitektio/mikro-next/commit/a1466012d8bd773abb0afc97c92e00b6974a3456))

- Add token
  ([`4470a23`](https://github.com/arkitektio/mikro-next/commit/4470a2397d26c93a9716d77a0391ceb88c28ef1b))


## v0.7.0 (2025-07-08)

### Bug Fixes

- Added new dev deployment to test
  ([`d355391`](https://github.com/arkitektio/mikro-next/commit/d3553913e47f5fe21e38b359f359d98e41b38043))

### Features

- Typing update
  ([`4aa0035`](https://github.com/arkitektio/mikro-next/commit/4aa0035dbe086f143cde3dff370b53e4f87c0011))


## v0.6.0 (2025-07-02)


## v0.5.0 (2025-06-27)

### Bug Fixes

- Zarr update plus down
  ([`bfb960d`](https://github.com/arkitektio/mikro-next/commit/bfb960db276a77058163949e93a5008911e4a5a7))

### Features

- Add validation tests for FourByFourMatrix and PartialAffineTransformationViewInput
  ([`8a851b8`](https://github.com/arkitektio/mikro-next/commit/8a851b85fc3d4adf8798d62bb3cc0df024b8be68))

- Enhance data layer and upload functionality
  ([`f6faca7`](https://github.com/arkitektio/mikro-next/commit/f6faca76142726e7e74d4c50b24ce1b79923967b))

- Added assertion to ensure `fakt` is a dictionary in `FaktsDataLayer`. - Removed unused imports and
  improved type hints in `upload.py`. - Refactored `apply_recursive` function for better
  readability. - Updated `ImageFileLike`, `MeshLike`, and `FileCoercible` to support
  `io.BufferedReader`. - Deleted unused testing files and directories. - Improved type hinting and
  error handling in `traits.py`. - Refined `rechunk` function in `utils.py` for better type safety.

- Updated arkitekt stack
  ([`32f0f90`](https://github.com/arkitektio/mikro-next/commit/32f0f909daa3c0726cb6339fc32a3ee035c064e7))


## v0.4.0 (2025-05-15)


## v0.3.1 (2025-05-13)

### Bug Fixes

- Update dependencies for rath and koil to latest versions
  ([`df36640`](https://github.com/arkitektio/mikro-next/commit/df36640eace76dc598e28c51aedf97b8cbf24753))

### Features

- Added coercible typing and fixed new upload routines
  ([`4aff17b`](https://github.com/arkitektio/mikro-next/commit/4aff17b387253c27ae19e83528a3d119894096de))


## v0.3.0 (2025-05-09)


## v0.2.0 (2025-05-09)

### Features

- Add readme entry in pyproject.toml and new integration test for dataset creation with parent
  ([`b0ae9ae`](https://github.com/arkitektio/mikro-next/commit/b0ae9ae91b462e5d238c12c1c38325531a3f62d9))


## v0.1.0 (2025-05-09)

### Chores

- Bump version to 0.1.60
  ([`722cb89`](https://github.com/arkitektio/mikro-next/commit/722cb899dfd2da9f7a0e261f6fcc8466d1f52b4f))

### Features

- Add HistogramView and corresponding mutations to support histogram data
  ([`77a8d76`](https://github.com/arkitektio/mikro-next/commit/77a8d762bb69d2222843857c6ea554b886d3e73a))

- Add semantic release configuration and update health check URL formatting
  ([`f538233`](https://github.com/arkitektio/mikro-next/commit/f538233f81cd592528a77b9a45c9149b17e16bdd))

- Added all integrations
  ([`388b9b6`](https://github.com/arkitektio/mikro-next/commit/388b9b6b20e91ae5950485f817258c21ac1f2643))

- Refactor query execution and update storage handling to support large arrays that are first
  computed
  ([`fef521b`](https://github.com/arkitektio/mikro-next/commit/fef521ba37d211b5fd1e4b1d2c4a134019e04322))
