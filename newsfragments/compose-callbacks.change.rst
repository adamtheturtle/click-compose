Replace ``multi_callback`` with the fully typed binary ``compose_callbacks`` primitive.
Compose its result again to build pipelines longer than two callbacks.
The ``deduplicate`` and ``sequence_validator`` helpers now accept the sequence values produced by Click's ``multiple=True`` options rather than optional values.
