from django.conf import settings

# HELP Pagination Block Size
HELP_BLOCK_SIZE = getattr(settings, 'HELP_BLOCK_SIZE', 5)

# HELP Pagination Chunk Size
HELP_CHUNK_SIZE = getattr(settings, 'HELP_CHUNK_SIZE', 20)
