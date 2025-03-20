from django.core.exceptions import ValidationError


def validate_file_size(file):
    MAX_SIZE= 10
    MAX_SIZE_IN_BYTES= MAX_SIZE * 1024 * 1024
    
    if file.size > MAX_SIZE_IN_BYTES:
        raise ValidationError(f"File can't be larger than {MAX_SIZE} MB")