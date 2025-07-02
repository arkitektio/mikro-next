# CHANGELOG


## v0.5.0 (2025-06-27)

### Bug Fixes

- Zarr update plus down
  ([`bfb960d`](https://github.com/arkitektio/mikro-next/commit/bfb960db276a77058163949e93a5008911e4a5a7))

### Features

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
