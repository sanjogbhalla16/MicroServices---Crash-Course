# if All Else Fails: Use Pydantic v1

In some cases, redis-om may not fully support Pydantic v2.x. Downgrading to Pydantic v1.x is an option:

pip install "pydantic<2.0"
After downgrading, the configuration using arbitrary_types_allowed=True in the Config class should work.
