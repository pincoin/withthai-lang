from django.conf import settings

# Article Pagination Block Size
ARTICLE_BLOCK_SIZE = getattr(settings, 'ARTICLE_BLOCK_SIZE', 5)

# ARTICLE Pagination Chunk Size
ARTICLE_CHUNK_SIZE = getattr(settings, 'ARTICLE_CHUNK_SIZE', 20)
