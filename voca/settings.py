from django.conf import settings

# VOCA Pagination Block Size
VOCA_BLOCK_SIZE = getattr(settings, 'VOCA_BLOCK_SIZE', 5)

# VOCA Pagination Chunk Size
VOCA_CHUNK_SIZE = getattr(settings, 'VOCA_CHUNK_SIZE', 3)
